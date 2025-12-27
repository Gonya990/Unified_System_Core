#!/usr/bin/env python3
"""
Автоматическое исправление проблем с интеграциями Home Assistant
Использует REST API для диагностики и исправления
"""

import sys
import json
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

from ha_client import HomeAssistantClient

def print_section(title):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}\n")

def check_integration_status(client):
    """Проверка статуса всех интеграций"""
    print_section("📊 СТАТУС ИНТЕГРАЦИЙ")
    
    integrations = client.get_integrations()
    
    failed = []
    working = []
    
    for integration in integrations:
        domain = integration.get('domain', 'unknown')
        title = integration.get('title', 'Unknown')
        state = integration.get('state', 'unknown')
        entry_id = integration.get('entry_id', '')
        
        if state == 'loaded':
            working.append(f"✅ {domain}: {title}")
        else:
            failed.append({
                'domain': domain,
                'title': title,
                'state': state,
                'entry_id': entry_id
            })
            print(f"❌ {domain}: {title} - {state}")
    
    print(f"\n✅ Работают: {len(working)}")
    print(f"❌ Проблемы: {len(failed)}")
    
    return failed, working

def reload_failed_integrations(client, failed):
    """Попытка перезагрузить проблемные интеграции"""
    print_section("🔄 ПЕРЕЗАГРУЗКА ПРОБЛЕМНЫХ ИНТЕГРАЦИЙ")
    
    for integration in failed:
        domain = integration['domain']
        title = integration['title']
        entry_id = integration['entry_id']
        
        # Пропускаем интеграции, которые требуют ручной настройки
        skip_domains = ['smartthings', 'bluetooth']  # SmartThings требует очистки подписок
        
        if domain in skip_domains:
            print(f"⏭️  Пропускаем {domain} - требуется ручная настройка")
            continue
        
        try:
            print(f"🔄 Перезагружаем {domain} ({title})...")
            result = client.reload_integration(entry_id)
            print(f"   ✅ Успешно: {result}")
        except Exception as e:
            print(f"   ❌ Ошибка: {e}")

def check_bluetooth_config(client):
    """Проверка конфигурации Bluetooth"""
    print_section("🔵 ДИАГНОСТИКА BLUETOOTH")
    
    # Получаем состояние Bluetooth интеграции
    integrations = client.get_integrations()
    bt_integration = next((i for i in integrations if i.get('domain') == 'bluetooth'), None)
    
    if not bt_integration:
        print("❌ Bluetooth интеграция не найдена")
        return
    
    print(f"Статус: {bt_integration.get('state', 'unknown')}")
    print(f"Entry ID: {bt_integration.get('entry_id', 'N/A')}")
    
    print("\n📝 РЕШЕНИЕ:")
    print("Bluetooth требует доступа к DBus хоста.")
    print("Если HA в Docker, добавьте в docker-compose.yaml:")
    print("""
volumes:
  - /run/dbus:/run/dbus:ro
network_mode: host
    """)

def check_smartthings_config(client):
    """Проверка конфигурации SmartThings"""
    print_section("📱 ДИАГНОСТИКА SMARTTHINGS")
    
    integrations = client.get_integrations()
    st_integration = next((i for i in integrations if i.get('domain') == 'smartthings'), None)
    
    if not st_integration:
        print("❌ SmartThings интеграция не найдена")
        return
    
    print(f"Статус: {st_integration.get('state', 'unknown')}")
    print(f"Entry ID: {st_integration.get('entry_id', 'N/A')}")
    
    print("\n📝 РЕШЕНИЕ:")
    print("Ошибка 'Reached limit of subscriptions' означает:")
    print("1. Перейдите: https://smartthings.developer.samsung.com/")
    print("2. Удалите старые неиспользуемые подписки (webhooks)")
    print("3. Или создайте новый Personal Access Token")
    print("4. Удалите и добавьте интеграцию заново в HA")

def get_entity_counts(client):
    """Подсчет сущностей по доменам"""
    print_section("📈 СТАТИСТИКА СУЩНОСТЕЙ")
    
    states = client.get_states()
    
    domains = {}
    unavailable = []
    
    for state in states:
        entity_id = state.get('entity_id', '')
        domain = entity_id.split('.')[0] if '.' in entity_id else 'unknown'
        state_value = state.get('state', '')
        
        domains[domain] = domains.get(domain, 0) + 1
        
        if state_value == 'unavailable':
            unavailable.append(entity_id)
    
    # Топ-10 доменов
    sorted_domains = sorted(domains.items(), key=lambda x: x[1], reverse=True)
    
    print("Топ-10 доменов по количеству сущностей:")
    for domain, count in sorted_domains[:10]:
        print(f"  {domain}: {count}")
    
    print(f"\n❌ Недоступных сущностей: {len(unavailable)}")
    if unavailable:
        print("Первые 10:")
        for entity in unavailable[:10]:
            print(f"  - {entity}")

def main():
    print("🏠 Home Assistant - Автоматическая диагностика и исправление")
    print("=" * 60)
    
    try:
        client = HomeAssistantClient()
        
        # Проверка подключения
        print("🔌 Проверка подключения к Home Assistant...")
        health = client.check_health()
        
        if not health.get('healthy'):
            print(f"❌ Не удалось подключиться: {health.get('error')}")
            return 1
        
        print(f"✅ Подключено к HA {health.get('version')}")
        print(f"📍 Локация: {health.get('location_name')}")
        print(f"📊 Сущностей: {health.get('entities_count')}")
        
        # Проверка интеграций
        failed, working = check_integration_status(client)
        
        # Статистика сущностей
        get_entity_counts(client)
        
        # Специфичные проверки
        check_bluetooth_config(client)
        check_smartthings_config(client)
        
        # Попытка исправления
        if failed:
            print("\n" + "=" * 60)
            response = input("Попытаться автоматически исправить? (y/n): ")
            if response.lower() == 'y':
                reload_failed_integrations(client, failed)
        
        print_section("✅ ДИАГНОСТИКА ЗАВЕРШЕНА")
        print("Проверьте рекомендации выше для ручного исправления.")
        
        return 0
        
    except Exception as e:
        print(f"\n❌ КРИТИЧЕСКАЯ ОШИБКА: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == '__main__':
    sys.exit(main())
