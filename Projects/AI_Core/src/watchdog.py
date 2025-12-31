
# ... (imports remain)
import subprocess

# ... (existing logging/config)

class BudgetMonitor:
    def __init__(self):
        self.last_check = 0
        self.check_interval = 3600 * 4  # Check every 4 hours
        self.alert_sent = False

    def check_budget_alerts(self):
        """Scan Gmail for budget alerts > 90%."""
        if time.time() - self.last_check < self.check_interval:
            return

        try:
            # Lazy import to avoid circular dependency issues at module level
            from src.gmail_client import GmailClient
            client = GmailClient()
            if not client.authenticated:
                return

            # Search specifically for budget alerts from Google
            query = "from:CloudPlatform-noreply@google.com subject:budget"
            messages = client.search_emails(query, max_results=3)
            
            for msg in messages:
                snippet = msg.get('snippet', '')
                subject = msg.get('subject', '')
                
                # Check for high percentages
                if "100%" in subject or "150%" in subject or "90%" in subject:
                    # Check date - very recent? (Today/Yesterday)
                    # For now, just reacting to presence of high alert in top 3
                    logger.warning(f"Budget Alert Found: {subject}")
                    
                    # User requested to stop receiving these notifications (2025-12-30)
                    if not self.alert_sent:
                        # send_alert(f"💰 **БЮДЖЕТ ПРЕВЫШЕН!**\nНайдено уведомление: {subject}\n\n⚡ **ПЕРЕКЛЮЧАЮ НА OLLAMA**")
                        self.enforce_ollama()
                        self.alert_sent = True
                        
        except Exception as e:
            logger.error(f"Budget check failed: {e}")
        finally:
            self.last_check = time.time()

    def enforce_ollama(self):
        """Force switch to Ollama in .env and restart bot."""
        env_path = os.path.join(os.path.dirname(__file__), "..", ".env")
        try:
            # Read current env
            with open(env_path, 'r') as f:
                lines = f.readlines()
            
            new_lines = []
            changed = False
            for line in lines:
                if line.startswith("INFERENCE_PROVIDER="):
                    if "ollama" not in line.lower():
                        new_lines.append("INFERENCE_PROVIDER=ollama\n")
                        changed = True
                    else:
                        new_lines.append(line)
                else:
                    new_lines.append(line)
            
            if changed:
                with open(env_path, 'w') as f:
                    f.writelines(new_lines)
                logger.info("Switched INFERENCE_PROVIDER to ollama.")
                
                # Restart service
                os.system("sudo systemctl restart ai-bot")
                logger.info("Restarted ai-bot service.")
            else:
                logger.info("Already on Ollama.")
                
        except Exception as e:
            logger.error(f"Failed to enforce Ollama: {e}")
            send_alert(f"❌ Не удалось переключить на Ollama автоматически: {e}")

def main():
    logger.info("Watchdog started.")
    fail_count = 0
    budget_monitor = BudgetMonitor()
    
    # Wait for bot to start initially
    time.sleep(10)
    
    while True:
        # 1. Health Check
        if check_health():
            if fail_count > 0:
                logger.info("Bot recovered.")
                if fail_count >= FAIL_THRESHOLD:
                    send_alert("✅ Бот восстановился и снова онлайн.")
            fail_count = 0
        else:
            fail_count += 1
            logger.warning(f"Health check failed ({fail_count}/{FAIL_THRESHOLD})")
            
            if fail_count == FAIL_THRESHOLD:
                send_alert(f"⚠️ Бот не отвечает уже {FAIL_THRESHOLD} минут!\nВозможно, он завис или упал.")
                # Auto-restart attempt
                os.system("sudo systemctl restart ai-bot")
        
        # 2. Budget Check
        budget_monitor.check_budget_alerts()
                
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()
