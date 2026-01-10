# Translation & Language Protocol

This document defines how agents should handle language preferences to ensure smooth collaboration between users with different language needs (e.g., Kosta prefers English, Igor prefers Russian).

## Configuration
All preferences are stored in: `.claude/settings/language-preferences.json`

## Policies
### 1. Presentation Layer (User Output)
- Agents MUST present their final answer in the user's `output_language`.
- If the agent needs to "read" or "process" content in a different language, it must translate it before showing it to the user.
- The `[tag]` (e.g., `[russian]`) indicates that the content was originally in that language.
- Original text is removed to keep the interface clean and English-only (or Russian-only) for the user.

### 2. Coordination Layer (Inter-Agent Mail)
- Agents send mail in the language THEY are currently operating in.
- Metadata should be included if possible (e.g., `[lang:en]`) to help the receiving agent.
- **NEVER** force a global language on other agents; respect that they have their own local user preferences.

## Implementation Checklist
- [ ] Check `.claude/settings/language-preferences.json` on session start.
- [ ] Set local session instructions based on the active `user` or `agent` key.
- [ ] Apply translation/tagging/stripping logic to all final responses.
