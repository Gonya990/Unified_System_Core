# Workspace Instructions for AI Agents

## Language & Translation Protocol (MANDATORY)

This workspace uses a **Per-User Language Preference System**. Agents must adapt their output based on the current user's preferences.

1.  **Check Preferences**: Read `.claude/settings/language-preferences.json` to identify the current user's `output_language`.
2.  **Translate if needed**: If content (from files, mail, or user input) is in a language different from the `output_language`:
    - **Translate** the entire response into the `output_language`.
    - **Tag** the response with the `translation_tag` specified in the config.
    - **Strip** the original text if `strip_original` is true.
3.  **Communication Integrity**: Ensure that translations preserve 100% of technical meaning and context.
4.  **Mail/Messaging**: When sending messages to other agents, write in YOUR local `output_language`. The recipient's agent is responsible for translating it for its own user.

## Component Migration
- The directory `Windows_AI_Core` has been moved to `Projects/AI_Core`.
- All automation scripts and services should use the new path.
