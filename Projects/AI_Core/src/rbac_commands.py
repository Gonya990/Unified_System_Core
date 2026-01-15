"""
RBAC Management Commands for Telegram Bot

Administrative commands for managing granular permissions.
"""

import logging

from telegram import Update
from telegram.ext import ContextTypes

logger = logging.getLogger(__name__)


async def grant_project_access(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    /grant_access <user_id> <project> <role>

    Examples:
    - /grant_access 123456 ai_core developer
    - /grant_access 789012 family_assistant family
    """
    user_id = update.effective_user.id

    # Check if user is admin
    if not context.bot_data.get("identity").rbac:
        await update.message.reply_text("❌ RBAC system not available")
        return

    rbac = context.bot_data.get("identity").rbac

    if not rbac.db.is_admin(user_id):
        await update.message.reply_text("⛔ Only admins can grant access")
        return

    if len(context.args) < 3:
        await update.message.reply_text(
            "Usage: /grant_access <user_id> <project> <role>\n\n"
            "Available projects:\n"
            "- ai_core\n"
            "- content_factory\n"
            "- family_assistant\n"
            "- automation\n"
            "- knowledge_base\n"
            "- personal\n"
            "- global\n\n"
            "Available roles:\n"
            "- owner (full control)\n"
            "- admin (administrative)\n"
            "- developer (code access)\n"
            "- member (basic access)\n"
            "- family (family projects)\n"
            "- guest (read-only)"
        )
        return

    try:
        from rbac import ProjectScope, Role

        target_user_id = int(context.args[0])
        project = ProjectScope(context.args[1].lower())
        role = Role[context.args[2].upper()]

        success = rbac.grant_role(target_user_id, role, project, granted_by=user_id)

        if success:
            await update.message.reply_text(
                f"✅ Access granted!\n\nUser: {target_user_id}\nProject: {project.value}\nRole: {role.value}"
            )
        else:
            await update.message.reply_text("❌ Failed to grant access")

    except ValueError as e:
        await update.message.reply_text(f"❌ Invalid project or role: {e}")
    except Exception as e:
        logger.error(f"Error granting access: {e}")
        await update.message.reply_text(f"❌ Error: {e}")


async def revoke_project_access(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    /revoke_access <user_id> <project>

    Example: /revoke_access 123456 ai_core
    """
    user_id = update.effective_user.id

    # Check if user is admin
    if not context.bot_data.get("identity").rbac:
        await update.message.reply_text("❌ RBAC system not available")
        return

    rbac = context.bot_data.get("identity").rbac

    if not rbac.db.is_admin(user_id):
        await update.message.reply_text("⛔ Only admins can revoke access")
        return

    if len(context.args) < 2:
        await update.message.reply_text("Usage: /revoke_access <user_id> <project>")
        return

    try:
        from rbac import ProjectScope

        target_user_id = int(context.args[0])
        project = ProjectScope(context.args[1].lower())

        success = rbac.revoke_permissions(target_user_id, project)

        if success:
            await update.message.reply_text(f"✅ Access revoked\n\nUser: {target_user_id}\nProject: {project.value}")
        else:
            await update.message.reply_text("❌ Failed to revoke access")

    except ValueError as e:
        await update.message.reply_text(f"❌ Invalid project: {e}")
    except Exception as e:
        logger.error(f"Error revoking access: {e}")
        await update.message.reply_text(f"❌ Error: {e}")


async def list_user_permissions(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    /my_permissions - Show your permissions
    /my_permissions <user_id> - Show another user's permissions (admin only)
    """
    user_id = update.effective_user.id

    if not context.bot_data.get("identity").rbac:
        await update.message.reply_text("❌ RBAC system not available")
        return

    rbac = context.bot_data.get("identity").rbac

    # Target user
    target_user_id = user_id
    if context.args:
        if not rbac.db.is_admin(user_id):
            await update.message.reply_text("⛔ Only admins can view other users' permissions")
            return
        target_user_id = int(context.args[0])

    # Get permissions
    permissions = rbac.get_user_permissions(target_user_id)

    if not permissions:
        await update.message.reply_text(
            "📭 No project-specific permissions found\n\n(You may still have global role-based access)"
        )
        return

    # Format message
    msg = f"**🔐 Permissions for User {target_user_id}**\n\n"

    for perm in permissions:
        msg += f"**{perm.project.value}**"
        if perm.resource != "*":
            msg += f" / {perm.resource}"
        msg += "\n"
        msg += f"Permissions: {', '.join([p.value for p in perm.permissions])}\n"
        if perm.granted_by:
            msg += f"Granted by: {perm.granted_by}\n"
        msg += "\n"

    await update.message.reply_text(msg, parse_mode="Markdown")


async def show_project_users(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    /project_users <project> - Show all users with access to a project

    Example: /project_users ai_core
    """
    user_id = update.effective_user.id

    if not context.bot_data.get("identity").rbac:
        await update.message.reply_text("❌ RBAC system not available")
        return

    rbac = context.bot_data.get("identity").rbac

    if not rbac.db.is_admin(user_id):
        await update.message.reply_text("⛔ Only admins can view project users")
        return

    if not context.args:
        await update.message.reply_text("Usage: /project_users <project>")
        return

    try:
        from rbac import ProjectScope

        project = ProjectScope(context.args[0].lower())
        users = rbac.get_project_users(project)

        if not users:
            await update.message.reply_text(
                f"📭 No users with explicit access to **{project.value}**", parse_mode="Markdown"
            )
            return

        msg = f"**👥 Users with access to {project.value}**\n\n"

        for uid in users:
            user_info = rbac.db.get_user(uid)
            if user_info:
                msg += f"- {user_info.get('full_name', 'Unknown')} ({uid})\n"
            else:
                msg += f"- User {uid}\n"

        await update.message.reply_text(msg, parse_mode="Markdown")

    except ValueError as e:
        await update.message.reply_text(f"❌ Invalid project: {e}")
    except Exception as e:
        logger.error(f"Error showing project users: {e}")
        await update.message.reply_text(f"❌ Error: {e}")


async def show_access_audit(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    /audit_log [limit] - Show access audit log (admin only)

    Example: /audit_log 50
    """
    user_id = update.effective_user.id

    if not context.bot_data.get("identity").rbac:
        await update.message.reply_text("❌ RBAC system not available")
        return

    rbac = context.bot_data.get("identity").rbac

    if not rbac.db.is_admin(user_id):
        await update.message.reply_text("⛔ Only admins can view audit logs")
        return

    limit = 20
    if context.args:
        try:
            limit = int(context.args[0])
        except:
            pass

    logs = rbac.get_audit_log(limit=limit)

    if not logs:
        await update.message.reply_text("📭 No audit log entries found")
        return

    msg = f"**🔍 Access Audit Log (last {len(logs)} entries)**\n\n"

    for log in logs[:20]:  # Show max 20 in message
        status = "✅" if log.get("access_granted") else "❌"
        msg += f"{status} User {log['user_id']} - {log['project']}/{log.get('resource', '*')}\n"
        msg += f"   Permission: {log.get('permission_checked', 'N/A')} | {log.get('timestamp', 'N/A')}\n\n"

    await update.message.reply_text(msg, parse_mode="Markdown")


# Register handlers in bot
def register_rbac_handlers(application):
    """Add RBAC command handlers to bot application"""
    from telegram.ext import CommandHandler

    application.add_handler(CommandHandler("grant_access", grant_project_access))
    application.add_handler(CommandHandler("revoke_access", revoke_project_access))
    application.add_handler(CommandHandler("my_permissions", list_user_permissions))
    application.add_handler(CommandHandler("project_users", show_project_users))
    application.add_handler(CommandHandler("audit_log", show_access_audit))

    logger.info("RBAC command handlers registered")
