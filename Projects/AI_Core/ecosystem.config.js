const path = require("path");

const ROOT_DIR = __dirname;

module.exports = {
  apps: [
    {
      name: "ai-core-ios-listener",
      script: path.join(ROOT_DIR, "src/firestore_listener.py"),
      cwd: ROOT_DIR,
      interpreter: ".venv/bin/python3",
      args: "--env .env",
      instances: 1,
      exec_mode: "fork",
      env: {
        NODE_ENV: "production"
      },
      error_file: "logs/ios-error.log",
      out_file: "logs/ios-out.log",
      log_file: "logs/ios-combined.log",
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
    },
    {
      name: "bybit-monitor",
      script: path.join(ROOT_DIR, "src/bybit_trading_bot.py"),
      cwd: ROOT_DIR,
      interpreter: ".venv/bin/python3",
      args: "--env .env",
      env: {
        BYBIT_MONITOR_ONLY: "false",
        BYBIT_TESTNET: "false"
      },
      error_file: "logs/bybit-error.log",
      out_file: "logs/bybit-out.log",
      log_file: "logs/bybit-combined.log",
      time: true,
      max_memory_restart: "200M",
      watch: false
    }
  ]
};
