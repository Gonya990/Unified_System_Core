#!/usr/bin/env python3
"""
Быстрая диагностика Home Assistant через REST API
"""

from collections import Counter

import requests

# HA Configuration
HA_URL = "http://100.81.133.25:8123"
HA_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJhYWQ3YjJiN2M4NDg0NWEzODA0YTU4MWUwYWYyNjk3MyIsImlhdCI6MTc2Njg0NTEyNywiZXhwIjoyMDgyMjA1MTI3fQ.H4iTu7T_IYaom9ecHVA5EVBJ-cFBXyFXwkgykPdDcjc"

headers = {"Authorization": f"Bearer {HA_TOKEN}", "Content-Type": "application/json"}


def api_get(endpoint):
    """Make GET request to HA API"""
    url = f"{HA_URL}/api/{endpoint}"
    r = requests.get(url, headers=headers, timeout=10)
    r.raise_for_status()
    return r.json()


def api_post(endpoint, data=None):
    """Make POST request to HA API"""
    url = f"{HA_URL}/api/{endpoint}"
    r = requests.post(url, headers=headers, json=data or {}, timeout=10)
    r.raise_for_status()
    return r.json()


print("=" * 70)
print("🏠 HOME ASSISTANT - БЫСТРАЯ ДИАГНОСТИКА")
print("=" * 70)

# 1. Общая информация
print("\n📊 ОБЩАЯ ИНФОРМАЦИЯ:")
config = api_get("config")
print(f"  Версия: {config.get('version')}")
print(f"  Локация: {config.get('location_name')}")
print(f"  Часовой пояс: {config.get('time_zone')}")

# 2. Статистика сущностей
print("\n📈 СТАТИСТИКА СУЩНОСТЕЙ:")
states = api_get("states")
print(f"  Всего сущностей: {len(states)}")

# Подсчет по доменам
domains = Counter(s["entity_id"].split(".")[0] for s in states if "." in s["entity_id"])
print("\n  Топ-10 доменов:")
for domain, count in domains.most_common(10):
    print(f"    {domain}: {count}")

# 3. Недоступные сущности
unavailable = [s for s in states if s.get("state") == "unavailable"]
print(f"\n❌ НЕДОСТУПНЫЕ СУЩНОСТИ: {len(unavailable)}")
if unavailable:
    # Группируем по доменам
    unavail_domains = Counter(s["entity_id"].split(".")[0] for s in unavailable if "." in s["entity_id"])
    print("  По доменам:")
    for domain, count in unavail_domains.most_common():
        print(f"    {domain}: {count}")

    print("\n  Первые 15 недоступных:")
    for s in unavailable[:15]:
        name = s.get("attributes", {}).get("friendly_name", s["entity_id"])
        print(f"    - {s['entity_id']} ({name})")

# 4. Проблемные интеграции (по unavailable сущностям)
print("\n🔍 АНАЛИЗ ПРОБЛЕМ:")

problem_integrations = {
    "smartthings": 0,
    "bluetooth": 0,
    "xiaomi_miot": 0,
    "yandex_station": 0,
    "localtuya": 0,
    "tuya": 0,
}

for s in unavailable:
    entity_id = s["entity_id"]
    for integration in problem_integrations.keys():
        if integration in entity_id or entity_id.split(".")[0] in ["light", "switch", "sensor", "binary_sensor"]:
            # Проверяем через атрибуты
            attrs = s.get("attributes", {})
            if "integration" in attrs and attrs["integration"] == integration:
                problem_integrations[integration] += 1

# Выводим только проблемные
print("  Интеграции с недоступными устройствами:")
for integration, count in problem_integrations.items():
    if count > 0:
        print(f"    ❌ {integration}: {count} недоступных")

# 5. Сервисы
print("\n🔧 ДОСТУПНЫЕ СЕРВИСЫ:")
services = api_get("services")
print(f"  Всего доменов с сервисами: {len(services)}")

# Проверяем ключевые сервисы
key_services = ["homeassistant", "light", "switch", "automation", "script"]
for domain in key_services:
    if domain in services:
        service_count = len(services[domain])
        print(f"    ✅ {domain}: {service_count} сервисов")

# 6. Рекомендации
print("\n💡 РЕКОМЕНДАЦИИ:")

if unavail_domains.get("light", 0) > 5 or unavail_domains.get("switch", 0) > 5:
    print("  ⚠️  Много недоступных света/выключателей")
    print("     → Проверьте SmartThings и LocalTuya")

if unavail_domains.get("sensor", 0) > 10:
    print("  ⚠️  Много недоступных сенсоров")
    print("     → Проверьте Xiaomi Miot и Bluetooth")

if unavail_domains.get("media_player", 0) > 0:
    print("  ⚠️  Недоступные медиа-плееры")
    print("     → Проверьте Yandex.Station")

print("\n" + "=" * 70)
print("✅ ДИАГНОСТИКА ЗАВЕРШЕНА")
print("=" * 70)
print("\nДля исправления проблем:")
print("  1. SmartThings: Очистите подписки на https://smartthings.developer.samsung.com/")
print("  2. Bluetooth: Добавьте DBus в Docker (см. HA_FIX_PLAN.md)")
print("  3. Xiaomi: Проверьте IP-адреса устройств в роутере")
print("  4. Yandex.Station: Отсканируйте QR-код для авторизации")
