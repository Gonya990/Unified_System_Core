#!/usr/bin/env python3
"""
Device Registration Form - Unified System

Стандартная форма для регистрации новых устройств в Tailscale сети.
"""

import json
import sys
from datetime import datetime
from pathlib import Path

# ANSI colors
CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
RESET = "\033[0m"
BOLD = "\033[1m"


def print_header():
    print(f"\n{CYAN}╔════════════════════════════════════════════════════════════════╗{RESET}")
    print(f"{CYAN}║{RESET}  {BOLD}Unified System - Device Registration Form{RESET}                  {CYAN}║{RESET}")
    print(f"{CYAN}╚════════════════════════════════════════════════════════════════╝{RESET}\n")


def get_input(prompt, required=True, default=None):
    """Get user input with validation"""
    while True:
        if default:
            value = input(f"{prompt} [{default}]: ").strip() or default
        else:
            value = input(f"{prompt}: ").strip()

        if value or not required:
            return value

        if required:
            print(f"{RED}⚠️  This field is required!{RESET}")


def get_choice(prompt, choices):
    """Get user choice from list"""
    print(f"\n{prompt}")
    for i, choice in enumerate(choices, 1):
        print(f"  {i}. {choice}")

    while True:
        try:
            choice_num = int(input(f"\nSelect (1-{len(choices)}): "))
            if 1 <= choice_num <= len(choices):
                return choices[choice_num - 1]
        except ValueError:
            pass
        print(f"{RED}Invalid choice!{RESET}")


def get_multiselect(prompt, options):
    """Get multiple selections from list"""
    print(f"\n{prompt}")
    print("(Enter numbers separated by commas, e.g., 1,3,5)")

    for i, option in enumerate(options, 1):
        print(f"  {i}. {option}")

    while True:
        try:
            selections = input("\nSelect: ").strip()
            if not selections:
                return []

            indices = [int(x.strip()) - 1 for x in selections.split(",")]
            selected = [options[i] for i in indices if 0 <= i < len(options)]

            if selected:
                return selected
        except (ValueError, IndexError):
            pass
        print(f"{RED}Invalid selection!{RESET}")


def register_device():
    """Main registration flow"""
    print_header()

    device = {}

    # Basic Information
    print(f"{BOLD}📋 Базовая Информация{RESET}")
    print("─" * 60)
    device["tailscale_ip"] = get_input("Tailscale IP (100.x.x.x)")
    device["hostname"] = get_input("Hostname", default="device-name")
    device["local_ip"] = get_input("Локальный IP (если есть)", required=False)

    # Owner Information
    print(f"\n{BOLD}👤 Информация о Владельце{RESET}")
    print("─" * 60)
    device["owner"] = {}
    device["owner"]["name"] = get_input("Имя владельца")
    device["owner"]["telegram_id"] = get_input("Telegram ID (цифры)")
    device["owner"]["telegram_username"] = get_input("Telegram username (@xxx)", required=False)

    # Role & Purpose
    print(f"\n{BOLD}🎭 Роль и Назначение{RESET}")
    print("─" * 60)

    roles = ["OWNER", "INFRASTRUCTURE_ADMIN", "ADMIN", "DEVELOPER", "MEMBER", "FAMILY", "GUEST"]
    device["role"] = get_choice("Выберите роль", roles)
    device["purpose"] = get_input("Назначение устройства (краткое описание)")

    # Project Access
    print(f"\n{BOLD}📁 Доступ к Проектам{RESET}")
    print("─" * 60)

    projects = [
        "global",
        "ai_core",
        "content_factory",
        "family_assistant",
        "automation",
        "knowledge_base",
        "infrastructure",
        "personal",
    ]
    device["projects_access"] = get_multiselect("Выберите проекты для доступа", projects)

    # Permissions
    print(f"\n{BOLD}🔐 Права Доступа{RESET}")
    print("─" * 60)

    device["permissions"] = {}
    if device["role"] in ["OWNER", "INFRASTRUCTURE_ADMIN"]:
        print(f"{GREEN}✅ Роль {device['role']} получает ВСЕ права автоматически{RESET}")
        device["permissions"] = "ALL"
    else:
        perms = ["read", "write", "execute", "delete", "admin", "share", "manage_users"]
        selected_perms = get_multiselect("Выберите разрешения", perms)

        for perm in perms:
            device["permissions"][perm] = perm in selected_perms

    # Hardware Specifications
    print(f"\n{BOLD}💻 Технические Характеристики{RESET}")
    print("─" * 60)

    device["hardware"] = {}
    hw_types = ["laptop", "phone", "server", "tablet", "desktop", "other"]
    device["hardware"]["type"] = get_choice("Тип устройства", hw_types)

    os_choices = ["macOS", "Windows", "Linux", "iOS", "Android", "other"]
    device["hardware"]["os"] = get_choice("Операционная система", os_choices)

    device["hardware"]["cpu"] = get_input("CPU", required=False)
    device["hardware"]["ram"] = get_input("RAM (GB)", required=False)
    device["hardware"]["storage"] = get_input("Storage (GB)", required=False)

    # Status & Notes
    print(f"\n{BOLD}📊 Статус{RESET}")
    print("─" * 60)

    statuses = ["online", "offline", "planned"]
    device["status"] = get_choice("Текущий статус", statuses)
    device["deployment_date"] = datetime.now().strftime("%Y-%m-%d")
    device["notes"] = get_input("Дополнительные примечания", required=False)

    return device


