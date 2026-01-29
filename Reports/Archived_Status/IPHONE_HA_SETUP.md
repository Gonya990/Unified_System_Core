# 📱 iPhone Home Assistant App - Включение Фонового Обновления

## 🎯 Проблема

**Недоступные сенсоры:** 9 сенсоров iPhone (Igor) показывают статус `unavailable`

**Список недоступных:**

- Connection Type
- Storage
- SSID
- BSSID
- SIM 1
- SIM 2
- Last Update Trigger
- Audio Output
- Geocoded Location

**Причина:** Приложение Home Assistant Companion на iPhone не обновляет данные
в фоновом режиме.

---

## ✅ Решение: Включение Фонового Обновления

### Шаг 1: Настройки iOS

1. **Откройте Настройки iPhone**
2. **Прокрутите вниз** и найдите **"Home Assistant"**
3. **Нажмите на приложение**

### Шаг 2: Обновление Контента

1. **Найдите "Обновление контента"** (Background App Refresh)
2. **Включите переключатель** (должен стать зеленым)

### Шаг 3: Разрешения Локации

1. **Нажмите "Локация"** (Location)
2. **Выберите "Всегда"** (Always)
   - Это необходимо для сенсоров SSID, BSSID, Geocoded Location

### Шаг 4: Уведомления

1. **Вернитесь назад** и нажмите **"Уведомления"** (Notifications)
2. **Включите "Разрешить уведомления"**
   - Это позволит HA отправлять обновления даже когда приложение закрыто

### Шаг 5: Настройки в Приложении HA

1. **Откройте приложение Home Assistant**
2. **Нажмите на иконку профиля** (внизу справа)
3. **Настройки → Companion App**
4. **Sensors → Enable All** (включить все сенсоры)
5. **Нажмите "Update Sensors"** (обновить сенсоры)

---

## 🔋 Оптимизация Батареи

### Важно! Режим Энергосбережения

Если включен **Режим энергосбережения** (Low Power Mode):

- Фоновое обновление **автоматически отключается**
- Сенсоры перестают обновляться

**Решение:**

1. Настройки → Аккумулятор
2. Отключите "Режим энергосбережения"
3. Или создайте автоматизацию в Shortcuts для включения HA при зарядке

---

## 📊 Проверка Работы

### После Настройки

1. **Откройте приложение HA**
2. **Настройки → Companion App → Sensors**
3. **Проверьте статус каждого сенсора:**
   - ✅ Зеленая галочка = работает
   - ❌ Красный крестик = отключен

4. **Нажмите "Update Sensors"**
5. **Подождите 1-2 минуты**

### Проверка в Home Assistant

1. Откройте HA Web: <http://192.168.1.216:8123>
2. Developer Tools → States
3. Найдите сенсоры iPhone:

   ```text
   sensor.iphone_igor_connection_type
   sensor.iphone_igor_storage
   sensor.iphone_igor_ssid
   sensor.iphone_igor_bssid
   sensor.iphone_igor_sim_1
   sensor.iphone_igor_sim_2
   sensor.iphone_igor_last_update_trigger
   sensor.iphone_igor_audio_output
   sensor.iphone_igor_geocoded_location
   ```

4. Все должны показывать актуальные значения (не `unavailable`)

---

## 🔧 Расширенная Настройка

### Частота Обновления

По умолчанию HA Companion обновляет сенсоры:

- **При изменении локации** (геозоны)
- **При изменении WiFi сети**
- **Каждые 15 минут** (в фоне)
- **При открытии приложения**

### Увеличение Частоты (опционально)

1. **Настройки → Companion App**
2. **Location → Zone Based Tracking**
3. **Уменьшите "Zone Radius"** для более частых обновлений
4. **Включите "Significant Location Changes"**

### Принудительное Обновление

Создайте автоматизацию в HA:

```yaml
automation:
  - alias: "Update iPhone Sensors Every 10 Minutes"
    trigger:
      - platform: time_pattern
        minutes: "/10"
    action:
      - service: notify.mobile_app_iphone_igor
        data:
          message: "command_update_sensors"
```

---

## ⚠️ Troubleshooting

### Сенсоры Все Еще Unavailable?

**1. Перезапустите приложение:**

- Закройте приложение полностью (свайп вверх в App Switcher)
- Откройте заново
- Нажмите "Update Sensors"

**2. Переавторизуйтесь:**

- Настройки → Companion App
- Logout
- Login заново с вашим HA сервером

**3. Переустановите приложение:**

- Удалите приложение HA
- Установите заново из App Store
- Настройте подключение к серверу

**4. Проверьте подключение:**

- Убедитесь, что iPhone в той же сети, что и HA
- Или настроен внешний доступ (Nabu Casa / DuckDNS)

### Некоторые Сенсоры Не Работают?

**Connection Type / SSID / BSSID:**

- Требуют разрешение "Локация: Всегда"
- Проверьте в Настройки → Home Assistant → Локация

**SIM 1 / SIM 2:**

- Работают только на iPhone с двумя SIM-картами
- Если у вас одна SIM, эти сенсоры будут `unavailable`

**Geocoded Location:**

- Требует активный интернет
- Использует обратное геокодирование (координаты → адрес)

---

## 📋 Чек-лист Настройки

- [ ] Настройки iOS → Home Assistant → Обновление контента: **ВКЛ**
- [ ] Настройки iOS → Home Assistant → Локация: **Всегда**
- [ ] Настройки iOS → Home Assistant → Уведомления: **ВКЛ**
- [ ] Режим энергосбережения: **ВЫКЛ** (или настроена автоматизация)
- [ ] HA App → Sensors → Enable All: **ВКЛ**
- [ ] HA App → Update Sensors: **Выполнено**
- [ ] HA Web → Developer Tools → States: **Проверено**

---

## 🎯 Ожидаемый Результат

После выполнения всех шагов:

- ✅ Все 9 сенсоров iPhone должны показывать актуальные данные
- ✅ Сенсоры обновляются автоматически каждые 15 минут
- ✅ Сенсоры обновляются при изменении локации/WiFi
- ✅ Можно использовать в автоматизациях HA

---

## 📱 Дополнительные Возможности

### Полезные Сенсоры iPhone

- **Battery Level** - уровень заряда
- **Battery State** - состояние зарядки
- **Activity** - текущая активность (ходьба, вождение, и т.д.)
- **Steps** - количество шагов (из Health)
- **Distance** - пройденное расстояние
- **Floors Climbed** - пройденные этажи

### Интеграция с Автоматизациями

#### Пример 1: Включить свет при возвращении домой

```yaml
automation:
  - alias: "Welcome Home"
    trigger:
      - platform: state
        entity_id: device_tracker.iphone_igor
        to: "home"
    action:
      - service: light.turn_on
        target:
          entity_id: light.entrance
```

#### Пример 2: Уведомление о низком заряде

```yaml
automation:
  - alias: "Low Battery Alert"
    trigger:
      - platform: numeric_state
        entity_id: sensor.iphone_igor_battery_level
        below: 20
    action:
      - service: notify.telegram
        data:
          message: >-
            ⚠️ iPhone заряд: {{ states('sensor.iphone_igor_battery_level') }}%
```

---

**Создано:** 2025-12-27  
**Для:** iPhone (Igor) Home Assistant Companion App  
**Проблема:** 9 unavailable sensors
