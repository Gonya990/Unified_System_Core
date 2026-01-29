#!/usr/bin/env python3
"""
OpenAI Profile Extractor | Извлекатель профиля OpenAI
English: Extract profile, custom instructions, and preferences from OpenAI
Russian: Извлечение профиля, пользовательских инструкций и настроек из OpenAI
"""

import json
from datetime import datetime
from pathlib import Path


# Colors
class Colors:
    RED = '\033[0;31m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    BLUE = '\033[0;34m'
    NC = '\033[0m'

def print_bilingual(english: str, russian: str, color: str = Colors.NC):
    """Print message in both English and Russian"""
    print(f"{color}English: {english}{Colors.NC}")
    print(f"{color}Russian: {russian}{Colors.NC}")

def extract_profile(data_dir: Path) -> dict:
    """Extract profile information from OpenAI export"""
    profile = {
        "extraction_date": datetime.now().isoformat(),
        "user_info": {},
        "preferences": {},
        "custom_instructions": {
            "about_user": "",
            "response_style": ""
        },
        "data_controls": {},
        "subscription": {}
    }

    # Look for user.json or account.json
    for filename in ['user.json', 'account.json', 'profile.json']:
        filepath = data_dir / filename
        if filepath.exists():
            print_bilingual(
                f"Found {filename}, extracting...",
                f"Найден {filename}, извлечение...",
                Colors.YELLOW
            )

            with open(filepath) as f:
                user_data = json.load(f)

            profile['user_info'] = {
                'email': user_data.get('email', 'N/A'),
                'name': user_data.get('name', 'N/A'),
                'created_at': user_data.get('created', 'N/A'),
                'id': user_data.get('id', 'N/A')
            }

            # Extract preferences if available
            if 'preferences' in user_data:
                profile['preferences'] = user_data['preferences']

            # Extract custom instructions if available
            if 'custom_instructions' in user_data:
                ci = user_data['custom_instructions']
                profile['custom_instructions'] = {
                    'about_user': ci.get('about_user_message', ''),
                    'response_style': ci.get('about_model_message', '')
                }

            break

    return profile

def create_agent_preferences(profile: dict, output_path: Path):
    """Create agent preferences file based on OpenAI profile"""

    agent_prefs = {
        "created_from": "openai_profile",
        "created_at": datetime.now().isoformat(),
        "user_context": {
            "name": profile['user_info'].get('name', 'User'),
            "background": profile['custom_instructions'].get('about_user', ''),
            "communication_preferences": profile['custom_instructions'].get('response_style', '')
        },
        "agent_behavior": {
            "tone": "professional and helpful",
            "verbosity": "balanced",
            "code_style": "clean and well-documented",
            "bilingual": True,
            "languages": ["en", "ru"]
        },
        "openai_sync": {
            "last_sync": datetime.now().isoformat(),
            "auto_sync": False,
            "sync_interval_days": 7
        }
    }

    # Map OpenAI preferences to agent preferences
    if profile.get('preferences'):
        prefs = profile['preferences']

        # Example mappings (adjust based on actual OpenAI preference structure)
        if 'theme' in prefs:
            agent_prefs['agent_behavior']['theme'] = prefs['theme']

        if 'language' in prefs:
            agent_prefs['agent_behavior']['primary_language'] = prefs['language']

    with open(output_path, 'w') as f:
        json.dump(agent_prefs, f, indent=2, ensure_ascii=False)

    return agent_prefs

def create_profile_markdown(profile: dict, output_path: Path):
    """Create markdown documentation of the extracted profile"""

    md = []
    md.append("# OpenAI Profile Information\n")
    md.append("# Информация профиля OpenAI\n\n")
    md.append(f"**Extracted | Извлечено:** {profile['extraction_date']}\n\n")
    md.append("---\n\n")

    # User Info
    md.append("## User Information | Информация о пользователе\n\n")
    for key, value in profile['user_info'].items():
        md.append(f"- **{key.title()}:** {value}\n")
    md.append("\n")

    # Custom Instructions
    md.append("## Custom Instructions | Пользовательские инструкции\n\n")
    md.append("### About User | О пользователе\n\n")
    md.append(f"{profile['custom_instructions'].get('about_user', 'Not set')}\n\n")
    md.append("### Response Style | Стиль ответов\n\n")
    md.append(f"{profile['custom_instructions'].get('response_style', 'Not set')}\n\n")

    # Preferences
    if profile.get('preferences'):
        md.append("## Preferences | Настройки\n\n")
        md.append("```json\n")
        md.append(json.dumps(profile['preferences'], indent=2, ensure_ascii=False))
        md.append("\n```\n\n")

    # Data Controls
    if profile.get('data_controls'):
        md.append("## Data Controls | Контроль данных\n\n")
        md.append("```json\n")
        md.append(json.dumps(profile['data_controls'], indent=2, ensure_ascii=False))
        md.append("\n```\n\n")

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(''.join(md))

def main():
    """Main extraction function"""
    print(f"{Colors.BLUE}{'='*70}{Colors.NC}")
    print(f"{Colors.BLUE}   OpenAI Profile Extractor{Colors.NC}")
    print(f"{Colors.BLUE}   Извлекатель профиля OpenAI{Colors.NC}")
    print(f"{Colors.BLUE}{'='*70}{Colors.NC}\n")

    # Directories
    script_dir = Path(__file__).parent
    data_dir = script_dir / "data" / "raw"
    output_dir = script_dir / "data" / "processed"

    output_dir.mkdir(parents=True, exist_ok=True)

    # Extract profile
    print_bilingual(
        "Extracting profile information...",
        "Извлечение информации профиля...",
        Colors.YELLOW
    )

    profile = extract_profile(data_dir)

    # Save raw profile
    profile_json_path = output_dir / "openai_profile.json"
    with open(profile_json_path, 'w') as f:
        json.dump(profile, f, indent=2, ensure_ascii=False)

    print_bilingual(
        f"✓ Saved raw profile to {profile_json_path}",
        f"✓ Сохранен исходный профиль в {profile_json_path}",
        Colors.GREEN
    )

    # Create agent preferences
    print_bilingual(
        "Creating agent preferences...",
        "Создание настроек агента...",
        Colors.YELLOW
    )

    agent_prefs_path = Path("/Users/macbook/Documents/Unified_System/Agent_Context/agent_preferences.json")
    create_agent_preferences(profile, agent_prefs_path)

    print_bilingual(
        f"✓ Created agent preferences at {agent_prefs_path}",
        f"✓ Созданы настройки агента в {agent_prefs_path}",
        Colors.GREEN
    )

    # Create markdown documentation
    print_bilingual(
        "Creating profile documentation...",
        "Создание документации профиля...",
        Colors.YELLOW
    )

    profile_md_path = output_dir / "OPENAI_PROFILE.md"
    create_profile_markdown(profile, profile_md_path)

    print_bilingual(
        f"✓ Created profile documentation at {profile_md_path}",
        f"✓ Создана документация профиля в {profile_md_path}",
        Colors.GREEN
    )

    # Summary
    print(f"\n{Colors.GREEN}{'='*70}{Colors.NC}")
    print_bilingual(
        "✓ Profile extraction complete!",
        "✓ Извлечение профиля завершено!",
        Colors.GREEN
    )
    print(f"{Colors.GREEN}{'='*70}{Colors.NC}\n")

    # Display custom instructions if available
    if profile['custom_instructions']['about_user']:
        print(f"{Colors.BLUE}Custom Instructions Found | Найдены пользовательские инструкции:{Colors.NC}\n")
        print(f"{Colors.YELLOW}About User:{Colors.NC}")
        print(profile['custom_instructions']['about_user'][:200] + "...\n")
        print(f"{Colors.YELLOW}Response Style:{Colors.NC}")
        print(profile['custom_instructions']['response_style'][:200] + "...\n")

if __name__ == '__main__':
    main()
