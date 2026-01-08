# 🔵 Исправление Bluetooth в Home Assistant (Docker)

## 🎯 Проблема

В логах Home Assistant наблюдается циклическая ошибка:
`Failed to force stop scanner: 'NoneType' object has no attribute 'send'`

**Причина:** Контейнер Home Assistant не имеет доступа к системной шине D-Bus хоста, которая необходима для взаимодействия с Bluetooth-адаптером `hci0`.

---

## ✅ Решение

Чтобы Bluetooth заработал, нужно перенастроить запуск контейнера Home Assistant.

### Шаг 1: Подключение к хосту

Подключитесь к серверу `smart` (IP `192.168.1.216`):

```bash
ssh root@192.168.1.216
```

### Шаг 2: Модификация docker-compose.yml

Найдите файл, которым запускается HA. Обычно это `/home/root/homeassistant/docker-compose.yml` или похожий путь.

Добавьте следующие параметры в секцию `services → homeassistant`:

```yaml
services:
  homeassistant:
    # ... другие параметры ...
    volumes:
      - /config:/config
      - /run/dbus:/run/dbus:ro  # 💡 ВАЖНО: Проброс DBus
      - /etc/localtime:/etc/localtime:ro
    network_mode: host          # 💡 ВАЖНО: Должен быть host mode
    privileged: true            # 💡 РЕКОМЕНДУЕТСЯ для прямого доступа к железу
    # ...
```

### Шаг 3: Перезапуск контейнера

В папке с `docker-compose.yml` выполните:

```bash
docker compose up -d
```

### Шаг 4: Проверка на стороне HA

1. Зайдите в **Settings → System → Logs**.
2. Ошибка `Failed to force stop scanner` должна исчезнуть.
3. Перейдите в **Settings → Devices & Services**.
4. Найдите интеграцию **Bluetooth**. Она должна показывать статус `Loaded`.

---

## 🛠️ Если Bluetooth все еще не работает

### 1. Проверьте статус службы на хосте

Выполните на сервере `smart`:

```bash
systemctl status bluetooth
```

Если она `inactive`, включите:

```bash
systemctl enable --now bluetooth
```

### 2. Прямая проверка адаптера

```bash
hciconfig -a
```

Если адаптер `DOWN`, поднимите его:

```bash
hciconfig hci0 up
```

### 3. Установка BlueZ (если отсутствует)

```bash
dnf install bluez  # Для Fedora (ваш хост)
```

---

## 📋 Почему это важно?

Без доступа к Bluetooth Home Assistant не сможет:

- Отслеживать iPhone через `device_tracker` по Bluetooth.
- Управлять умными замками, датчиками температуры и другими BLE устройствами.
- Быстро обнаруживать новые устройства в доме.

---
**Инструкция создана:** 2025-12-27  
**Для хоста:** smart (192.168.1.216), Fedora 41  
