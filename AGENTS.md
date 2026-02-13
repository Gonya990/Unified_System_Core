# Workspace Instructions for AI Agents

## Language & Translation Protocol (MANDATORY)

This workspace uses a **Per-User Language Preference System**. Agents must
adapt their output based on the current user's preferences.

1. **Check Preferences**: Read `.claude/settings/language-preferences.json` to
   identify the current user's `output_language`.
2. **Translate if needed**: If content (from files, mail, or user input) is in a
   language different from the `output_language`:
    - **Translate** the entire response into the `output_language`.
    - **Tag** the response with the `translation_tag` specified in the config.
    - **Strip** the original text if `strip_original` is true.
3. **Communication Integrity**: Ensure that translations preserve 100% of
   technical meaning and context.
4. **Mail/Messaging**: When sending messages to other agents, write in YOUR
   local `output_language`. The recipient's agent is responsible for translating
   it for its own user.

## Component Locations

| Component | Path | Description |
| :--- | :--- | :--- |
| AI Bot | `Projects/AI_Core/` | Main AI bot with calendar, memory, |
| | | and multi-provider inference |
| Content | `Projects/Content_Factory/` | Video generation pipeline with |
| Factory | | Sora2 and Pexels integration |
| ChatKit | `Projects/ChatKit/` | Web dashboard for management |
| IdentityManager | `Scripts/Security/` | Secure identity & vault access |
| | `identity_manager.py` | (Argon2id + RSA) |

**Note**: The old `Windows_AI_Core` directory has been migrated to
`Projects/AI_Core`.

## OpenAI ChatGPT Conversations Knowledge Base

**Location:** `Agent_Context/Knowledge_Base/OpenAI_Conversations/`

**Description:**
- **English:** Historical ChatGPT conversations imported from OpenAI export
- **Russian:** Исторические разговоры ChatGPT, импортированные из экспорта OpenAI

**Last Updated:** 2026-01-12 21:13:14

**Contents:** 50 conversation files

**Purpose:** Reference material for continuity, context, and learning from past interactions.

---
