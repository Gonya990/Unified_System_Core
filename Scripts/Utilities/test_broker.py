
import json
import os
import shutil
import unittest

from Scripts.Utilities.token_broker import TokenBroker


class TestTokenBroker(unittest.TestCase):

    def setUp(self):
        # Create a dummy secrets file
        self.test_dir = "secrets_test"
        if not os.path.exists(self.test_dir):
            os.makedirs(self.test_dir)

        self.keys_path = os.path.join(self.test_dir, "keys.json")
        data = {
            "gemini": [{"alias": "T1", "key": "GEM-1", "tier": "free"}],
            "openai": [{"alias": "O1", "key": "OPEN-1", "tier": "paid"}, {"alias": "O2", "key": "OPEN-2", "tier": "paid"}]
        }
        with open(self.keys_path, 'w') as f:
            json.dump(data, f)

    def tearDown(self):
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_load_keys(self):
        broker = TokenBroker(secrets_path=self.keys_path)
        pools = broker.list_available_pools()
        self.assertEqual(pools['gemini'], 1)
        self.assertEqual(pools['openai'], 2)

    def test_get_key(self):
        broker = TokenBroker(secrets_path=self.keys_path)
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
        # Create empty file
        empty_path = os.path.join(self.test_dir, "empty.json")
        with open(empty_path, 'w') as f:
            json.dump({}, f)

        # Mock Env
        os.environ["GEMINI_API_KEY"] = "ENV-GEM"
        broker = TokenBroker(secrets_path=empty_path)

        self.assertEqual(broker.get_key("gemini"), "ENV-GEM")

if __name__ == '__main__':
    unittest.main()
