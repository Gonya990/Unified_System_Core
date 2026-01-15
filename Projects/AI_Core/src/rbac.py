"""
Granular Role-Based Access Control (RBAC) System

This module implements a comprehensive RBAC system with:
- Hierarchical roles (OWNER > ADMIN > DEVELOPER > MEMBER > FAMILY > GUEST)
- Granular permissions (read, write, execute, delete, admin)
- Project-scoped access control
- Resource-level permissions
- Audit logging

Philosophy:
"Каждому индивидууму - свои права доступа к проектам и наработкам"
(To each individual - their own access rights to projects and achievements)
"""

import json
import logging
from datetime import datetime
from enum import Enum
from typing import Optional

logger = logging.getLogger(__name__)


class Permission(str, Enum):
    """Base permissions for all resources"""

    READ = "read"  # Can view/read resource
    WRITE = "write"  # Can create/update resource
    EXECUTE = "execute"  # Can run/trigger actions
    DELETE = "delete"  # Can delete resource
    ADMIN = "admin"  # Full administrative access
    SHARE = "share"  # Can share with others
    MANAGE_USERS = "manage_users"  # Can manage user access


class Role(str, Enum):
    """Predefined role hierarchy"""

    OWNER = "OWNER"  # Полный контроль системы (original creator)
    ADMIN = "ADMIN"  # Административный доступ ко всем проектам
    DEVELOPER = "DEVELOPER"  # Доступ к разработке и кодовой базе
    MEMBER = "MEMBER"  # Базовый доступ к общим ресурсам
    FAMILY = "FAMILY"  # Доступ к семейным проектам
    GUEST = "GUEST"  # Минимальный доступ только для чтения


class ProjectScope(str, Enum):
    """Available project scopes in the Unified System"""

    AI_CORE = "ai_core"  # Telegram Bot & AI Infrastructure
    CONTENT_FACTORY = "content_factory"  # Video/Content Generation
    FAMILY_ASSISTANT = "family_assistant"  # Morning Brief, Homework, etc.
    AUTOMATION = "automation"  # Scripts and automation tools
    KNOWLEDGE_BASE = "knowledge_base"  # Personal knowledge management
    FINANCE = "finance"  # Financial tracking (if exists)
    HEALTH = "health"  # Health tracking integration
    INFRASTRUCTURE = "infrastructure"  # System-wide infrastructure
    PERSONAL = "personal"  # User's personal data
    GLOBAL = "global"  # System-wide access


# Default permission bundles for each role
ROLE_PERMISSIONS = {
    Role.OWNER: {
        Permission.READ,
        Permission.WRITE,
        Permission.EXECUTE,
        Permission.DELETE,
        Permission.ADMIN,
        Permission.SHARE,
        Permission.MANAGE_USERS,
    },
    Role.ADMIN: {
        Permission.READ,
        Permission.WRITE,
        Permission.EXECUTE,
        Permission.DELETE,
        Permission.SHARE,
        Permission.MANAGE_USERS,
    },
    Role.DEVELOPER: {Permission.READ, Permission.WRITE, Permission.EXECUTE, Permission.SHARE},
    Role.MEMBER: {Permission.READ, Permission.WRITE, Permission.EXECUTE},
    Role.FAMILY: {Permission.READ, Permission.WRITE},
    Role.GUEST: {Permission.READ},
}


class AccessControlEntry:
    """Single access control entry for a user-project-resource combination"""

    def __init__(
        self,
        user_id: int,
        project: ProjectScope,
        resource: str = "*",
        permissions: set[Permission] = None,
        granted_by: Optional[int] = None,
        granted_at: Optional[datetime] = None,
    ):
        self.user_id = user_id
        self.project = project
        self.resource = resource  # "*" for project-wide, specific for resource-level
        self.permissions = permissions or set()
        self.granted_by = granted_by
        self.granted_at = granted_at or datetime.now()

    def to_dict(self) -> dict:
        return {
            "user_id": self.user_id,
            "project": self.project.value,
            "resource": self.resource,
            "permissions": [p.value for p in self.permissions],
            "granted_by": self.granted_by,
            "granted_at": self.granted_at.isoformat(),
        }

    @staticmethod
    def from_dict(data: dict) -> "AccessControlEntry":
        return AccessControlEntry(
            user_id=data["user_id"],
            project=ProjectScope(data["project"]),
            resource=data.get("resource", "*"),
            permissions={Permission(p) for p in data.get("permissions", [])},
            granted_by=data.get("granted_by"),
            granted_at=datetime.fromisoformat(data["granted_at"]) if data.get("granted_at") else None,
        )


