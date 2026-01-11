# Implementation Plan - System Integration and Audit

# План реализации - Системная интеграция и аудит

# Goal Description / Описание цели

Consolidate the existing working zones (`Projects/AI_Core`, `Home_Assistant_Config`, `Sandbox`) into a cohesive structure. Refactor the main check script `admin_check.sh` to be a central utility, fully localized to Russian, and ensure it correctly validates the compiled resources (Admins: igor/gonya).
Объединить существующие рабочие зоны в единую структуру. Рефакторинг `admin_check.sh` в центральную утилиту на русском языке.

## User Review Required / Требуется проверка пользователя
>
> [!IMPORTANT]
> **Security Warning / Предупреждение о безопасности**:
> Found sensitive files in `Home_Assistant_Config` (`Токен ХА для Васи.odt`, `ключи Ngrok.odt`).
> **Action**: These should eventually be moved to a secure vault (e.g., 1Password/Bitwarden) or environment variables. For this task, I will leave them but log a warning.
> **Действие**: Эти файлы следует переместить в безопасное хранилище. В рамках этой задачи я оставлю их, но добавлю предупреждение.

## Proposed Changes / Предлагаемые изменения

### Directory Structure / Структура папок

Reorganize `Unified_System` to have a dedicated scripts area.
Переорганизация `Unified_System` для выделения области скриптов.

#### [NEW] [Unified_System/Scripts](file:///Users/macbook/Documents/Unified_System/Scripts)

- Create directory for shared system scripts.

#### [MODIFY] [admin_check.sh](file:///Users/macbook/Documents/Unified_System/Sandbox/admin_check.sh)

- **Move** to `Unified_System/Scripts/admin_check.sh`.
- **Translate** all comments to Russian.
- **Refactor** to verify existence of `Projects/AI_Core` and `Home_Assistant_Config`.
- **Update** "Resource Inventory" section to be dynamic (check if folders exist).

### Component: Projects/AI_Core

- No code changes planned, but will be referenced in the central check script.
- Без изменений кода, но будет добавлен в проверку.

### Component: Home_Assistant_Config

- No code changes planned, but will be referenced in the central check script.
- Без изменений кода, но будет добавлен в проверку.

## Verification Plan / План проверки

### Automated Tests / Автоматические тесты

- Run the refactored `admin_check.sh` and verify output.
  - Command: `bash /Users/macbook/Documents/Unified_System/Scripts/admin_check.sh`
- Verify it correctly identifies the current user (macbook/igor/gonya).
- Verify it correctly detects the sub-directories.

### Manual Verification / Ручная проверка

- **User Action**: Run the script and confirm the "Inventory" section matches reality.
- **User Action**: Confirm the output language is strictly Russian.
