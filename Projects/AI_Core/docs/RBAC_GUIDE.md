# Granular Access Control (RBAC) System

## Философия

**"Каждому индивидууму - свои права доступа к проектам и наработкам"**

Система детализированного контроля доступа основана на принципе разделения прав между пользователями, обеспечивая безопасность и приватность данных каждого.

---

## Архитектура

### 1. Иерархия ролей (Role Hierarchy)

```
OWNER > ADMIN > DEVELOPER > MEMBER > FAMILY > GUEST
```

- **OWNER**: Полный контроль системы (создатель/основатель)
- **ADMIN**: Административный доступ ко всем проектам
- **DEVELOPER**: Доступ к разработке и кодовой базе
- **MEMBER**: Базовый доступ к общим ресурсам
- **FAMILY**: Доступ к семейным проектам (Morning Brief, Homework)
- **GUEST**: Минимальный доступ только для чтения

### 2. Области проектов (Project Scopes)

- **AI_CORE**: Telegram Bot & AI Infrastructure
- **CONTENT_FACTORY**: Video/Content Generation
- **FAMILY_ASSISTANT**: Morning Brief, Homework Tracking
- **AUTOMATION**: Scripts and automation tools
- **KNOWLEDGE_BASE**: Personal knowledge management
- **FINANCE**: Financial tracking
- **HEALTH**: Health tracking integration
- **INFRASTRUCTURE**: System-wide infrastructure
- **PERSONAL**: User's personal data
- **GLOBAL**: System-wide access

### 3. Детализированные разрешения (Permissions)

- **READ**: Просмотр/чтение ресурса
- **WRITE**: Создание/редактирование ресурса
- **EXECUTE**: Запуск/выполнение действий
- **DELETE**: Удаление ресурса
- **ADMIN**: Полный административный доступ
- **SHARE**: Предоставление доступа другим
- **MANAGE_USERS**: Управление пользователями

---

## Практические примеры использования

### Scenario 1: Настройка семейного доступа

```python
from rbac import RBACManager, ProjectScope, Role, create_family_member_access

# Инициализация
rbac = RBACManager(db)

# Владелец системы (вы)
owner_id = 708531393  # Igor
rbac.grant_role(owner_id, Role.OWNER, ProjectScope.GLOBAL, granted_by=owner_id)

# Член семьи (например, Костя)
family_member_id = 578363419
create_family_member_access(rbac, family_member_id, granted_by=owner_id)

# Результат: Костя имеет доступ к Family Assistant, но не к AI Core
```

### Scenario 2: Привлечение разработчика

```python
from rbac import create_developer_access

# Новый разработчик для Content Factory
developer_id = 123456789
create_developer_access(rbac, developer_id, granted_by=owner_id)

# Результат: разработчик может читать/писать/запускать код, но не может удалять
```

### Scenario 3: Временный доступ к проекту

```python
from rbac import Permission

# Дать другу временный доступ к Knowledge Base (только чтение)
friend_id = 987654321
rbac.grant_permissions(
    friend_id,
    ProjectScope.KNOWLEDGE_BASE,
    {Permission.READ},
    granted_by=owner_id
)

# Позже отозвать доступ
rbac.revoke_permissions(friend_id, ProjectScope.KNOWLEDGE_BASE)
```

### Scenario 4: Ресурс-специфичный доступ

```python
# Дать доступ только к конкретному скрипту в Automation
rbac.grant_permissions(
    user_id=888888,
    project=ProjectScope.AUTOMATION,
    permissions={Permission.READ, Permission.EXECUTE},
    resource="morning_brief.py",
    granted_by=owner_id
)

# Проверка доступа
can_execute = rbac.check_permission(
    user_id=888888,
    project=ProjectScope.AUTOMATION,
    permission=Permission.EXECUTE,
    resource="morning_brief.py"
)
```

---

## Telegram Bot Commands

### Административные команды

#### `/grant_access <user_id> <project> <role>`

Предоставить доступ пользователю к проекту

**Примеры:**

```
/grant_access 123456 ai_core developer
/grant_access 789012 family_assistant family
/grant_access 555777 knowledge_base member
```

#### `/revoke_access <user_id> <project>`

