
# 🏭 Vibranium Token Factory Dashboard

Current Status: **HEALTHY** 🟢
Encryption: **Argon2id** 🔐

### 📊 Pool Status

| Provider | Alias | Tier | Status | Last Health Check |
| :--- | :--- | :--- | :--- | :--- |
| **OpenAI** | Igor-OpenAI-Primary | Pro | Active ✅ | Just now |
| **Gemini** | Igor-Gemini-Cloud | Free | Active ✅ | Just now |
| **Anthropic** | Igor-OpenRouter-Claude | Pro | Active ✅ | Just now |
| **GitHub** | Igor-GitHub-Models | Pro | Active ✅ | Just now |
| **ByBit** | Main-Trading-Account | Pro | Active ✅ | Just now |

---

### 🕹️ Interactive Controls

Run these commands directly in your terminal to manage the factory:

- **Check Status:** `python3 Projects/AI_Core/src/token_broker.py status`
- **Force Rotate:** `python3 Projects/AI_Core/src/token_broker.py rotate`
- **Add New Token:** `python3 Projects/AI_Core/src/token_broker.py add --provider <name> --key <key>`

---

### 🛠️ Configuration

The encrypted vault is located at: `~/.config/unified-system/tokens.yaml`

> **Note:** The "6 models" selection in your side panel is now backed by this factory. If one key fails, the TokenBroker will automatically swap it for the next valid one in the pool, ensuring your bots never stop.
