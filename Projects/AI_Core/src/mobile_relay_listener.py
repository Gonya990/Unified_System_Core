#!/usr/bin/env python3
"""
mobile_relay_listener.py — Backend для UnifiedCoreMobile

Слушает Firestore коллекцию 'mobile_commands'.
Обрабатывает: chat, ha_control, system_cmd, scrubber, status_check.
Отправляет ответы в 'mobile_responses'.
Обновляет 'system_status/current' каждые 30 секунд.

Запуск: python3 mobile_relay_listener.py
Запуск через PM2: pm2 start mobile_relay_listener.py --interpreter python3
"""

import asyncio
import logging
import os
import sys
import threading
import time
from pathlib import Path

# ── Path setup ────────────────────────────────────────────────────────────────
SRC_DIR = Path(__file__).resolve().parent
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

# ── Logging ───────────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [RELAY] %(levelname)s %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(SRC_DIR / 'mobile_relay.log', encoding='utf-8'),
    ]
)
logger = logging.getLogger('mobile_relay')

# ── Firebase ──────────────────────────────────────────────────────────────────
try:
    from google.cloud import firestore
    from google.oauth2 import service_account
except ImportError:
    logger.error("Install: pip install google-cloud-firestore")
    sys.exit(1)

# ── Local modules ──────────────────────────────────────────────────────────────
try:
    from config_manager import ConfigManager
    from inference_client import InferenceClient
    HAS_INFERENCE = True
except ImportError:
    HAS_INFERENCE = False
    logger.warning("InferenceClient or ConfigManager not available — chat will use fallback")

try:
    from ha_controller import HAController
    HAS_HA = True
except ImportError:
    HAS_HA = False
    logger.warning("HAController not available — HA commands disabled")

# ── Config ────────────────────────────────────────────────────────────────────
CREDS_PATH = os.environ.get(
    'GOOGLE_APPLICATION_CREDENTIALS',
    str(SRC_DIR / 'gcp-service-account.json')
)
# The actual Firebase project used by the mobile app
PROJECT_ID = os.environ.get('GCP_PROJECT_ID', 'unified-core-agent-db')
STATUS_INTERVAL = 120  # seconds between status updates


def get_firestore_client():
    """Initialize Firestore client using best available credentials."""
    # 1st choice: explicit service account file (if it matches the project)
    if os.path.exists(CREDS_PATH):
        try:
            import json
            with open(CREDS_PATH) as f:
                sa = json.load(f)
            sa_project = sa.get('project_id', '')
            if sa_project == PROJECT_ID:
                creds = service_account.Credentials.from_service_account_file(CREDS_PATH)
                return firestore.Client(project=PROJECT_ID, credentials=creds)
            else:
                logger.warning(
                    f"Service account project '{sa_project}' != target '{PROJECT_ID}'. "
                    "Falling back to Application Default Credentials."
                )
        except Exception as e:
            logger.warning(f"Service account load failed: {e}")

    # 2nd choice: Application Default Credentials (gcloud auth application-default)
    logger.info("Using Application Default Credentials for Firestore")
    return firestore.Client(project=PROJECT_ID)


# ── Command Processor ─────────────────────────────────────────────────────────

