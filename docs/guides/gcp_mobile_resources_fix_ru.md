# Как исправить ошибку в Google Cloud Mobile и открыть все сервисы

## Что видно на скрине

На первом скрине в разделе **Resources**:
- `App Engine not available in this project...`
- в `Compute Engine` и `Kubernetes Engine` нет ресурсов (`No VMs`, `No clusters`).

Это обычно не «поломка приложения», а состояние проекта:
1. Не включены нужные API.
2. Не создано App Engine приложение.
3. Нет созданных ресурсов (VM, дисков, кластеров).
4. Нет нужных IAM прав.
5. Есть активный инцидент в Billing (как на втором скрине), из-за которого часть операций может быть недоступна.

## Быстрый чек-лист (10–15 минут)

1. Открой проект в веб-консоли (не только в мобильном приложении).
2. Проверь Billing:
   - `Billing account` подключен к проекту.
   - Карта/платёжный профиль активны.
3. Включи API:
   - `App Engine Admin API`
   - `Compute Engine API`
   - `Kubernetes Engine API`
   - `Cloud Billing API`
   - `Service Usage API`
4. Создай базовые ресурсы:
   - App Engine app (регион выбрать один раз)
   - 1 VM в Compute Engine
   - (опционально) 1 GKE Autopilot cluster
5. Проверь IAM роли для твоего аккаунта:
   - `Project Owner` или связка `Editor + Billing Account User + Service Usage Admin`
6. Подожди 3–10 минут после включения API (кэш в мобильном интерфейсе).
7. Перезапусти приложение Google Cloud или обнови экран.

## Как включить App Engine (частая причина сообщения "not available")

1. Открой: `https://console.cloud.google.com/appengine`
2. Нажми **Create Application**.
3. Выбери регион (после выбора изменить нельзя).
4. Подтверди создание.

После этого карточка App Engine в мобильном приложении обычно начинает отображаться корректно.

## Почему на втором скрине важен Billing Incident

Если есть активный инцидент по Cloud Billing data processing:
- Метрики/статусы, связанные с биллингом, могут отображаться с задержкой.
- Создание ресурсов иногда проходит, но отчёты по расходам обновляются не сразу.

Это не всегда блокирует работу проекта полностью, но может создавать ощущение «ничего не работает».

## Минимальная диагностика через gcloud

```bash
# 1) Проверить текущий проект
gcloud config get-value project

# 2) Проверить, подключен ли billing
gcloud beta billing projects describe PROJECT_ID

# 3) Список включенных API
gcloud services list --enabled --project PROJECT_ID

# 4) Статус App Engine
gcloud app describe --project PROJECT_ID

# 5) Проверка прав
gcloud projects get-iam-policy PROJECT_ID \
  --flatten="bindings[].members" \
  --format="table(bindings.role, bindings.members)" \
  --filter="bindings.members:YOUR_EMAIL"
```

## Как это связать с твоим VASER Super-Admin GPT

Чтобы GPT действительно «видел и управлял всем», нужны две части:

1. **Control Plane (VASER Control Hub)**
   - хранит доступы (SSH/WinRM/API токены);
   - исполняет команды;
   - логирует и применяет политику безопасности.

2. **Actions в Custom GPT через OpenAPI**
   - GPT вызывает `scan_network`, `get_device_info`, `run_command`, `ha.service_call`, `create_task` и т.д.;
   - Hub валидирует запрос и выполняет его от имени GPT.

Без этих actions GPT в чате не получит «реальный доступ» к инфраструктуре.

## Готовые артефакты в репозитории

В репозитории уже есть основные заготовки под твою цель:
- OpenAPI-манифест Super-Admin: `docs/openapi/vaser_super_admin.yaml`
- Роль Super-Admin: `docs/agent-guidelines/vaser-super-admin-role.md`

Это можно сразу использовать для импорта в Custom GPT Actions и последующей привязки к VASER Hub backend.

## Что делать прямо сейчас (практический план)

1. Починить GCP проект по чек-листу выше (Billing + API + App Engine create).
2. Поднять backend VASER Hub endpoint (`/actions/*`) для всех operationId из OpenAPI.
3. Импортировать `docs/openapi/vaser_super_admin.yaml` в Custom GPT Actions.
4. Прогнать smoke-тесты:
   - `scan_network` (read-only)
   - `ha.get_state`
   - `/local/read`
   - `create_task`
5. Включить confirm-first политику для `run_command`, `remove_device`, `reboot_device`, `configure_device`.

## Короткий вывод

Текущая «ошибка» в Google Cloud Mobile почти наверняка связана с конфигурацией проекта (API/App Engine/IAM/Billing), а не с твоим телефоном. После базовой инициализации проекта и подключения Actions через VASER Hub ты получишь как раз тот уровень управления, который описал: сеть, Home Assistant, локальные команды, облака, менеджмент и аналитика.
