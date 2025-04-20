import unittest
from ai_cyberdefender_genius.core.auto_attacker import AutoAttacker
from ai_cyberdefender_genius.core.auto_efficiency_manager import AutoEfficiencyManager
from ai_cyberdefender_genius.core.auto_file_manager import AutoFileManager
from ai_cyberdefender_genius.core.auto_universal_manager import AutoUniversalManager
from ai_cyberdefender_genius.core.user_friendly_protector import UserFriendlyProtector

class TestCoreModules(unittest.TestCase):

    def test_auto_attacker_reconnaissance(self):
        attacker = AutoAttacker()
        result = attacker.reconnaissance("127.0.0.1")
        self.assertIsInstance(result, (str, type(None)))

    def test_auto_efficiency_manager_start_stop(self):
        manager = AutoEfficiencyManager(base_dir=".")
        manager.start()
        self.assertTrue(manager.running)
        manager.stop()
        self.assertFalse(manager.running)

    def test_auto_file_manager_log_daily_activity(self):
        manager = AutoFileManager(base_dir=".")
        try:
            manager.log_daily_activity("Test activity")
        except Exception as e:
            self.fail(f"log_daily_activity raised Exception unexpectedly: {e}")

    def test_auto_universal_manager_load_config(self):
        manager = AutoUniversalManager()
        manager.load_environment_config()
        self.assertIn("os", manager.env_config)
        self.assertIn("device", manager.env_config)

    def test_user_friendly_protector_enforce_admin_access(self):
        protector = UserFriendlyProtector(base_dir=".", admin_fingerprint="admin123")
        self.assertTrue(protector.enforce_admin_access("admin123"))
        self.assertFalse(protector.enforce_admin_access("wrongfingerprint"))

if __name__ == "__main__":
    unittest.main()
