# Web settings grayed out

**Date | Дата:** Unknown_Date 00:00:00

**ID:** 6932f294-69e8-832c-9371-40af298ba588

---

**👤 User | Пользователь:**

opencode web settings grayed out


**🤖 Assistant | Ассистент:**

Do you mean OpenCode when you say “opencode web”? Or do you mean Visual Studio Code (or something else)? 
If you mean OpenCode — I couldn’t find widespread reports of a “web settings” screen being grayed out in OpenCode. OpenCode’s configuration is done via JSON or JSONC config files (e.g. opencode.jsonc or ~/.config/opencode/opencode.json) rather than via a typical GUI settings panel. 
opencode.ai

That suggests there may simply not be a “web settings” GUI in OpenCode — hence nothing to enable/disable.

If you downloaded a version for Windows, there is an issue in the project repo about “no editor set / can’t open editor”. 
GitHub

If you meant VS Code (or a similar code editor), “settings greyed out” usually means that:

You are using a non-default profile (so user settings won’t apply until you switch back to the “Default” profile). 
Stack Overflow
+1

Or the settings you tried to change are unknown/unrecognized (maybe due to disabled/missing extensions), so the editor disabled them. 
Stack Overflow
+1

Or there’s some workspace-level config overriding them. 
askai.glarity.app
+1

If you clarify exactly where (which tool/editor, which “web settings” panel) you see it grayed out — and maybe paste the exact message you see — I can try to help you debug.