Отозвать доступ пользователя к проекту

**Пример:**

```
/revoke_access 123456 ai_core
```

#### `/my_permissions [user_id]`

Показать свои разрешения (или разрешения другого пользователя для админов)

**Примеры:**

```
/my_permissions           # Ваши права
/my_permissions 123456    # Права user 123456 (admin only)
```

#### `/project_users <project>`

Показать всех пользователей с доступом к проекту (admin only)

**Пример:**

```
/project_users ai_core
```

#### `/audit_log [limit]`

Показать лог доступа (admin only)

**Пример:**

```
/audit_log 50
```

---

## Использование в коде

### Проверка доступа в обработчике команд

```python
from rbac import ProjectScope, Permission

async def sensitive_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    rbac = context.bot_data['identity'].rbac
    
    # Проверить, может ли пользователь выполнить действие
    if not rbac.check_permission(
        user_id, 
        ProjectScope.CONTENT_FACTORY, 
        Permission.EXECUTE
    ):
        await update.message.reply_text("⛔ Недостаточно прав")
        return
    
    # Выполнить защищенное действие
    await update.message.reply_text("✅ Действие выполнено")
```

### Декоратор для защиты функций

```python
from functools import wraps
from rbac import ProjectScope, Permission

def require_permission(project: ProjectScope, permission: Permission):
    """Декоратор для проверки прав доступа"""
    def decorator(func):
        @wraps(func)
        async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
            user_id = update.effective_user.id
            rbac = context.bot_data['identity'].rbac
            
            if not rbac.check_permission(user_id, project, permission):
                await update.message.reply_text(
                    f"⛔ Требуется разрешение: {permission.value} для {project.value}"
                )
                return
            
            return await func(update, context)
        return wrapper
    return decorator

# Использование
@require_permission(ProjectScope.AUTOMATION, Permission.EXECUTE)
async def run_automation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Этот код выполнится только если у пользователя есть права
    ...
```

---

## Миграция с legacy role system

Система полностью обратно совместима:

- **Legacy ADMIN/MEMBER/GUEST** роли продолжают работать
- Автоматическая миграция: ADMIN = глобальный доступ ко всему
- Новые пользователи получают детализированные права
- Постепенный переход: можно использовать обе системы параллельно

---

## Аудит и безопасность

### Отслеживание доступа

Все проверки прав логируются в `access_audit_log`:

- user_id
- project
- resource
- permission_checked
- access_granted (true/false)
- timestamp
- context

### Просмотр аудита

```python
# Последние 100 попыток доступа
logs = rbac.get_audit_log(limit=100)

# Фильтр по пользователю
user_logs = rbac.get_audit_log(user_id=123456, limit=50)

# Фильтр по проекту
project_logs = rbac.get_audit_log(project=ProjectScope.AI_CORE, limit=50)
```

---

## Рекомендации по безопасности

1. **Принцип минимальных привилегий**: Давайте только необходимые права
2. **Регулярный аудит**: Проверяйте логи доступа
3. **Временный доступ**: Отзывайте права после завершения задач
4. **Разделение проектов**: Используйте project scopes для изоляции
5. **Resource-level control**: Для критических данных используйте ресурсный уровень

---

## FAQ

**Q: Как дать пользователю доступ ко всей системе?**
A: `rbac.grant_role(user_id, Role.ADMIN, ProjectScope.GLOBAL)`

**Q: Как ограничить доступ только к одному скрипту?**
A: Используйте параметр `resource` в `grant_permissions()`

**Q: Можно ли временно ограничить права?**
A: Да, просто вызовите `revoke_permissions()` когда нужно

**Q: Что если я удалю все права пользователя?**
A: Legacy роль (GUEST) всё равно даст базовый READ доступ

**Q: Как узнать, кто дал мне доступ?**
A: Используйте `/my_permissions` - увидите `granted_by`

---

## Roadmap

- [ ] Time-based permissions (автоматическое истечение)
- [ ] Permission groups (группы пользователей)
- [ ] API key-based access (для внешних интеграций)
- [ ] Two-factor for sensitive operations
- [ ] Notification on permission changes

---

**Built with ❤️ for the Unified System**  
*Protecting each individual's digital footprint*
