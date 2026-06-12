import asyncio
import logging
import threading
import time

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("MobileRelayListener")

# Local AI Core imports
from config_manager import ConfigManager
from firestore_db import get_db
from inference_client import InferenceClient

# Initialize Core Components
config = ConfigManager()
inference = InferenceClient(config)
db = get_db()

if not db.use_firestore:
    logger.error("Firestore is not enabled or credentials are missing.")
    exit(1)


def process_command_async(doc_id, data):
    async def _process():
        try:
            cmd_type = data.get('type', 'chat')
            payload = data.get('payload', {})
            session_id = data.get('sessionId', 'unknown')

            logger.info(f"Processing command {doc_id} of type {cmd_type}")

            from google.cloud import firestore

            if cmd_type == 'chat':
                user_text = payload.get('message', '')

                # Update Firestore history for the user (Memory)
                user_id = data.get('deviceId') or config.get("ADMIN_ID", "admin")
                history = db.get_conversation(user_id) or []
                history.append({"role": "user", "content": user_text})

                if len(history) > 10:
                    history = history[-10:]
                db.save_conversation(user_id, history)

                context = "\n".join([f"{msg['role']}: {msg['content']}" for msg in history])
                prompt = f"Conversation History:\n{context}\n\nRespond to the last message."

                logger.info("Generating AI response...")
                response_text = await inference.complete(prompt)

                history.append({"role": "assistant", "content": response_text})
                db.save_conversation(user_id, history)

                # Write to mobile_responses
                db.db.collection('mobile_responses').add({
                    'commandId': doc_id,
                    'text': response_text,
                    'type': 'text',
                    'timestamp': firestore.SERVER_TIMESTAMP
                })

            elif cmd_type == 'ha_control':
                import os

                import requests
                action = payload.get('action')
                entity_id = payload.get('entity_id')
                logger.info(f"Relaying HA command: {action} on {entity_id}")

                ha_token = config.get("HA_TOKEN")
                ha_url = os.environ.get("HA_URL", "http://192.168.1.189:8123")

                response_text = "Failed to send HA command"
                if ha_token:
                    headers = {
                        "Authorization": f"Bearer {ha_token}",
                        "Content-Type": "application/json"
                    }
                    domain = entity_id.split('.')[0] if entity_id and '.' in entity_id else "homeassistant"
                    url = f"{ha_url}/api/services/{domain}/{action}"
                    try:
                        res = requests.post(url, headers=headers, json={"entity_id": entity_id}, timeout=5)
                        if res.ok:
                            response_text = f"HA Command {action} for {entity_id} successful."
                        else:
                            response_text = f"HA Command failed: {res.status_code} {res.text}"
                    except Exception as e:
                        response_text = f"HA Request error: {e}"
                else:
                    response_text = "HA_TOKEN not configured in ConfigManager."

                db.db.collection('mobile_responses').add({
                    'commandId': doc_id,
                    'text': response_text,
                    'type': 'ha_result',
                    'timestamp': firestore.SERVER_TIMESTAMP
                })

            elif cmd_type == 'status_check':
                db.db.collection('system_status').document('current').set({
                    'ha_online': True,
                    'ai_core_alive': True,
                    'services': {
                        'firestore': 'online',
                        'ai_core': 'online'
                    },
                    'last_update': firestore.SERVER_TIMESTAMP,
                    'uptime_seconds': 999,
                    'active_agents': ['relay']
                }, merge=True)

            # Update original command status
            db.db.collection('mobile_commands').document(doc_id).update({'status': 'done'})
            logger.info(f"Finished processing command {doc_id}")

        except Exception as e:
            logger.error(f"Error processing command {doc_id}: {e}")
            db.db.collection('mobile_commands').document(doc_id).update({'status': 'error'})

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(_process())
    loop.close()


def on_snapshot(col_snapshot, changes, read_time):
    for change in changes:
        if change.type.name == 'ADDED':
            doc = change.document
            data = doc.to_dict()

            if data.get('status') == 'pending':
                logger.info(f"Detected new command: {doc.id}")
                doc.reference.update({'status': 'processing'})
                threading.Thread(target=process_command_async, args=(doc.id, data)).start()


def main():
    logger.info("Starting Unified Mobile Relay Listener...")

    col_query = db.db.collection('mobile_commands').where('status', '==', 'pending')
    col_watch = col_query.on_snapshot(on_snapshot)

    logger.info("Listening for new mobile commands in real-time...")

    # Periodically update system status
    def update_status():
        while True:
            try:
                from google.cloud import firestore
                db.db.collection('system_status').document('current').set({
                    'ai_core_alive': True,
                    'last_update': firestore.SERVER_TIMESTAMP
                }, merge=True)
            except Exception as e:
                logger.error(f"Status update failed: {e}")
            time.sleep(60)

    threading.Thread(target=update_status, daemon=True).start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("Shutting down Mobile Relay Listener.")

if __name__ == '__main__':
    main()
