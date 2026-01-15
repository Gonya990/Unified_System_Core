#!/usr/bin/env python3
"""
Unified System - Network-wide RBAC Configuration

Настраивает права доступа для всех устройств в Tailscale сети.
"""

import json
import logging
from pathlib import Path
import sys

# Add RBAC module to path
sys.path.insert(0, str(Path(__file__).parent.parent / "Projects/AI_Core/src"))

from rbac import (
    RBACManager,
    ProjectScope,
    Permission,
    Role,
)
from user_context_db import UserContextDB

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("NetworkRBAC")

# Network Device Registry
NETWORK_DEVICES = {
    # CORE Server
    "100.110.209.49": {
        "name": "CORE Server",
        "hostname": "unified-home-core-cloud",
        "role": "SYSTEM",
        "user_id": 1,  # System user
        "projects": ["global"],
        "permissions": "ALL",
    },
    # Igor's Devices
    "100.93.121.47": {
        "name": "MacBook Air (Office)",
        "hostname": "MacBookAir-2.lan",
        "role": "OWNER",
        "user_id": 708531393,  # Igor
        "projects": ["global", "ai_core", "content_factory", "automation", "knowledge_base"],
        "permissions": "ALL",
    },
    "100.86.233.87": {
        "name": "iPhone (Igor)",
        "role": "OWNER",
        "user_id": 708531393,
        "projects": ["global"],
        "permissions": "ALL",
    },
    "100.127.194.111": {
        "name": "Windows PC (Gaming+VM)",
        "role": "DEVELOPER",
        "user_id": 708531393,
        "projects": ["automation", "ai_core"],
        "permissions": ["read", "write", "execute"],
        "notes": "После миграции на VM - запуск агентов",
    },
    "100.114.27.103": {
        "name": "Tablet (Igor+Arthur)",
        "role": "FAMILY",
        "user_id": 708531393,  # Primary: Igor
        "secondary_users": [999999999],  # Arthur (нужен Telegram ID)
        "projects": ["family_assistant", "personal"],
        "permissions": ["read", "write"],
    },
    # Kostya's Devices
    "100.97.100.92": {
        "name": "Laptop (Kostya)",
        "role": "ADMIN",
        "user_id": 578363419,  # Kostya
        "projects": ["ai_core", "content_factory", "automation", "personal"],
        "permissions": ["read", "write", "execute", "delete", "share"],
    },
    "100.102.123.22": {
        "name": "Phone (Kostya)",
        "role": "ADMIN",
        "user_id": 578363419,
        "projects": ["global"],
        "permissions": ["read", "write", "execute", "share"],
    },
    "100.78.145.67": {
        "name": "Hardware Control (Kostya)",
        "role": "INFRASTRUCTURE_ADMIN",
        "user_id": 578363419,
        "projects": ["infrastructure"],
        "permissions": "ALL",
        "exclusive": True,
        "notes": "ЭКСКЛЮЗИВНЫЙ контроль железа и ресурсов - только Kostya!",
    },
    # Infrastructure Nodes
    "100.74.137.122": {
        "name": "Tools Server",
        "role": "DEVELOPER",
        "user_id": 1,  # System
        "projects": ["automation", "infrastructure"],
        "permissions": ["read", "execute"],
    },
    "100.81.133.25": {
        "name": "Home Assistant",
        "role": "FAMILY",
        "user_id": 708531393,  # Igor (primary)
        "secondary_users": [578363419, 999999999],  # Oksana, Arthur
        "projects": ["family_assistant", "automation"],
        "permissions": ["read", "write", "execute"],
    },
    "100.100.134.4": {
        "name": "Unknown Resource",
        "role": "PENDING",
        "user_id": None,
        "projects": [],
        "permissions": [],
        "notes": "Требует уточнения у Кости - назначение и права доступа",
    },
}


def setup_network_rbac(rbac: RBACManager):
    """Setup RBAC for all network devices"""
    logger.info("=" * 60)
    logger.info("Setting up Network-wide RBAC")
    logger.info("=" * 60)

    configured = 0
    skipped = 0

    for ip, device in NETWORK_DEVICES.items():
        device_name = device["name"]
        role = device["role"]
        user_id = device.get("user_id")

        if role == "PENDING" or user_id is None:
            logger.warning(f"⏭️  Skipping {device_name} ({ip}) - {device.get('notes', 'No user assigned')}")
            skipped += 1
            continue

        logger.info(f"\n📱 Configuring: {device_name} ({ip})")
        logger.info(f"   Role: {role}, User: {user_id}")

        # Grant role-based permissions
        if device["permissions"] == "ALL":
            # Full access to all specified projects
            for project_name in device.get("projects", ["global"]):
                try:
                    project = ProjectScope(project_name)
                    rbac.grant_role(user_id, Role[role], project, granted_by=user_id)
                    logger.info(f"   ✅ Granted {role} to {project.value}")
                except ValueError:
                    logger.warning(f"   ⚠️  Unknown project: {project_name}")
        else:
            # Granular permissions
            permissions = set()
            for perm_name in device.get("permissions", []):
                try:
                    permissions.add(Permission(perm_name))
                except ValueError:
                    logger.warning(f"   ⚠️  Unknown permission: {perm_name}")

            for project_name in device.get("projects", []):
                try:
                    project = ProjectScope(project_name)
                    rbac.grant_permissions(user_id, project, permissions, granted_by=user_id)
                    logger.info(f"   ✅ Granted {permissions} to {project.value}")
                except ValueError:
                    logger.warning(f"   ⚠️  Unknown project: {project_name}")

        # Handle secondary users (для общих устройств)
        for secondary_user in device.get("secondary_users", []):
            if secondary_user:
                logger.info(f"   👥 Secondary user: {secondary_user}")
                # Grant same permissions as primary
                for project_name in device.get("projects", []):
                    try:
                        project = ProjectScope(project_name)
                        rbac.grant_role(secondary_user, Role.FAMILY, project, granted_by=user_id)
                    except ValueError:
                        pass

        configured += 1

    logger.info("")
    logger.info("=" * 60)
    logger.info(f"✅ Configuration complete")
    logger.info(f"   Configured: {configured} devices")
    logger.info(f"   Skipped: {skipped} devices")
    logger.info("=" * 60)


def export_network_config(output_file: Path):
    """Export network configuration to JSON"""
    config = {
        "version": "1.0",
        "updated": "2026-01-15",
        "network": "Tailscale VPN",
        "devices": NETWORK_DEVICES,
    }

    with open(output_file, "w") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)

    logger.info(f"📄 Network config exported to: {output_file}")


def main():
    """Main execution"""
    logger.info("🌐 Unified System - Network RBAC Setup")
    logger.info("")

    # Initialize database and RBAC
    db = UserContextDB()
    rbac = RBACManager(db)

    # Setup network-wide permissions
    setup_network_rbac(rbac)

    # Export configuration
    config_file = Path(__file__).parent.parent / "Agent_Context/Infrastructure/network_config.json"
    config_file.parent.mkdir(parents=True, exist_ok=True)
    export_network_config(config_file)

    logger.info("")
    logger.info("🎯 Next Steps:")
    logger.info("1. Review TAILSCALE_NETWORK_MAP.md")
    logger.info("2. Verify permissions with /my_permissions in bot")
    logger.info("3. Deploy to CORE server (100.110.209.49)")
    logger.info("")


if __name__ == "__main__":
    main()
