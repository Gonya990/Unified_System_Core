#!/usr/bin/env python3
"""
SmartThings InstalledApps Cleanup via REST API
Alternative to SmartThings CLI for cleaning up old Home Assistant integrations
"""

import sys

import requests

# Configuration
ST_API_BASE = "https://api.smartthings.com/v1"


def get_token():
    """Get Personal Access Token from user"""
    print("=" * 70)
    print("🏠 SmartThings InstalledApps Cleanup (REST API)")
    print("=" * 70)
    print()
    print("Для работы требуется Personal Access Token (PAT)")
    print("Получите его на: https://account.smartthings.com/tokens")
    print()
    print("Необходимые разрешения:")
    print("  ✅ r:installedapps")
    print("  ✅ w:installedapps")
    print("  ✅ r:devices:*")
    print()

    token = input("Введите ваш PAT: ").strip()
    return token


def api_request(method, endpoint, token, data=None):
    """Make API request to SmartThings"""
    url = f"{ST_API_BASE}/{endpoint}"
    headers = {"Authorization": f"Bearer {token}", "Accept": "application/json"}

    if method == "GET":
        response = requests.get(url, headers=headers)
    elif method == "DELETE":
        response = requests.delete(url, headers=headers)
    else:
        raise ValueError(f"Unsupported method: {method}")

    return response


def list_installed_apps(token):
    """List all installed apps"""
    print("\n🔍 Поиск InstalledApps...")

    response = api_request("GET", "installedapps", token)

    if response.status_code != 200:
        print(f"❌ Ошибка API: {response.status_code}")
        print(response.text)
        return []

    data = response.json()
    apps = data.get("items", [])

    print(f"Найдено приложений: {len(apps)}")
    return apps


def filter_ha_apps(apps):
    """Filter Home Assistant apps"""
    ha_apps = [app for app in apps if "Home Assistant" in app.get("displayName", "")]
    return ha_apps


def display_apps(apps):
    """Display apps in a table"""
    print("\n" + "=" * 70)
    print("Приложения Home Assistant:")
    print("=" * 70)

    for i, app in enumerate(apps, 1):
        app_id = app.get("installedAppId", "N/A")
        display_name = app.get("displayName", "N/A")
        status = app.get("installedAppStatus", "N/A")
        created = app.get("createdDate", "N/A")

        print(f"\n{i}. {display_name}")
        print(f"   ID: {app_id}")
        print(f"   Status: {status}")
        print(f"   Created: {created}")

    print("=" * 70)


def delete_app(app_id, token):
    """Delete an installed app"""
    print(f"\n🗑️  Удаляю {app_id}...")

    response = api_request("DELETE", f"installedapps/{app_id}", token)

    if response.status_code in [200, 204]:
        print("   ✅ Успешно удалено")
        return True
    else:
        print(f"   ❌ Ошибка: {response.status_code}")
        print(f"   {response.text}")
        return False


def main():
    try:
        # Get token
        token = get_token()

        # List all apps
        all_apps = list_installed_apps(token)

        if not all_apps:
            print("\n❌ Не удалось получить список приложений")
            return 1

        # Filter HA apps
        ha_apps = filter_ha_apps(all_apps)

        if not ha_apps:
            print("\n✅ Приложения Home Assistant не найдены")
            return 0

        print(f"\nНайдено приложений Home Assistant: {len(ha_apps)}")

        if len(ha_apps) == 1:
            print("\n✅ Найдено только одно приложение Home Assistant")
            print("Это нормально. Проблема может быть в другом.")
            return 0

        # Display apps
        display_apps(ha_apps)

        # Ask what to do
        print("\n⚠️  ВНИМАНИЕ: Найдено несколько приложений Home Assistant!")
        print("Рекомендация: Оставьте только ОДНО самое новое приложение")
        print()

        choice = input("Автоматически удалить старые приложения? (yes/no): ").strip().lower()

        if choice != "yes":
            print("\nРучное удаление:")
            print("  1. Выберите ID приложения для удаления из списка выше")
            print("  2. Используйте этот скрипт с опцией delete:")
            print(f"     python3 {sys.argv[0]} delete <APP_ID>")
            return 0

        # Sort by creation date (keep newest)
        sorted_apps = sorted(ha_apps, key=lambda x: x.get("createdDate", ""), reverse=True)
        apps_to_delete = sorted_apps[1:]  # All except newest

        print(f"\nБудут удалены {len(apps_to_delete)} приложений (оставлено самое новое)")

        confirm = input("Подтвердите удаление (yes/no): ").strip().lower()

        if confirm != "yes":
            print("Отменено пользователем")
            return 0

        # Delete old apps
        deleted = 0
        failed = 0

        for app in apps_to_delete:
            app_id = app.get("installedAppId")
            if delete_app(app_id, token):
                deleted += 1
            else:
                failed += 1

        # Summary
        print("\n" + "=" * 70)
        print("📊 РЕЗУЛЬТАТЫ")
        print("=" * 70)
        print(f"Удалено успешно: {deleted}")
        print(f"Ошибок: {failed}")

        if failed == 0:
            print("\n✅ Очистка завершена успешно!")
            print("\nСледующие шаги:")
            print("  1. Откройте Home Assistant")
            print("  2. Настройки → Устройства и Сервисы → SmartThings")
            print("  3. Нажмите 'Reload' (перезагрузить интеграцию)")
            print("  4. Проверьте, что все устройства доступны")
        else:
            print("\n⚠️  Некоторые приложения не удалось удалить")

        print("=" * 70)
        return 0

    except KeyboardInterrupt:
        print("\n\nОтменено пользователем")
        return 1
    except Exception as e:
        print(f"\n❌ КРИТИЧЕСКАЯ ОШИБКА: {e}")
        import traceback

        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
