import os
import sys
import unittest

import yaml

# Add Utilities to path
sys.path.append(os.path.join(os.getcwd(), "Scripts/Utilities"))
from token_broker import TokenBroker


class TestTokenBrokerUpgraded(unittest.TestCase):
    def setUp(self):
        self.test_vault = os.path.join(os.getcwd(), "test_vault.yaml")
        self.test_rbac = os.path.join(os.getcwd(), "test_rbac.yaml")
        self.master_key = "test_master_token"
        os.environ["AGENT_MAIL_TOKEN"] = self.master_key

        # Reset Singleton for testing
        TokenBroker._instance = None
        self.broker = TokenBroker(vault_path=self.test_vault)

    def tearDown(self):
        if os.path.exists(self.test_vault):
            os.remove(self.test_vault)
        if os.path.exists(self.test_rbac):
            os.remove(self.test_rbac)

    def test_encryption_unification(self):
        """Verify encryption matches IdentityOrchestrator expectation."""
        plaintext = "secret_data_123"
        # Test with default system salt
        encrypted = self.broker.encrypt_value(plaintext)
        decrypted = self.broker.decrypt_value(encrypted)
        self.assertEqual(plaintext, decrypted)

        # Verify that changing salt breaks decryption
        decrypted_wrong = self.broker.decrypt_value(encrypted, salt=b"wrong-salt")
        self.assertNotEqual(plaintext, decrypted_wrong)

    def test_rbac_loading(self):
        """Verify RBAC loading from file."""
        rbac_data = {
            "agents": {"AdminAgent": "admin", "TestAgent": "pro_agent", "BasicAgent": "worker"},
            "default_role": "worker",
        }
        with open(self.test_rbac, "w") as f:
            yaml.dump(rbac_data, f)

        # Mocking canonical path by creating it in a temp location if needed,
        # but here we test the check_permission logic with direct path simulation if possible.
        # However, check_permission hardcodes the paths. I'll mock os.path.exists.

        from unittest.mock import patch

        with patch("os.path.exists") as mock_exists:

            def side_effect(path):
                if "rbac.yaml" in path or "rbac_policy.yaml" in path:
                    return True
                return False

            mock_exists.side_effect = side_effect

            with patch("builtins.open", unittest.mock.mock_open(read_data=yaml.dump(rbac_data))):
                # Admin always has access
                self.assertTrue(self.broker.check_permission("AdminAgent", "openai", "pro"))

                # Pro agent has access to pro tier
                self.assertTrue(self.broker.check_permission("TestAgent", "openai", "pro"))

                # Worker DOES NOT have access to pro tier
                self.assertFalse(self.broker.check_permission("BasicAgent", "openai", "pro"))

                # Worker HAS access to standard tier
                self.assertTrue(self.broker.check_permission("BasicAgent", "openai", "standard"))


if __name__ == "__main__":
    unittest.main()
