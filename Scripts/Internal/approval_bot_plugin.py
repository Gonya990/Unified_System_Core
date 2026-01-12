import json
import logging
import sqlite3
from datetime import datetime

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

logger = logging.getLogger(__name__)

class ApprovalManager:
    def __init__(self, db_path="/home/gonya/Unified_System/Projects/AI_Core/user_context.db"):
        self.db_path = db_path

    def request_approval(self, agent: str, task_type: str, payload: dict):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO pending_approvals (requester_agent, task_type, task_payload, created_at)
                VALUES (?, ?, ?, ?)
            ''', (agent, task_type, json.dumps(payload), datetime.now()))
            conn.commit()

    def get_pending_to_notify(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM pending_approvals WHERE status = 'pending' ORDER BY created_at ASC")
            return [dict(row) for row in cursor.fetchall()]

    def update_status(self, approval_id: int, status: str):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE pending_approvals SET status = ? WHERE id = ?", (status, approval_id))
            conn.commit()

approval_mgr = ApprovalManager()

async def check_approvals_job(context: ContextTypes.DEFAULT_TYPE):
    """Background job to notify about pending approvals."""
    pending = approval_mgr.get_pending_to_notify()
    if not pending:
        return

    admin_id = 708531393  # Primary Admin ID

    for task in pending:
        task_id = task['id']
        try:
            payload = json.loads(task['task_payload'])
        except:
            payload = {'summary': task['task_payload']}

        text = f"🛡️ **Request for Approval**\n\n" \
               f"👤 **Agent:** `{task['requester_agent']}`\n" \
               f"📌 **Type:** `{task['task_type']}`\n" \
               f"📝 **Details:**\n{payload.get('summary', 'No summary provided')}"

        keyboard = [[
            InlineKeyboardButton("✅ Approve", callback_data=f"apprv_ok_{task_id}"),
            InlineKeyboardButton("❌ Reject", callback_data=f"apprv_no_{task_id}")
        ]]
        reply_markup = InlineKeyboardMarkup(keyboard)

        try:
            await context.bot.send_message(
                chat_id=admin_id,
                text=text,
                reply_markup=reply_markup,
                parse_mode='Markdown'
            )
            approval_mgr.update_status(task_id, 'notified')
        except Exception as e:
            logger.error(f"Failed to send approval request: {e}")

async def process_approval_button(query, data):
    """Handle approval-related callback data."""
    parts = data.split('_')
    action = parts[1] # ok, no
    task_id = int(parts[2])

    if action == "ok":
        approval_mgr.update_status(task_id, 'approved')
        await query.edit_message_text(f"✅ Task {task_id} marked as **APPROVED**.", parse_mode='Markdown')
    elif action == "no":
        approval_mgr.update_status(task_id, 'rejected')
        await query.edit_message_text(f"❌ Task {task_id} marked as **REJECTED**.", parse_mode='Markdown')
