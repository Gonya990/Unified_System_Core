#!/usr/bin/env python3
"""
Bot Commands Test Report
Checks all handlers and quick buttons
"""
import re

BOT_FILE = "/home/gonya/Unified_System_Core/Projects/AI_Core/src/ai_telegram_bot_v2.py"

print("🤖 TELEGRAM BOT - COMMAND & HANDLER CHECK")
print("=" * 60)

with open(BOT_FILE) as f:
    content = f.read()

# 1. Check registered commands
print("\n✅ REGISTERED COMMANDS:")
commands_block = re.search(r'commands_to_register = \{(.+?)\}', content, re.DOTALL)
if commands_block:
    commands = re.findall(r'"(\w+)":\s*(\w+)', commands_block.group(1))
    for cmd, handler in commands:
        print(f"  /{cmd:<15} → {handler}")

# 2. Check message handlers
print("\n✅ MESSAGE HANDLERS:")
handlers = [
    ("PHOTO", "handle_photo"),
    ("VOICE", "handle_voice"),
    ("AUDIO", "handle_audio"),
    ("VIDEO", "handle_video"),
    ("DOCUMENT", "handle_document"),
]

for filter_type, handler in handlers:
    if f"filters.{filter_type}" in content and handler in content:
        status = "✅ OK"
    elif handler in content:
        status = "⚠️  Function exists, check registration"
    else:
        status = "❌ MISSING"
    print(f"  {filter_type:<12} → {handler:<20} {status}")

# 3. Check quick buttons
print("\n✅ QUICK BUTTONS (InlineKeyboard):")
button_patterns = [
    r'InlineKeyboardButton\(.*?"(.*?)".*?\)',
    r'KeyboardButton\("(.*?)"\)',
]

buttons = set()
for pattern in button_patterns:
    matches = re.findall(pattern, content)
    buttons.update(matches)

for button in sorted(buttons)[:20]:  # Top 20
    print(f"  📱 {button}")

# 4. Check AI functions
print("\n✅ AI INTEGRATION CHECK:")
ai_functions = [
    ("generate_image", "DALL-E 3 image generation"),
    ("analyze_image", "Vision (photo analysis)"),
    ("transcribe_audio", "Whisper (voice → text)"),
    ("generate_speech", "TTS (text → voice)"),
]

for func, description in ai_functions:
    if f"async def {func}" in content or f"await inference.{func}" in content:
        print(f"  ✅ {func:<20} ({description})")
    else:
        print(f"  ❌ {func:<20} ({description}) - MISSING")

# 5. Check callback handlers
print("\n✅ CALLBACK QUERY HANDLERS:")
callback_patterns = re.findall(r'callback_data="(.*?)"', content)
unique_callbacks = set(callback_patterns)
for cb in sorted(unique_callbacks)[:15]:
    print(f"  🔘 {cb}")

print("\n" + "=" * 60)
print("📊 SUMMARY:")
print(f"  - Commands registered: {len(commands) if commands_block else 0}")
print(f"  - Quick buttons found: {len(buttons)}")
print(f"  - Callback queries: {len(unique_callbacks)}")
print("\n✅ Check complete! Review bot_commands_test.txt for details")
