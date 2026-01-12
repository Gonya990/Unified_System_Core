
import json
import logging
import os
import unittest

from token_broker import TokenBroker

# Configure logging
logging.basicConfig(level=logging.INFO)

class TestTokenBroker(unittest.TestCase):

    def setUp(self):
        # Create a dummy keys.json
        self.test_keys_path = "test_keys_vault.json"

        self.dummy_data = {
            "gemini": [
                {"alias": "Key_A", "key": "gemini-key-A", "tier": "free", "owner": "UserA"},
                {"alias": "Key_B", "key": "gemini-key-B", "tier": "free", "owner": "UserB"},
                {"alias": "Key_C", "key": "gemini-key-C", "tier": "pro", "owner": "UserC"}
            ]
        }

        with open(self.test_keys_path, 'w') as f:
            json.dump(self.dummy_data, f)

        # Initialize Broker
        # Reset singleton instance for testing provided we can (hacky but needed for unit test isolation)
        TokenBroker._instance = None
        self.broker = TokenBroker(secrets_path=self.test_keys_path)

    def tearDown(self):
        if os.path.exists(self.test_keys_path):
            os.remove(self.test_keys_path)

    def test_load_keys(self):
        pools = self.broker.list_available_pools()
        self.assertEqual(pools['gemini']['total'], 3)
        print("\n[Test] Keys loaded successfully.")

    def test_round_robin(self):
        print("\n[Test] Testing Round-Robin Rotation...")
        # Expect A -> B -> A -> B (Tier free)
        k1 = self.broker.get_key("gemini", tier="free")
        print(f"1. Got: {k1}")
        self.assertEqual(k1, "gemini-key-A")

        k2 = self.broker.get_key("gemini", tier="free")
        print(f"2. Got: {k2}")
        self.assertEqual(k2, "gemini-key-B")

        k3 = self.broker.get_key("gemini", tier="free")
        print(f"3. Got: {k3}")
        self.assertEqual(k3, "gemini-key-A")

    def test_blacklist_logic(self):
        print("\n[Test] Testing Failure Blacklist...")
        # Fail Key A
        self.broker.report_failure("gemini-key-A", "gemini")

        # Next call should skip A and give B
        k = self.broker.get_key("gemini", tier="free")
        print(f"After failure, Got: {k}")
        self.assertEqual(k, "gemini-key-B")

        # Next call should still give B because A is on cooldown
        k_next = self.broker.get_key("gemini", tier="free")
        print(f"Next call, Got: {k_next}")
        self.assertEqual(k_next, "gemini-key-B")

    def test_tier_filtering(self):
        print("\n[Test] Testing Tier Filtering...")
        k_pro = self.broker.get_key("gemini", tier="pro")
        self.assertEqual(k_pro, "gemini-key-C")

if __name__ == '__main__':
    unittest.main()
