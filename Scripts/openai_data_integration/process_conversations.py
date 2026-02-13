#!/usr/bin/env python3
"""
OpenAI Conversations Processor | Обработчик разговоров OpenAI
English: Process exported ChatGPT conversations.json into structured markdown
Russian: Обработка экспортированных разговоров ChatGPT conversations.json в структурированный markdown
"""

import json
import re
import sys
from datetime import datetime
from pathlib import Path


# Colors for terminal output
class Colors:
    RED = "\033[0;31m"
    GREEN = "\033[0;32m"
    YELLOW = "\033[1;33m"
    BLUE = "\033[0;34m"
    NC = "\033[0m"  # No Color


def print_bilingual(english: str, russian: str, color: str = Colors.NC):
    """Print message in both English and Russian"""
    print(f"{color}English: {english}{Colors.NC}")
    print(f"{color}Russian: {russian}{Colors.NC}")


def load_config() -> dict:
    """Load configuration file"""
    script_dir = Path(__file__).parent
    config_path = script_dir / "config.json"

    with open(config_path) as f:
        return json.load(f)


def parse_conversation(conv: dict) -> dict:
    """Parse a single conversation into structured format"""
    messages = []

    # Extract title
    title = conv.get("title", "Untitled Conversation")

    # Check for scraper format (simplified)
    if "messages" in conv and isinstance(conv.get("messages"), list):
        # Scraper format
        for msg in conv["messages"]:
            role = msg.get("role", "unknown")
            content = msg.get("content", "")
            if content:
                messages.append({"role": role, "content": content, "timestamp": None})

        # Date is unknown for scraped data, use generic fallback or extract from title if possible?
        # For now, default to None/Unknown
        date_str = "Unknown_Date"
        time_str = "00:00:00"

        return {
            "title": title,
            "date": date_str,
            "time": time_str,
            "messages": messages,
            "id": conv.get("conversation_id", "unknown"),
        }

    # Extract creation time
    create_time = conv.get("create_time")
    if create_time:
        dt = datetime.fromtimestamp(create_time)
        date_str = dt.strftime("%Y-%m-%d")
        time_str = dt.strftime("%H:%M:%S")
    else:
        date_str = "Unknown"
        time_str = "Unknown"

    # Extract messages (official export format)
    mapping = conv.get("mapping", {})

    # Build conversation tree
    for _node_id, node in mapping.items():
        message = node.get("message")
        if not message:
            continue

        author = message.get("author", {}).get("role", "unknown")
        content = message.get("content", {})

        # Extract text content
        parts = content.get("parts", [])
        text = "\n".join(str(part) for part in parts if part)

        if text:
            messages.append({"role": author, "content": text, "timestamp": message.get("create_time")})

    return {"title": title, "date": date_str, "time": time_str, "messages": messages, "id": conv.get("id", "unknown")}


def conversation_to_markdown(conv_data: dict, include_timestamps: bool = True) -> str:
    """Convert conversation data to markdown format"""
    md = []

    # Header
    md.append(f"# {conv_data['title']}\n")
    md.append(f"**Date | Дата:** {conv_data['date']} {conv_data['time']}\n")
    md.append(f"**ID:** {conv_data['id']}\n")
    md.append("---\n")

    # Messages
    for msg in conv_data["messages"]:
        role = msg["role"].upper()
        role_label = {
            "USER": "**👤 User | Пользователь:**",
            "ASSISTANT": "**🤖 Assistant | Ассистент:**",
            "SYSTEM": "**⚙️ System | Система:**",
        }.get(role, f"**{role}:**")

        md.append(f"{role_label}\n")
        md.append(f"{msg['content']}\n\n")

        if include_timestamps and msg.get("timestamp"):
            dt = datetime.fromtimestamp(msg["timestamp"])
            md.append(f"*{dt.strftime('%Y-%m-%d %H:%M:%S')}*\n\n")

    return "\n".join(md)


