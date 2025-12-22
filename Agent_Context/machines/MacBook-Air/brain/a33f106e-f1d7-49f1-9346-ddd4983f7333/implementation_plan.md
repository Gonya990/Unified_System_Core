# План интеграции SSH (SSH Integration Plan)

## Описание цели
Интегрировать логику управления SSH (из `b64_correct.txt`) в созданную систему "Инструментов" (`instruments.py`). Это позволит агенту (и через веб-интерфейс) выполнять действия на удаленных хостах (NUC, WSL), которые были описаны в исходных файлах проекта.

## Требуется проверка пользователя
> [!NOTE]
> Я перепишу логику PowerShell скрипта на **Python**, чтобы она работала нативно внутри нашего Flask-приложения и реестра инструментов. Будут добавлены инструменты для генерации ключей и выполнения команд.

## Предлагаемые изменения

### Конфигурация
#### [MODIFY] [control_schema.json](file:///Users/macbook/.gemini/antigravity/playground/fiery-rocket/config/control_schema.json)
- Добавить секцию `hosts` с IP адресами для NUC (`100.81.133.25`) и WSL (`100.88.65.71`).
- Добавить настройки для путей SSH ключей.

### Исходный код
#### [NEW] [src/ssh_instruments.py](file:///Users/macbook/.gemini/antigravity/playground/fiery-rocket/src/ssh_instruments.py)
- `ensure_ssh_key()`: Проверяет наличие ключа, генерирует если нужно.
- `deploy_key(host, user)`: Копирует ключ на хост (аналог скрипта).
- `run_remote_command(host, user, command)`: Выполняет команду через SSH.

#### [MODIFY] [src/instruments.py](file:///Users/macbook/.gemini/antigravity/playground/fiery-rocket/src/instruments.py)
- Импорт и регистрация новых инструментов: `ssh_deploy`, `ssh_exec`.

#### [MODIFY] [app.py](file:///Users/macbook/.gemini/antigravity/playground/fiery-rocket/app.py)
- (Опционально) Добавить возможность вызова этих инструментов через API, если это требуется для визуального теста.

## План верификации

### Ручная верификация
- Проверить, что инструменты загружаются.
- Попробовать выполнить команду `ssh_exec` (например `hostname`) на одном из хостов (потребует сетевой доступности).
- Убедиться, что логика генерации ключей соответствует исходному `b64_correct.txt`.
