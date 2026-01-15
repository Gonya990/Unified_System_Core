#!/usr/bin/env python3
"""
RBAC System Initialization and Testing Script

This script:
1. Initializes the RBAC system
2. Sets up default permissions for the owner
3. Creates example access patterns
4. Tests permission checks
"""

import logging
import sys
from pathlib import Path

# Setup paths
ROOT_DIR = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(ROOT_DIR / "Projects/AI_Core/src"))

from rbac import (  # noqa: E402
    Permission,
    ProjectScope,
    RBACManager,
    create_family_member_access,
    setup_default_permissions,
)
from user_context_db import UserContextDB  # noqa: E402

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger("RBAC Init")


def initialize_rbac():
    """Initialize RBAC system with default setup"""
    logger.info("=" * 60)
    logger.info("Initializing RBAC System")
    logger.info("=" * 60)

    # Initialize database
    db = UserContextDB()
    logger.info("✅ Database initialized")

    # Initialize RBAC
    rbac = RBACManager(db)
    logger.info("✅ RBAC Manager initialized")

    # Setup owner (Igor - 708531393)
    owner_id = 708531393
    setup_default_permissions(rbac, owner_id)
    logger.info(f"✅ Owner permissions configured (User {owner_id})")

    return rbac, db


def setup_example_users(rbac: RBACManager):
    """Setup example access patterns"""
    logger.info("")
    logger.info("=" * 60)
    logger.info("Setting up example users")
    logger.info("=" * 60)

    owner_id = 708531393

    # Example 1: Family member (Kostya - 578363419)
    family_member_id = 578363419
    create_family_member_access(rbac, family_member_id, granted_by=owner_id)
    logger.info(f"✅ Family access granted to User {family_member_id}")

    # Example 2: Developer access (example user)
    # developer_id = 123456789
    # create_developer_access(rbac, developer_id, granted_by=owner_id)
    # logger.info(f"✅ Developer access granted to User {developer_id}")

    logger.info("")
    logger.info("Example setup complete!")


def test_permissions(rbac: RBACManager):
    """Test permission checks"""
    logger.info("")
    logger.info("=" * 60)
    logger.info("Testing permission checks")
    logger.info("=" * 60)

    owner_id = 708531393
    family_member_id = 578363419

    # Test 1: Owner can access everything
    test_cases = [
        (owner_id, ProjectScope.AI_CORE, Permission.ADMIN, True, "Owner -> AI_CORE/ADMIN"),
        (owner_id, ProjectScope.CONTENT_FACTORY, Permission.DELETE, True, "Owner -> CONTENT_FACTORY/DELETE"),
        (family_member_id, ProjectScope.FAMILY_ASSISTANT, Permission.READ, True, "Family -> FAMILY_ASSISTANT/READ"),
        (family_member_id, ProjectScope.FAMILY_ASSISTANT, Permission.WRITE, True, "Family -> FAMILY_ASSISTANT/WRITE"),
        (family_member_id, ProjectScope.AI_CORE, Permission.WRITE, False, "Family -> AI_CORE/WRITE (should deny)"),
        (family_member_id, ProjectScope.PERSONAL, Permission.READ, True, "Family -> PERSONAL/READ"),
    ]

    passed = 0
    failed = 0

    for user_id, project, permission, expected, description in test_cases:
        result = rbac.check_permission(user_id, project, permission, log_access=False)
        status = "✅ PASS" if result == expected else "❌ FAIL"

        if result == expected:
            passed += 1
        else:
            failed += 1

        logger.info(f"{status} | {description} -> {result}")

    logger.info("")
    logger.info(f"Test results: {passed} passed, {failed} failed")

    return failed == 0


def show_user_permissions(rbac: RBACManager, user_id: int):
    """Display user's permissions"""
    logger.info("")
    logger.info("=" * 60)
    logger.info(f"Permissions for User {user_id}")
    logger.info("=" * 60)

    permissions = rbac.get_user_permissions(user_id)

    if not permissions:
        logger.info("No project-specific permissions found")
        logger.info("(User may have global role-based access)")
        return

    for perm in permissions:
        resource_info = f"/{perm.resource}" if perm.resource != "*" else ""
        logger.info(f"📁 {perm.project.value}{resource_info}")
        logger.info(f"   Permissions: {', '.join([p.value for p in perm.permissions])}")
        if perm.granted_by:
            logger.info(f"   Granted by: {perm.granted_by}")
        logger.info("")


def main():
    """Main execution"""
    logger.info("🚀 RBAC System Initialization Script")
    logger.info("")

    try:
        # Initialize
        rbac, db = initialize_rbac()

        # Setup examples
        setup_example_users(rbac)

        # Test
        success = test_permissions(rbac)

        # Show permissions
        show_user_permissions(rbac, 708531393)
        show_user_permissions(rbac, 578363419)

        # Summary
        logger.info("")
        logger.info("=" * 60)
        if success:
            logger.info("✅ RBAC System successfully initialized and tested!")
        else:
            logger.warning("⚠️ RBAC System initialized but some tests failed")
        logger.info("=" * 60)
        logger.info("")
        logger.info("Next steps:")
        logger.info("1. Restart Telegram Bot to enable RBAC commands")
        logger.info("2. Use /my_permissions to check your access")
        logger.info("3. Use /grant_access to manage other users")
        logger.info("4. Check docs/RBAC_GUIDE.md for full documentation")
        logger.info("")

        return 0 if success else 1

    except Exception as e:
        logger.error(f"❌ Error during initialization: {e}")
        import traceback

        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
