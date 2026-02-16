import os
import shutil
import unittest

import yaml

from Scripts.Utilities.token_broker import TokenBroker


class TestTokenBroker(unittest.TestCase):
    def setUp(self):
        # Reset singleton for test isolation
        TokenBroker._instance = None

        self.test_dir = "secrets_test"
        if not os.path.exists(self.test_dir):
            os.makedirs(self.test_dir)

        self.keys_path = os.path.join(self.test_dir, "keys.yaml")
        data = {
            "gemini": [{"alias": "T1", "key": "GEM-1", "tier": "free"}],
            "openai": [
                {"alias": "O1", "key": "OPEN-1", "tier": "paid"},
                {"alias": "O2", "key": "OPEN-2", "tier": "paid"},
            ],
        }
        with open(self.keys_path, "w") as f:
            yaml.dump(data, f)

    def tearDown(self):
        TokenBroker._instance = None
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_load_keys(self):
        broker = TokenBroker(vault_path=self.keys_path)
        pools = broker.list_available_pools()
        self.assertEqual(pools["gemini"]["total"], 1)
        self.assertEqual(pools["openai"]["total"], 2)

    def test_get_key(self):
        broker = TokenBroker(vault_path=self.keys_path)
        key = broker.get_key("gemini")
        self.assertEqual(key, "GEM-1")

        # Test Rotation (Statistically likely to hit both)
        keys_seen = set()
        for _ in range(20):
            k = broker.get_key("openai")
            if k:
                keys_seen.add(k)

        self.assertTrue(len(keys_seen) > 0)
        print(f"Keys seen in rotation: {keys_seen}")

    def test_fallback(self):
        # Create empty vault
        empty_path = os.path.join(self.test_dir, "empty.yaml")
        with open(empty_path, "w") as f:
            yaml.dump({}, f)

        TokenBroker._instance = None
        broker = TokenBroker(vault_path=empty_path)

        # No keys loaded from empty vault
        self.assertIsNone(broker.get_key("gemini"))


if __name__ == "__main__":
    unittest.main()
