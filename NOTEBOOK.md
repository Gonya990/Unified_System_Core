# 📓 Agent Workspace Notebook

**Last Updated:** 2026-01-13
**Agent:** Antigravity

## ⚖️ Morality & Rules (The Conscience)

- **Global1Sim Repair:** Submodule `Projects/global1sim` is broken.
  **Action:** Ignore errors but do not deploy until fixed.
- **Contact Form:** Spec sent to `VioletCastle`.
  **Rule:** Do not implement code until Spec is approved (Mail > 502).
- **Mail Loop:** Resolved.
  **Rule:** Never send auto-ack to subjects containing "Re:" and "Concilium".

## 📝 Drafts & snippets

### Contact Form Spec (Sent)

- Fields: Name, Email, Subject, Body
- Validation: Zod
- Action: POST /api/contact -> Telegram Alert

## ⏳ Pending / Waiting

- [ ] Reply from `VioletCastle` (Mail ID > 502)
- [ ] Fix permissions for `global1sim` repo (Owner: Kostya)

## 💡 Ideas / Backlog

- Add "Concilium" mode explanation to Wiki?
- Refactor `unified.py` to use `rich` library for better UI?

---
*Use this file for temporary code blocks, swift notes, and context tracking.*
