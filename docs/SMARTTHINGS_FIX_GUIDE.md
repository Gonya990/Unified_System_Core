# 🔧 SmartThings - Полное Руководство по Исправлению

## 📊 Проблема

**Ошибка:** `Reached limit of subscriptions`  
**Затронуто:** 27 устройств SmartThings  
**Причина:** Накопление старых webhook подписок от предыдущих установок Home Assistant

---

## 🎯 Архитектура SmartThings

### Основные Компоненты

1. **SmartThings Cloud** - центральная платформа
2. **Locations** - логические группы (дом, офис и т.д.)
   - До 10 локаций на аккаунт
   - Содержат: Rooms, Devices, Hubs, Automations
3. **Devices** - физические устройства:
   - Hub Connected (Zigbee, Z-Wave, Matter, LAN)
   - Cloud Connected (через сторонние облака)
   - Direct Connected (WiFi напрямую)
   - Mobile Connected (через телефон)
4. **Subscriptions** - webhook подписки для событий устройств

### Как Работают Подписки

- Каждая интеграция (например, Home Assistant) создает **InstalledApp**
- InstalledApp создает **webhook subscriptions** для каждого устройства
- Подписки остаются активными до явного удаления
- **Лимит:** ~40 подписок каждые 15 минут на InstalledApp

**Проблема:** При переустановке HA старые подписки не удаляются автоматически!

---

## 🛠️ Решение 1: Через SmartThings CLI (Рекомендуется)

### Шаг 1: Установка SmartThings CLI

```bash
# На macOS
npm install -g @smartthings/cli

# Проверка установки
smartthings --version
```

### Шаг 2: Авторизация

```bash
# Войти в аккаунт Samsung
smartthings login

# Откроется браузер для авторизации
# Следуйте инструкциям
```

### Шаг 3: Просмотр Установленных Приложений

```bash
# Список всех InstalledApps
smartthings apps:installed:list

# Вывод будет примерно таким:
# ┌────────────────────────────────────┬─────────────────┬──────────────┐
# │ ID                                 │ Display Name    │ App ID       │
# ├────────────────────────────────────┼─────────────────┼──────────────┤
# │ abc123-def456-ghi789               │ Home Assistant  │ ha-app-001   │
# │ xyz789-uvw456-rst123               │ Home Assistant  │ ha-app-002   │  <- Старая!
# │ mno345-pqr678-stu901               │ Home Assistant  │ ha-app-003   │  <- Старая!
# └────────────────────────────────────┴─────────────────┴──────────────┘
```

### Шаг 4: Удаление Старых Приложений

```bash
# Удалить конкретное приложение по ID
smartthings apps:installed:delete xyz789-uvw456-rst123

# Подтвердите удаление
# Это автоматически удалит все связанные подписки!
```

### Шаг 5: Проверка Подписок

```bash
# Список всех подписок (опционально)
smartthings subscriptions:list

# Если остались orphaned подписки, удалите вручную:
smartthings subscriptions:delete <subscription-id>
```

---

## 🛠️ Решение 2: Через SmartThings API

### Шаг 1: Получение Personal Access Token (PAT)

1. Перейдите: <https://account.smartthings.com/tokens>
2. Войдите с аккаунтом Samsung
3. Нажмите **"Generate new token"**
4. Выберите разрешения:
   - ✅ `r:installedapps`
   - ✅ `w:installedapps`
   - ✅ `r:devices:*`
   - ✅ `w:devices:*`
   - ✅ `r:locations:*`
5. Сохраните токен (показывается только один раз!)

### Шаг 2: Список InstalledApps через API

```bash
# Замените YOUR_PAT на ваш токен
curl -X GET "https://api.smartthings.com/v1/installedapps" \
  -H "Authorization: Bearer YOUR_PAT" \
  -H "Accept: application/json"
```

**Ответ:**

```json
{
  "items": [
    {
      "installedAppId": "abc123-def456-ghi789",
      "displayName": "Home Assistant",
      "appId": "ha-app-001",
      "installedAppStatus": "AUTHORIZED"
    },
    {
      "installedAppId": "xyz789-uvw456-rst123",
      "displayName": "Home Assistant",
      "appId": "ha-app-002",
      "installedAppStatus": "AUTHORIZED"
    }
  ]
}
```

### Шаг 3: Удаление InstalledApp

```bash
# Удалить старое приложение
curl -X DELETE "https://api.smartthings.com/v1/installedapps/xyz789-uvw456-rst123" \
  -H "Authorization: Bearer YOUR_PAT"
```

### Шаг 4: Проверка Подписок

```bash
# Список всех подписок
curl -X GET "https://api.smartthings.com/v1/installedapps/abc123-def456-ghi789/subscriptions" \
  -H "Authorization: Bearer YOUR_PAT"
```

---

## 🛠️ Решение 3: Через Home Assistant (Самый Простой)

### Вариант A: Полная Переустановка

1. **Остановите Home Assistant:**

   ```bash
   ssh unified-home-core
   systemctl stop home-assistant@homeassistant
   ```

2. **Удалите конфигурацию SmartThings:**

   ```bash
   cd /config/.storage/
   
   # Бэкап на всякий случай
   cp core.config_entries core.config_entries.backup
   cp smartthings smartthings.backup
   
   # Удалите SmartThings записи
   rm smartthings
   
   # Отредактируйте core.config_entries
   nano core.config_entries
   # Найдите и удалите весь блок с "domain": "smartthings"
   ```

3. **Запустите Home Assistant:**

   ```bash
   systemctl start home-assistant@homeassistant
   ```

