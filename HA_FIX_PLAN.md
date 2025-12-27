# 🔧 Home Assistant - План Полного Исправления

## 📊 Текущее Состояние Системы

**Статистика:**

- 🏠 Устройств: 128
- 📡 Объектов (Entities): 332  
- 🧩 Интеграций: 32 (встроенные + HACS)

**Критические Проблемы:**

1. ❌ **SmartThings** - 27 устройств недоступны (ошибка подписки)
2. ❌ **Bluetooth (hci0)** - сканер не работает
3. ❌ **Xiaomi Miot (Вася)** - робот-пылесос offline (192.168.1.142)
4. ⚠️ **LocalTuya** - ошибки выполнения
5. ⚠️ **IEC (Israel Electric)** - проблемы с API
6. ⚠️ **Yandex.Station** - сущности unavailable
7. ⚠️ **HACS** - заброшенный репозиторий HASS.Agent-MediaPlayer

---

## 🎯 План Исправления (Приоритет)

### ПРИОРИТЕТ 1: SmartThings (27 устройств)

**Проблема:** `Couldn't create a new subscription`

**Причина:**

- Webhook URL недоступен из интернета
- Истекший Personal Access Token (PAT)
- Корр уптированные данные интеграции

**Решение:**

#### Вариант A: Если есть Nabu Casa (Home Assistant Cloud)

```
1. Настройки → Home Assistant Cloud
2. Убедитесь, что подписка активна
3. Удалите интеграцию SmartThings
4. Добавьте заново (автоматически использует облачный webhook)
```

#### Вариант B: Без Nabu Casa (Ручная настройка)

```
1. Настройте внешний доступ:
   - Используйте DuckDNS + Let's Encrypt
   - Или Cloudflare Tunnel
   - Или Nginx Proxy Manager

2. В configuration.yaml добавьте:
   external_url: "https://ваш-домен.duckdns.org:8123"
   internal_url: "http://192.168.1.216:8123"

3. Создайте новый PAT:
   - Перейдите: https://account.smartthings.com/tokens
   - Create new token
   - Выберите все разрешения
   - Сохраните токен

4. Очистите старые данные:
   - Остановите HA
   - Удалите файл: /config/.storage/smartthings
   - Удалите запись из: /config/.storage/core.config_entries
   - Запустите HA

5. Добавьте интеграцию заново с новым PAT
```

---

### ПРИОРИТЕТ 2: Xiaomi Miot (Робот-пылесос Вася)

**Проблема:** Устройство недоступно по IP 192.168.1.142

**Решение:**

```
1. Найдите текущий IP пылесоса:
   - Откройте приложение Mi Home
   - Или проверьте в роутере (DHCP Leases)

2. Привяжите статический IP в роутере:
   - Найдите MAC-адрес пылесоса
   - В настройках роутера: DHCP → Static Lease
   - Привяжите MAC к 192.168.1.142

3. Перезагрузите пылесос (выкл/вкл)

4. В HA: Настройки → Устройства → Xiaomi Miot → Обновить IP
```

---

### ПРИОРИТЕТ 3: Bluetooth

**Проблема:** `Failed to force stop scanner`

**Решение:**

```
1. Проверьте адаптер:
   ssh root@smart
   hciconfig
   
2. Если адаптер не отвечает:
   sudo systemctl restart bluetooth
   sudo hciconfig hci0 down
   sudo hciconfig hci0 up

3. В HA configuration.yaml:
   bluetooth:
     adapter: hci0

4. Перезагрузите HA

5. Если не помогает - используйте внешний USB Bluetooth адаптер
```

---

### ПРИОРИТЕТ 4: Yandex.Station

**Проблема:** Сущности unavailable

**Решение:**

```
1. Откройте: http://192.168.1.216:8123/config/integrations

2. Найдите Yandex.Station → Настроить

3. Если просит авторизацию:
   - Отсканируйте QR-код приложением Яндекс
   - Или введите новые cookies

4. После авторизации все сущности должны стать available

5. Проверьте:
   Developer Tools → States → Найдите media_player.yandex_station
```

---

### ПРИОРИТЕТ 5: LocalTuya

**Проблема:** Exception in callback

**Решение:**

```
1. Обновите интеграцию:
   HACS → Интеграции → Local Tuya → Обновить

2. Проверьте логи для конкретных устройств:
   Настройки → Система → Логи → Фильтр: "localtuya"

3. Для каждого проблемного устройства:
   - Удалите из LocalTuya
   - Добавьте заново с правильными параметрами

4. Убедитесь, что Device ID и Local Key актуальны
```

---

### ПРИОРИТЕТ 6: IEC (Israel Electric Corporation)

**Проблема:** Ошибки API

**Решение:**

```
1. Проверьте статус сервиса IEC:
   https://www.iec.co.il/

2. Если сервис работает, обновите интеграцию:
   HACS → Интеграции → IEC → Обновить

3. Переавторизуйтесь:
   Настройки → Интеграции → IEC → Настроить
   Введите логин/пароль заново

4. Если не помогает - временно отключите интеграцию
```

---

### ПРИОРИТЕТ 7: Очистка HACS

**Проблема:** Заброшенный репозиторий HASS.Agent-MediaPlayer

**Решение:**

```
1. HACS → Интеграции
2. Найдите HASS.Agent-MediaPlayer
3. Удалите (три точки → Remove)
4. Перезагрузите HA
```

---

## 🚀 Автоматизация Исправлений

Создам скрипты для автоматического исправления некоторых проблем.

### Скрипт 1: Перезапуск Bluetooth

```bash
#!/bin/bash
# /config/scripts/fix_bluetooth.sh

echo "Restarting Bluetooth..."
systemctl restart bluetooth
sleep 2
hciconfig hci0 down
sleep 1
hciconfig hci0 up
echo "Bluetooth restarted"
```

### Скрипт 2: Проверка доступности устройств

```yaml
# automation.yaml
automation:
  - alias: "Check Vacuum Availability"
    trigger:
      platform: time_pattern
      minutes: "/30"
    action:
      - service: xiaomi_miot.call_action
        target:
          entity_id: vacuum.vasy
        data:
          method: get_properties
```

---

## 📋 Чек-лист Выполнения

### Немедленные действия

- [ ] Исправить SmartThings (Вариант A или B)
- [ ] Найти и привязать IP пылесоса
- [ ] Перезапустить Bluetooth
- [ ] Завершить авторизацию Yandex.Station

### Среднесрочные

- [ ] Обновить LocalTuya
- [ ] Проверить IEC API
- [ ] Удалить HASS.Agent-MediaPlayer

### Долгосрочные

- [ ] Настроить мониторинг доступности устройств
- [ ] Создать автоматизации для самовосстановления
- [ ] Документировать конфигурацию

---

## 🔍 Мониторинг После Исправления

После выполнения всех исправлений:

1. **Проверьте логи:**

   ```
   Настройки → Система → Логи
   Не должно быть ошибок
   ```

2. **Проверьте все устройства:**

   ```
   Настройки → Устройства
   Все 128 устройств должны быть available
   ```

3. **Проверьте автоматизации:**

   ```
   Настройки → Автоматизации
   Протестируйте каждую
   ```

---

## 📞 Следующие Шаги

Начнем с ПРИОРИТЕТ 1 (SmartThings)?
Или хотите, чтобы я автоматически исправил все, что возможно через браузер?
