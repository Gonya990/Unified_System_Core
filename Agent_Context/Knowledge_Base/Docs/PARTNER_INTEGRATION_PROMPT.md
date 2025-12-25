# 🚀 Unified System: Partner Agent Integration Prompt

# 🚀 Unified System: Промпт для подготовки партнерского агента

> **Usage:** Copy and send this prompt to the AI Agent managing the partner repository to synchronize environments.  
> **Использование:** Скопируйте и отправьте этот промпт AI-агенту, управляющему партнерским репозиторием, для синхронизации окружений.

---

## 🤖 Integration Request / Запрос на интеграцию

**System Goal:** Enable "Federated Swarm" mode between our repositories. We need to standardize our structure to share tasks and resources via Tailscale while keeping personal data private.  
**Цель системы:** Включить режим «Федеративного роя» между нашими репозиториями. Нам нужно стандартизировать структуру для совместного использования задач и ресурсов через Tailscale, сохраняя конфиденциальность личных данных.

### Step 1: Repository Restructuring / Шаг 1: Реструктуризация репозитория

Please reorganize your `Knowledge_Base` folder into the following tiered structure:
Пожалуйста, организуйте вашу папку `Knowledge_Base` в следующую многоуровневую структуру:

1. **`/Knowledge_Base/Shared/`**: Create this for protocols, global task boards, and shared architectures.
2. **`/Knowledge_Base/Private/Admin_[Your_Name]/`**: Move all your personal session logs, `.env` files, and local configs here.
3. **`.gitignore`**: Ensure `Private/` directories and sensitive files are excluded from git or marked for local-only sync.

### Step 2: Protocol Support / Шаг 2: Поддержка протоколов

Verify and implement the following components:
Проверьте и внедрите следующие компоненты:

- **Tailscale Connectivity**: Confirm your machine is on the mesh network. Provide your internal IP.
- **Browser Automation (ndc)**: Ensure the `ndc` (Nodriver CLI) daemon is set up for token-efficient browser control.
- **WIP Commit Strategy**: Adopt the `WIP: <agent-id> - <desc>` commit style. Never use `git stash` to avoid invisible blocks.

### Step 3: Privacy Filter / Шаг 3: Фильтр приватности

Adopt the "Zero-Bleed" policy:
Примите политику «Zero-Bleed» (нулевая утечка):

- Never share data from `Private/` with my agent unless explicitly asked.
- Before sending context to me, scan it for API keys, passwords, or personal identifying information.

### Step 4: Documentation / Шаг 4: Документация

Create a `PARTNER_STATUS.md` in your `Shared/` folder with:
Создайте файл `PARTNER_STATUS.md` в вашей папке `Shared/` со следующей информацией:

- Your Agent ID and Role.
- List of available resources (e.g., "Ollama GPU available", "Fast Fiber Internet").
- Your current primary task.

---

**Are you ready to begin the reorganization? Please report your current Tailscale IP and confirmation of the new structure.**  
**Вы готовы начать реорганизацию? Пожалуйста, сообщите ваш текущий Tailscale IP и подтвердите готовность новой структуры.**