4. **Добавьте SmartThings заново:**
   - Откройте HA Web UI
   - Настройки → Устройства и Сервисы → Добавить интеграцию
   - Найдите "SmartThings"
   - Следуйте инструкциям

### Вариант B: Через SmartThings Mobile App

1. Откройте **SmartThings App** на телефоне
2. Перейдите: **Меню (☰) → Linked Services**
3. Найдите **"Home Assistant"** (может быть несколько!)
4. Удалите **ВСЕ** старые записи Home Assistant
5. В Home Assistant: перезагрузите интеграцию SmartThings

---

## 🔍 Диагностика

### Проверка Текущего Состояния

```bash
# Через SmartThings CLI
smartthings apps:installed:list

# Через API
curl -X GET "https://api.smartthings.com/v1/installedapps" \
  -H "Authorization: Bearer YOUR_PAT" | jq '.items[] | {id: .installedAppId, name: .displayName}'
```

### Проверка Лимитов

SmartThings имеет следующие лимиты:

| Ресурс | Лимит |
| ------ | ----- |
| Devices per Location | 300 |
| Subscriptions per InstalledApp | ~40 каждые 15 минут |
| Locations per Account | 10 |
| Rate Limit | HTTP 429 при превышении |

**Проверка через headers:**

```bash
curl -I "https://api.smartthings.com/v1/devices" \
  -H "Authorization: Bearer YOUR_PAT"

# Смотрите headers:
# X-RateLimit-Limit: 250
# X-RateLimit-Remaining: 245
# X-RateLimit-Reset: 1640000000
```

---

## 📋 Пошаговый План Исправления

### Для Вашей Системы (Рекомендуемый Подход)

**1. Установите SmartThings CLI (5 минут):**

```bash
npm install -g @smartthings/cli
smartthings login
```

**2. Найдите Старые InstalledApps (2 минуты):**

```bash
smartthings apps:installed:list
# Запишите ID всех "Home Assistant" приложений
```

**3. Удалите Старые (3 минуты):**

```bash
# Оставьте только ОДНО самое новое
# Удалите остальные:
smartthings apps:installed:delete <OLD_APP_ID_1>
smartthings apps:installed:delete <OLD_APP_ID_2>
```

**4. Проверьте в Home Assistant (1 минута):**

```bash
# Откройте HA
# Настройки → Устройства и Сервисы → SmartThings
# Нажмите "Reload" (перезагрузить интеграцию)
```

**5. Проверьте Устройства (2 минуты):**

```bash
# Все 27 устройств должны появиться!
# Если нет - добавьте интеграцию заново
```

---

## ⚠️ Важные Замечания

### Что НЕ Делать

- ❌ Не создавайте новые PAT без удаления старых InstalledApps
- ❌ Не удаляйте интеграцию в HA без очистки в SmartThings
- ❌ Не пытайтесь добавить >300 устройств в одну Location

### Best Practices

- ✅ Используйте **один** InstalledApp для Home Assistant
- ✅ Регулярно проверяйте список InstalledApps
- ✅ Используйте **capability subscriptions** вместо device subscriptions (если возможно)
- ✅ Настройте **внешний URL** для HA (не локальный IP)
- ✅ Используйте **HTTPS** для webhook URL

---

## 🔧 Автоматизация

### Скрипт для Очистки Старых InstalledApps

```bash
#!/bin/bash
# cleanup_smartthings.sh

echo "🔍 Поиск InstalledApps Home Assistant..."

# Получаем список всех InstalledApps
APPS=$(smartthings apps:installed:list --json | jq -r '.[] | select(.displayName == "Home Assistant") | .installedAppId')

# Подсчитываем количество
COUNT=$(echo "$APPS" | wc -l)

echo "Найдено: $COUNT приложений Home Assistant"

if [ "$COUNT" -gt 1 ]; then
    echo "⚠️  Обнаружено несколько приложений!"
    echo "Оставьте только самое новое, остальные удалите:"
    echo ""
    
    smartthings apps:installed:list | grep "Home Assistant"
    
    echo ""
    read -p "Введите ID приложений для удаления (через пробел): " IDS
    
    for ID in $IDS; do
        echo "🗑️  Удаляю $ID..."
        smartthings apps:installed:delete "$ID"
    done
    
    echo "✅ Очистка завершена!"
else
    echo "✅ Все в порядке, только одно приложение Home Assistant"
fi
```

**Использование:**

```bash
chmod +x cleanup_smartthings.sh
./cleanup_smartthings.sh
```

---

## 📞 Следующие Шаги

1. **Немедленно:**
   - Установите SmartThings CLI
   - Удалите старые InstalledApps

2. **После исправления:**
   - Перезагрузите интеграцию в HA
   - Проверьте все 27 устройств
   - Настройте автоматизации

3. **Профилактика:**
   - Раз в месяц проверяйте список InstalledApps
   - Используйте внешний URL для HA
   - Документируйте изменения

---

## 📚 Полезные Ссылки

- [SmartThings Developer Portal](https://developer.smartthings.com/)
- [SmartThings API Reference](https://developer.smartthings.com/docs/api/public)
- [SmartThings CLI Documentation](https://github.com/SmartThingsCommunity/smartthings-cli)
- [Personal Access Tokens](https://account.smartthings.com/tokens)
- [Rate Limits & Guardrails](https://developer.smartthings.com/docs/advanced/rate-limiting)

---

**Создано:** 2025-12-27  
**Для:** Home Assistant SmartThings Integration  
**Проблема:** `Reached limit of subscriptions`
