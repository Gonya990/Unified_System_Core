path = "/home/gonya/Unified_System_Core/Projects/AI_Core/src/ai_telegram_bot_v2.py"
with open(path) as f:
    lines = f.readlines()

new_lines = []
skip = False
for _i, line in enumerate(lines):
    # Fix the mess around line 4720-4740
    if "def main():" in line:
        new_lines.append(line)
        # Skip until we find the real application initialization
        continue

    if "[STARTUP] Restored Google Session" in line:
        # Fix indentation
        new_lines.append('                    logger.info(f"[STARTUP] Restored Google Session for user {uid}")\n')
        continue

    new_lines.append(line)

with open(path, "w") as f:
    f.writelines(new_lines)
print("File patched")