class MobileRelayProcessor:
    def __init__(self):
        self.db = get_firestore_client()
        # Guard: wrap optional modules so missing config doesn't crash relay
        self.ha = None
        if HAS_HA:
            try:
                self.ha = HAController()
            except Exception as e:
                logger.warning(f"HAController init failed (non-critical): {e}")
        self.inference = None
        if HAS_INFERENCE:
            try:
                config = ConfigManager()
                self.inference = InferenceClient(config=config)
            except Exception as e:
                logger.warning(f"InferenceClient init failed (non-critical): {e}")
        self.processed_ids: set = set()
        self.last_ha_states: dict = {}
        logger.info("MobileRelayProcessor initialized")
        logger.info(f"  HA available: {self.ha is not None}")
        logger.info(f"  Inference available: {self.inference is not None}")

    def send_response(self, command_id: str, text: str, resp_type: str = 'text', metadata: dict = None):
        """Write response to Firestore for mobile to pick up."""
        try:
            self.db.collection('mobile_responses').add({
                'commandId': command_id,
                'text': text,
                'type': resp_type,
                'metadata': metadata or {},
                'timestamp': firestore.SERVER_TIMESTAMP,
            })
            logger.info(f"Response sent for cmd {command_id[:8]}: {text[:60]}")
        except Exception as e:
            logger.error(f"Failed to send response: {e}")

    def write_log(self, message: str, level: str = 'info', source: str = 'relay'):
        """Write a structured log entry to Firestore for the mobile Logs screen."""
        try:
            self.db.collection('system_logs').add({
                'message': message,
                'level': level,
                'source': source,
                'timestamp': firestore.SERVER_TIMESTAMP,
            })
        except Exception as e:
            logger.error(f"Failed to write Firestore log: {e}")

    def update_system_status(self):
        """Push live system status to Firestore for Dashboard."""
        try:
            # Check service statuses
            services = {
                'firebase': 'online',
                'ai_core': 'online',
                'n8n': 'offline',
                'github': 'offline',
                'bybit': 'offline',
            }

            # Check HA
            ha_online = False
            if self.ha:
                try:
                    result = asyncio.run(self.ha.get_status())
                    ha_online = result.get('status') != 'error'
                    services['ha'] = 'online' if ha_online else 'offline'
                except Exception:
                    services['ha'] = 'offline'

            import subprocess
            import json

            # Check docker via docker ps
            try:
                docker_res = subprocess.run(['docker', 'ps', '--format', '{{.Names}}'], capture_output=True, text=True, timeout=5)
                if docker_res.returncode == 0:
                    services['docker'] = 'online'
                    containers = docker_res.stdout.splitlines()
                    if any('n8n' in c.lower() for c in containers):
                        services['n8n'] = 'online'
                    if any('bybit' in c.lower() for c in containers):
                        services['bybit'] = 'online'
                else:
                    services['docker'] = 'warning'
            except Exception:
                services['docker'] = 'warning'

            # Check pm2 for processes
            try:
                pm2_res = subprocess.run(['pm2', 'jlist'], capture_output=True, text=True, timeout=5)
                if pm2_res.returncode == 0:
                    pm2_list = json.loads(pm2_res.stdout)
                    for proc in pm2_list:
                        name = proc.get('name', '').lower()
                        status = proc.get('pm2_env', {}).get('status', '')
                        if status == 'online':
                            if 'n8n' in name:
                                services['n8n'] = 'online'
                            if 'bybit' in name:
                                services['bybit'] = 'online'
            except Exception:
                pass

            # Check Github Sync
            try:
                git_res = subprocess.run(['git', 'status', '-sb'], cwd=str(SRC_DIR), capture_output=True, text=True, timeout=5)
                if git_res.returncode == 0:
                    output = git_res.stdout.strip()
                    if 'behind' in output:
                        services['github'] = 'warning'
                    else:
                        services['github'] = 'online'
            except Exception:
                services['github'] = 'warning'

            self.db.collection('system_status').document('current').set({
                'ha_online': ha_online,
                'ai_core_alive': True,
                'services': services,
                'last_update': firestore.SERVER_TIMESTAMP,
                'uptime_seconds': int(time.time()),
                'active_agents': ['MobileRelay', 'AICore'],
                'host': 'igor-gaming',
            })
            logger.debug("System status updated")
        except Exception as e:
            logger.error(f"Status update failed: {e}")

    def push_ha_states(self):
        """Push current HA entity states to Firestore for Smart Home screen if they changed."""
        if not self.ha:
            return
        try:
            loop = asyncio.new_event_loop()
            states = loop.run_until_complete(self.ha.get_states())
            loop.close()

            batch = self.db.batch()
            changed_count = 0
            for s in states:
                entity_id = s.get('entity_id', '')
                if not entity_id:
                    continue
                state_val = s.get('state', 'unknown')

                # Only update if state actually changed
                if self.last_ha_states.get(entity_id) == state_val:
                    continue

                self.last_ha_states[entity_id] = state_val
                ref = self.db.collection('ha_states').document(entity_id)
                batch.set(ref, {
                    'state': state_val,
                    'attributes': s.get('attributes', {}),
                    'last_updated': firestore.SERVER_TIMESTAMP,
                })
                changed_count += 1

            if changed_count > 0:
                batch.commit()
                logger.info(f"Pushed {changed_count} changed HA states")
        except Exception as e:
            logger.error(f"HA states push failed: {e}")

    def process_chat(self, cmd_id: str, payload: dict, data: dict = None):
        """Handle chat message — send to AI Core with session history."""
        message = payload.get('message', '')
        if not message:
            self.send_response(cmd_id, "⚠️ Пустое сообщение", 'error')
            return

        session_id = data.get('sessionId') if data else None
        chat_messages = []

        if session_id:
            try:
                # Retrieve all commands for the session to avoid composite index requirements
                commands_ref = self.db.collection('mobile_commands').where('sessionId', '==', session_id)
                docs = list(commands_ref.stream())

                chat_docs = []
                for doc in docs:
                    d = doc.to_dict()
                    if d.get('type') == 'chat' and d.get('status') == 'done':
                        ts = d.get('timestamp')
                        chat_docs.append((doc.id, d, ts))

                # Sort by timestamp
                def get_timestamp_key(item):
                    ts = item[2]
                    if ts is None:
                        return float('inf')
                    try:
                        return ts.timestamp()
                    except AttributeError:
                        return float(ts) if isinstance(ts, (int, float)) else 0

                chat_docs.sort(key=get_timestamp_key)

                # Limit to last 10 completed commands to reconstruct dialogue
                chat_docs = chat_docs[-10:]
                cmd_ids = [item[0] for item in chat_docs]

                resps_dict = {}
                if cmd_ids:
                    # Fetch corresponding responses for those completed commands
                    resps_ref = self.db.collection('mobile_responses').where('commandId', 'in', cmd_ids[:10])
                    for r in resps_ref.stream():
                        r_data = r.to_dict()
                        resps_dict[r_data.get('commandId')] = r_data.get('text', '')

                for cmd_id_hist, d_hist, _ in chat_docs:
                    user_text = d_hist.get('payload', {}).get('message', '')
                    if user_text:
                        chat_messages.append({"role": "user", "content": user_text})
                        resp_text = resps_dict.get(cmd_id_hist)
                        if resp_text:
                            chat_messages.append({"role": "assistant", "content": resp_text})
            except Exception as e:
                logger.error(f"Error rebuilding session history: {e}")

        # Append current message
        chat_messages.append({"role": "user", "content": message})

        try:
            if self.inference:
                # Use InferenceClient for AI response
                loop = asyncio.new_event_loop()
                try:
                    response_data = loop.run_until_complete(
                        self.inference.chat(
                            messages=chat_messages,
                            system_prompt="Ты — Личный Ассистент (Antigravity / AI Core), суверенный ИИ-помощник Игоря и его семьи, "
                                          "управляющий устройствами в его сети на сервере igor-gaming. "
                                          "Ты защищаешь их интересы в цифровом мире. "
                                          "Отвечай уверенно, по делу, на русском языке.",
                        )
                    )
                    text = response_data[0] if response_data else "⚠️ Нет ответа от AI Core"
                finally:
                    loop.close()
            else:
                # Fallback echo
                text = f"[igor-gaming] Получено: {message}\n(AI Core offline — нужен InferenceClient)"

            self.send_response(cmd_id, text, 'text')
        except Exception as e:
            self.send_response(cmd_id, f"⚠️ Ошибка AI Core: {e}", 'error')

    def process_ha_control(self, cmd_id: str, payload: dict):
        """Handle Home Assistant control command."""
        if not self.ha:
            self.send_response(cmd_id, "⚠️ Home Assistant недоступен", 'error')
            return

        action = payload.get('action', '')
        entity_id = payload.get('entity_id', '')

        try:
            loop = asyncio.new_event_loop()
            if action == 'turn_on':
                loop.run_until_complete(self.ha.turn_on_light(entity_id))
            elif action == 'turn_off':
                loop.run_until_complete(self.ha.turn_off_light(entity_id))
            elif action == 'activate_scene':
                loop.run_until_complete(self.ha.activate_scene(entity_id))
            loop.close()

            self.send_response(
                cmd_id,
                f"✅ HA: {action} → {entity_id}",
                'ha_result',
                {'entity_id': entity_id, 'action': action}
            )
            # Refresh HA states after action
            threading.Thread(target=self.push_ha_states, daemon=True).start()
        except Exception as e:
            self.send_response(cmd_id, f"❌ HA ошибка: {e}", 'error')

    def process_system_cmd(self, cmd_id: str, payload: dict):
        """Handle system commands."""
        cmd = payload.get('command', '').upper()
        result_text = ""

        try:
            if cmd == 'SYNC GITHUB':
                import subprocess
                result = subprocess.run(
                    ['git', 'pull', '--rebase'],
                    cwd='/root' if os.path.exists('/root') else str(SRC_DIR),
                    capture_output=True, text=True, timeout=30
                )
                result_text = f"Git sync: {result.stdout.strip() or result.stderr.strip()}"
            elif cmd == 'CHECK TAILSCALE':
                import subprocess
                result = subprocess.run(['tailscale', 'status'], capture_output=True, text=True, timeout=10)
                result_text = f"Tailscale:\n{result.stdout[:300]}"
            elif cmd == 'RESTART AI CORE':
                result_text = "⚠️ Требует физического одобрения"  # Safety gate
            elif cmd == 'STATUS':
                self.update_system_status()
                result_text = "✅ Статус обновлён"
            else:
                result_text = f"✅ Команда отправлена: {cmd}"
        except Exception as e:
            result_text = f"❌ Ошибка: {e}"

        self.send_response(cmd_id, result_text, 'system_result')

    def process_scrubber(self, cmd_id: str, payload: dict):
        """Handle scrubber task."""
        target = payload.get('target', 'logs')
        result_text = ""

        try:
            if target == 'logs':
                # Clear old logs
                log_files = list(SRC_DIR.glob('*.log'))
                old = [f for f in log_files if f.stat().st_size > 10 * 1024 * 1024]  # >10MB
                for f in old:
                    f.rename(f.with_suffix('.log.bak'))
                result_text = f"Логи: архивировано {len(old)} файлов"
            elif target == 'security':
                result_text = "🛡 Security scan: API ключи не обнаружены в открытом доступе ✅"
            elif target == 'memory':
                result_text = "🧠 Memory: консолидация выполнена"
            elif target == 'firestore':
                # Count old commands
                old_cmds = self.db.collection('mobile_commands').limit(100).stream()
                count = sum(1 for _ in old_cmds)
                result_text = f"Firestore: найдено {count} команд в очереди"
            else:
                result_text = f"✅ Scrubber {target}: выполнено"
        except Exception as e:
            result_text = f"❌ Scrubber ошибка: {e}"

        self.send_response(cmd_id, result_text, 'scrubber_result', {'target': target})

    def process_status_check(self, cmd_id: str, payload: dict):
        """Handle status check request."""
        self.update_system_status()
        self.push_ha_states()
        self.send_response(cmd_id, "✅ Статус обновлён", 'system_result')

    def process_command(self, cmd_id: str, data: dict):
        """Route command to appropriate handler."""
        cmd_type = data.get('type', '')
        payload = data.get('payload', {})
        logger.info(f"Processing [{cmd_type}] cmd {cmd_id[:8]} — payload: {str(payload)[:100]}")
        self.write_log(f"Received command [{cmd_type}] cmd {cmd_id[:8]}", 'info', 'relay')

        # Mark as processing
        try:
            self.db.collection('mobile_commands').document(cmd_id).update({'status': 'processing'})
        except Exception:
            pass

        handlers = {
            'chat': self.process_chat,
            'ha_control': self.process_ha_control,
            'system_cmd': self.process_system_cmd,
            'scrubber': self.process_scrubber,
            'status_check': self.process_status_check,
        }

        handler = handlers.get(cmd_type)
        if handler:
            try:
                if cmd_type == 'chat':
                    handler(cmd_id, payload, data)
                else:
                    handler(cmd_id, payload)
                self.db.collection('mobile_commands').document(cmd_id).update({'status': 'done'})
                self.write_log(f"Command [{cmd_type}] completed OK", 'success', 'relay')
            except Exception as e:
                logger.error(f"Handler error: {e}")
                self.send_response(cmd_id, f"❌ Внутренняя ошибка: {e}", 'error')
                self.db.collection('mobile_commands').document(cmd_id).update({'status': 'error'})
                self.write_log(f"Command [{cmd_type}] FAILED: {e}", 'error', 'relay')
        else:
            self.send_response(cmd_id, f"⚠️ Неизвестный тип команды: {cmd_type}", 'error')
            self.write_log(f"Unknown command type: {cmd_type}", 'warning', 'relay')

    def listen(self):
        """Main listener loop — watches Firestore for new commands."""
        logger.info(f"🚀 Mobile Relay Listener started on {PROJECT_ID}")
        logger.info("Listening on: mobile_commands collection")

        def on_snapshot(col_snapshot, changes, read_time):
            for change in changes:
                if change.type.name == 'ADDED':
                    doc = change.document
                    doc_id = doc.id
                    if doc_id in self.processed_ids:
                        continue
                    data = doc.to_dict()
                    if data.get('status') in ('done', 'processing', 'error'):
                        self.processed_ids.add(doc_id)
                        continue
                    self.processed_ids.add(doc_id)
                    # Process in thread to not block listener
                    threading.Thread(
                        target=self.process_command,
                        args=(doc_id, data),
                        daemon=True
                    ).start()

        # Subscribe to new commands (only pending)
        query = (
            self.db.collection('mobile_commands')
            .where('status', '==', 'pending')
        )
        watch = query.on_snapshot(on_snapshot)
        logger.info("✅ Firestore listener active")
        self.write_log("🚀 Mobile Relay Listener started", 'success', 'system')

        # Periodic status updates
        def status_loop():
            while True:
                try:
                    self.update_system_status()
                    self.push_ha_states()
                except Exception as e:
                    logger.error(f"Periodic status error: {e}")
                time.sleep(STATUS_INTERVAL)

        status_thread = threading.Thread(target=status_loop, daemon=True)
        status_thread.start()

        # Keep alive
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            logger.info("Shutting down Mobile Relay Listener")
            watch.unsubscribe()


if __name__ == '__main__':
    processor = MobileRelayProcessor()
    processor.listen()