def create_index(conversations: list[dict], output_dir: Path) -> str:
    """Create an index file for all conversations"""
    md = ["# OpenAI ChatGPT Conversations Index\n"]
    md.append("# Индекс разговоров OpenAI ChatGPT\n\n")
    md.append(f"**Total Conversations | Всего разговоров:** {len(conversations)}\n\n")
    md.append("---\n\n")

    # Group by date
    by_date = {}
    for conv in conversations:
        date = conv["date"]
        if date not in by_date:
            by_date[date] = []
        by_date[date].append(conv)

    # Sort by date descending
    for date in sorted(by_date.keys(), reverse=True):
        md.append(f"## {date}\n\n")
        for conv in by_date[date]:
            filename = f"{conv['date']}_{sanitize_filename(conv['title'])}.md"
            md.append(f"- [{conv['title']}]({filename}) - {conv['time']}\n")
        md.append("\n")

    return "\n".join(md)


def sanitize_filename(filename: str) -> str:
    """Sanitize filename for filesystem compatibility"""
    # Remove invalid characters
    sanitized = re.sub(r'[<>:"/\\|?*]', "", filename)
    # Replace spaces with underscores
    sanitized = sanitized.replace(" ", "_")
    # Limit length
    return sanitized[:100]


def main():
    """Main processing function"""
    print(f"{Colors.BLUE}{'=' * 70}{Colors.NC}")
    print(f"{Colors.BLUE}   OpenAI Conversations Processor{Colors.NC}")
    print(f"{Colors.BLUE}   Обработчик разговоров OpenAI{Colors.NC}")
    print(f"{Colors.BLUE}{'=' * 70}{Colors.NC}\n")

    # Check arguments
    if len(sys.argv) < 2:
        print_bilingual(
            "Usage: process_conversations.py <conversations.json>",
            "Использование: process_conversations.py <conversations.json>",
            Colors.RED,
        )
        sys.exit(1)

    input_file = Path(sys.argv[1])

    if not input_file.exists():
        print_bilingual(f"File not found: {input_file}", f"Файл не найден: {input_file}", Colors.RED)
        sys.exit(1)

    # Load config
    print_bilingual("Loading configuration...", "Загрузка конфигурации...", Colors.YELLOW)
    config = load_config()

    output_dir = Path(config["processing"]["output_dir"])
    output_dir.mkdir(parents=True, exist_ok=True)

    # Load conversations
    print_bilingual(
        f"Loading conversations from {input_file}...", f"Загрузка разговоров из {input_file}...", Colors.YELLOW
    )

    with open(input_file, encoding="utf-8") as f:
        data = json.load(f)

    conversations = data if isinstance(data, list) else [data]

    print_bilingual(
        f"Found {len(conversations)} conversations", f"Найдено {len(conversations)} разговоров", Colors.GREEN
    )

    # Process each conversation
    processed = []
    for i, conv in enumerate(conversations, 1):
        print(f"\r{Colors.YELLOW}Processing | Обработка: {i}/{len(conversations)}{Colors.NC}", end="")

        conv_data = parse_conversation(conv)
        processed.append(conv_data)

        # Save to markdown
        md_content = conversation_to_markdown(conv_data, include_timestamps=config["processing"]["include_timestamps"])

        filename = f"{conv_data['date']}_{sanitize_filename(conv_data['title'])}.md"
        output_path = output_dir / filename

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(md_content)

    print()  # New line after progress

    # Create index
    if config["integration"]["create_index"]:
        print_bilingual("Creating index...", "Создание индекса...", Colors.YELLOW)
        index_content = create_index(processed, output_dir)
        index_path = output_dir / "INDEX.md"

        with open(index_path, "w", encoding="utf-8") as f:
            f.write(index_content)

        print_bilingual(f"Index saved to {index_path}", f"Индекс сохранен в {index_path}", Colors.GREEN)

    # Summary
    print(f"\n{Colors.GREEN}{'=' * 70}{Colors.NC}")
    print_bilingual(
        f"✓ Successfully processed {len(processed)} conversations",
        f"✓ Успешно обработано {len(processed)} разговоров",
        Colors.GREEN,
    )
    print_bilingual(f"Output directory: {output_dir}", f"Выходная директория: {output_dir}", Colors.GREEN)
    print(f"{Colors.GREEN}{'=' * 70}{Colors.NC}\n")

    print_bilingual(
        "Next step: Run ./integrate_to_workspace.sh",
        "Следующий шаг: Запустите ./integrate_to_workspace.sh",
        Colors.BLUE,
    )


if __name__ == "__main__":
    main()