def save_registration(device):
    """Save device registration"""
    # Save to JSON
    output_dir = Path(__file__).parent.parent.parent / "Agent_Context/Infrastructure/Devices"
    output_dir.mkdir(parents=True, exist_ok=True)

    filename = f"device_{device['tailscale_ip'].replace('.', '_')}.json"
    output_file = output_dir / filename

    with open(output_file, "w") as f:
        json.dump(device, f, indent=2, ensure_ascii=False)

    print(f"\n{GREEN}✅ Регистрация сохранена: {output_file}{RESET}")

    # Update network map
    print(f"\n{YELLOW}📝 TODO: Обновите TAILSCALE_NETWORK_MAP.md с информацией об этом устройстве{RESET}")

    # RBAC setup
    print(f"\n{YELLOW}🔐 TODO: Запустите setup_network_rbac.py для применения прав доступа{RESET}")

    return output_file


def print_summary(device):
    """Print registration summary"""
    print(f"\n{CYAN}{'=' * 60}{RESET}")
    print(f"{BOLD}📋 Сводка Регистрации{RESET}")
    print(f"{CYAN}{'=' * 60}{RESET}\n")

    print(f"{BOLD}Устройство:{RESET} {device['hostname']} ({device['tailscale_ip']})")
    print(f"{BOLD}Владелец:{RESET} {device['owner']['name']} (ID: {device['owner']['telegram_id']})")
    print(f"{BOLD}Роль:{RESET} {device['role']}")
    print(f"{BOLD}Проекты:{RESET} {', '.join(device['projects_access']) if device['projects_access'] else 'Нет'}")
    print(f"{BOLD}Статус:{RESET} {device['status']}")
    print(f"{BOLD}Дата:{RESET} {device['deployment_date']}")

    if device.get("notes"):
        print(f"{BOLD}Примечания:{RESET} {device['notes']}")


def main():
    """Main execution"""
    try:
        device = register_device()
        print_summary(device)

        confirm = input(f"\n{YELLOW}Сохранить регистрацию? (y/N): {RESET}").strip().lower()

        if confirm == "y":
            output_file = save_registration(device)

            print(f"\n{GREEN}╔════════════════════════════════════════════════════════════════╗{RESET}")
            print(
                f"{GREEN}║{RESET}  {BOLD}✅ Устройство успешно зарегистрировано!{RESET}                      {GREEN}║{RESET}"
            )
            print(f"{GREEN}╚════════════════════════════════════════════════════════════════╝{RESET}\n")

            print(f"{BOLD}Следующие шаги:{RESET}")
            print(f"  1. Проверьте файл: {output_file}")
            print("  2. Обновите TAILSCALE_NETWORK_MAP.md")
            print("  3. Запустите: python Scripts/Orchestration/setup_network_rbac.py")
            print("  4. Проверьте права: /my_permissions в Telegram боте")
        else:
            print(f"\n{YELLOW}⏭️  Регистрация отменена{RESET}")

    except KeyboardInterrupt:
        print(f"\n\n{RED}❌ Регистрация прервана пользователем{RESET}")
        sys.exit(1)


if __name__ == "__main__":
    main()