class RBACManager:
    """Main RBAC management class"""

    def __init__(self, db):
        """
        Args:
            db: Database instance (UserContextDB or FirestoreDB)
        """
        self.db = db
        self._init_permissions_table()

    def _init_permissions_table(self):
        """Initialize permissions table in database"""
        try:
            import sqlite3

            # Check if we're using SQLite
            if hasattr(self.db, "db_path"):
                with sqlite3.connect(self.db.db_path) as conn:
                    cursor = conn.cursor()
                    cursor.execute("""
                        CREATE TABLE IF NOT EXISTS user_permissions (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            user_id INTEGER NOT NULL,
                            project TEXT NOT NULL,
                            resource TEXT DEFAULT '*',
                            permissions TEXT NOT NULL,
                            granted_by INTEGER,
                            granted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                            FOREIGN KEY(user_id) REFERENCES users(user_id),
                            UNIQUE(user_id, project, resource)
                        )
                    """)
                    # Audit log table
                    cursor.execute("""
                        CREATE TABLE IF NOT EXISTS access_audit_log (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            user_id INTEGER NOT NULL,
                            project TEXT NOT NULL,
                            resource TEXT,
                            action TEXT NOT NULL,
                            permission_checked TEXT,
                            access_granted BOOLEAN NOT NULL,
                            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                            context TEXT
                        )
                    """)
                    conn.commit()
                    logger.info("RBAC tables initialized (SQLite)")
        except Exception as e:
            logger.error(f"Failed to initialize RBAC tables: {e}")

    # ========== Core RBAC Methods ==========

    def grant_role(
        self,
        user_id: int,
        role: Role,
        project: ProjectScope = ProjectScope.GLOBAL,
        granted_by: Optional[int] = None,
    ) -> bool:
        """
        Grant a predefined role to a user for a project.

        Args:
            user_id: User to grant role to
            role: Role to grant
            project: Project scope (default: GLOBAL)
            granted_by: Admin user granting the role

        Returns:
            Success status
        """
        permissions = ROLE_PERMISSIONS.get(role, set())
        return self.grant_permissions(user_id, project, permissions, granted_by=granted_by)

    def grant_permissions(
        self,
        user_id: int,
        project: ProjectScope,
        permissions: set[Permission],
        resource: str = "*",
        granted_by: Optional[int] = None,
    ) -> bool:
        """
        Grant specific permissions to a user for a project/resource.

        Args:
            user_id: User to grant permissions to
            project: Project scope
            permissions: Set of permissions to grant
            resource: Specific resource (default: "*" for project-wide)
            granted_by: Admin user granting the permissions

        Returns:
            Success status
        """
        try:
            import sqlite3

            if hasattr(self.db, "db_path"):
                permissions_json = json.dumps([p.value for p in permissions])

                with sqlite3.connect(self.db.db_path) as conn:
                    cursor = conn.cursor()
                    cursor.execute(
                        """
                        INSERT OR REPLACE INTO user_permissions
                        (user_id, project, resource, permissions, granted_by, granted_at)
                        VALUES (?, ?, ?, ?, ?, ?)
                    """,
                        (user_id, project.value, resource, permissions_json, granted_by, datetime.now()),
                    )
                    conn.commit()

                logger.info(f"Granted permissions {permissions} to user {user_id} for {project.value}/{resource}")
                return True
        except Exception as e:
            logger.error(f"Failed to grant permissions: {e}")
            return False

    def revoke_permissions(
        self,
        user_id: int,
        project: ProjectScope,
        resource: str = "*",
    ) -> bool:
        """Revoke all permissions for a user on a project/resource"""
        try:
            import sqlite3

            if hasattr(self.db, "db_path"):
                with sqlite3.connect(self.db.db_path) as conn:
                    cursor = conn.cursor()
                    cursor.execute(
                        "DELETE FROM user_permissions WHERE user_id = ? AND project = ? AND resource = ?",
                        (user_id, project.value, resource),
                    )
                    conn.commit()

                logger.info(f"Revoked permissions for user {user_id} on {project.value}/{resource}")
                return True
        except Exception as e:
            logger.error(f"Failed to revoke permissions: {e}")
            return False

    def check_permission(
        self,
        user_id: int,
        project: ProjectScope,
        permission: Permission,
        resource: str = "*",
        log_access: bool = True,
    ) -> bool:
        """
        Check if user has a specific permission for a project/resource.

        Args:
            user_id: User to check
            project: Project scope
            permission: Permission to check
            resource: Specific resource (default: "*")
            log_access: Whether to log this access check

        Returns:
            True if user has permission, False otherwise
        """
        # Legacy role-based check first (backward compatibility)
        try:
            user_role = self.db.get_role(user_id)

            # OWNER и ADMIN have global access to everything
            if user_role in ["OWNER", "ADMIN"]:
                if log_access:
                    self._log_access(user_id, project, resource, permission.value, True, "Global admin/owner access")
                return True
        except Exception:
            pass  # Database might not have role field yet

        try:
            import sqlite3

            if hasattr(self.db, "db_path"):
                with sqlite3.connect(self.db.db_path) as conn:
                    cursor = conn.cursor()

                    # Check project-wide permissions first
                    cursor.execute(
                        "SELECT permissions FROM user_permissions WHERE user_id = ? AND project = ? AND resource = '*'",
                        (user_id, project.value),
                    )
                    row = cursor.fetchone()

                    if row:
                        permissions_list = json.loads(row[0])
                        if permission.value in permissions_list or Permission.ADMIN.value in permissions_list:
                            if log_access:
                                self._log_access(
                                    user_id, project, resource, permission.value, True, "Project-wide permission"
                                )
                            return True

                    # Check resource-specific permissions
                    if resource != "*":
                        cursor.execute(
                            "SELECT permissions FROM user_permissions WHERE user_id = ? AND project = ? AND resource = ?",
                            (user_id, project.value, resource),
                        )
                        row = cursor.fetchone()

                        if row:
                            permissions_list = json.loads(row[0])
                            if permission.value in permissions_list or Permission.ADMIN.value in permissions_list:
                                if log_access:
                                    self._log_access(
                                        user_id,
                                        project,
                                        resource,
                                        permission.value,
                                        True,
                                        "Resource-specific permission",
                                    )
                                return True

            if log_access:
                self._log_access(user_id, project, resource, permission.value, False, "No matching permissions")
            return False

        except Exception as e:
            logger.error(f"Failed to check permission: {e}")
            return False

    def get_user_permissions(self, user_id: int, project: Optional[ProjectScope] = None) -> list[AccessControlEntry]:
        """
        Get all permissions for a user, optionally filtered by project.

        Args:
            user_id: User ID
            project: Optional project filter

        Returns:
            List of AccessControlEntry objects
        """
        try:
            import sqlite3

            if hasattr(self.db, "db_path"):
                with sqlite3.connect(self.db.db_path) as conn:
                    conn.row_factory = sqlite3.Row
                    cursor = conn.cursor()

                    if project:
                        cursor.execute(
                            "SELECT * FROM user_permissions WHERE user_id = ? AND project = ?",
                            (user_id, project.value),
                        )
                    else:
                        cursor.execute("SELECT * FROM user_permissions WHERE user_id = ?", (user_id,))

                    entries = []
                    for row in cursor.fetchall():
                        entries.append(
                            AccessControlEntry(
                                user_id=row["user_id"],
                                project=ProjectScope(row["project"]),
                                resource=row["resource"],
                                permissions={Permission(p) for p in json.loads(row["permissions"])},
                                granted_by=row.get("granted_by"),
                                granted_at=datetime.fromisoformat(row["granted_at"]) if row.get("granted_at") else None,
                            )
                        )
                    return entries
        except Exception as e:
            logger.error(f"Failed to get user permissions: {e}")
            return []

    def get_project_users(self, project: ProjectScope) -> list[int]:
        """Get all users who have any permissions on a project"""
        try:
            import sqlite3

            if hasattr(self.db, "db_path"):
                with sqlite3.connect(self.db.db_path) as conn:
                    cursor = conn.cursor()
                    cursor.execute(
                        "SELECT DISTINCT user_id FROM user_permissions WHERE project = ?",
                        (project.value,),
                    )
                    return [row[0] for row in cursor.fetchall()]
        except Exception as e:
            logger.error(f"Failed to get project users: {e}")
            return []

    def _log_access(
        self,
        user_id: int,
        project: ProjectScope,
        resource: str,
        permission: str,
        granted: bool,
        context: str = "",
    ):
        """Log access attempt for audit trail"""
        try:
            import sqlite3

            if hasattr(self.db, "db_path"):
                with sqlite3.connect(self.db.db_path) as conn:
                    cursor = conn.cursor()
                    cursor.execute(
                        """
                        INSERT INTO access_audit_log
                        (user_id, project, resource, action, permission_checked, access_granted, timestamp, context)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                        (
                            user_id,
                            project.value,
                            resource,
                            "access_check",
                            permission,
                            1 if granted else 0,
                            datetime.now(),
                            context,
                        ),
                    )
                    conn.commit()
        except Exception as e:
            logger.debug(f"Failed to log access: {e}")

    def get_audit_log(
        self,
        user_id: Optional[int] = None,
        project: Optional[ProjectScope] = None,
        limit: int = 100,
    ) -> list[dict]:
        """Retrieve audit log entries"""
        try:
            import sqlite3

            if hasattr(self.db, "db_path"):
                with sqlite3.connect(self.db.db_path) as conn:
                    conn.row_factory = sqlite3.Row
                    cursor = conn.cursor()

                    query = "SELECT * FROM access_audit_log WHERE 1=1"
                    params = []

                    if user_id:
                        query += " AND user_id = ?"
                        params.append(user_id)

                    if project:
                        query += " AND project = ?"
                        params.append(project.value)

                    query += " ORDER BY timestamp DESC LIMIT ?"
                    params.append(limit)

                    cursor.execute(query, params)
                    return [dict(row) for row in cursor.fetchall()]
        except Exception as e:
            logger.error(f"Failed to get audit log: {e}")
            return []


# ========== Convenience Functions ==========


def setup_default_permissions(rbac: RBACManager, owner_id: int):
    """
    Setup default permissions for a new system.

    Args:
        rbac: RBACManager instance
        owner_id: ID of the system owner (full access)
    """
    # Grant OWNER role to system owner
    rbac.grant_role(owner_id, Role.OWNER, ProjectScope.GLOBAL, granted_by=owner_id)

    logger.info(f"✅ Default RBAC permissions configured. Owner: {owner_id}")


def create_family_member_access(rbac: RBACManager, user_id: int, granted_by: int):
    """
    Convenience: Grant family member access to relevant projects.

    Args:
        rbac: RBACManager instance
        user_id: Family member user ID
        granted_by: Admin granting access
    """
    # Grant FAMILY role to family projects
    rbac.grant_role(user_id, Role.FAMILY, ProjectScope.FAMILY_ASSISTANT, granted_by=granted_by)
    rbac.grant_permissions(
        user_id,
        ProjectScope.PERSONAL,
        {Permission.READ, Permission.WRITE},
        granted_by=granted_by,
    )

    logger.info(f"✅ Family member access granted to user {user_id}")


def create_developer_access(rbac: RBACManager, user_id: int, granted_by: int):
    """
    Convenience: Grant developer access to code projects.

    Args:
        rbac: RBACManager instance
        user_id: Developer user ID
        granted_by: Admin granting access
    """
    # Grant DEVELOPER role to relevant projects
    for project in [ProjectScope.AI_CORE, ProjectScope.CONTENT_FACTORY, ProjectScope.AUTOMATION]:
        rbac.grant_role(user_id, Role.DEVELOPER, project, granted_by=granted_by)

    logger.info(f"✅ Developer access granted to user {user_id}")
