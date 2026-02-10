module.exports = {
  apps: [
    {
      name: "ai-bot-igor",
      script: "src/ai_telegram_bot_v2.py",
      interpreter: "python3",
      args: "--env .env.igor",
      instances: 1,
      exec_mode: "fork",
      env: {
        NODE_ENV: "production"
      },
      error_file: "logs/igor-error.log",
      out_file: "logs/igor-out.log",
      log_file: "logs/igor-combined.log",
      time: true,
      merge_logs: false,
      max_memory_restart: "500M",
      max_restarts: 10,
      min_uptime: "10s",
      watch: false,
      ignore_watch: [
        "node_modules",
        "logs",
        ".git",
        "*.db",
        "*.log",
        "venv",
        "venv_mac"
      ]
    }
  ]
};
