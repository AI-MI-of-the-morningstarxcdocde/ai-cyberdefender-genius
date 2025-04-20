import unittest
import sys
import os
from PySide6.QtWidgets import QApplication

# Add parent directory to sys.path to import main.py
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from main import MainApp

app = QApplication(sys.argv)

class TestMainApp(unittest.TestCase):
    def setUp(self):
        self.main_app = MainApp()

    def test_activate_app(self):
        self.main_app.app_active = False
        self.main_app.activate_app()
        self.assertTrue(self.main_app.app_active)
        self.assertEqual(self.main_app.status_label.text(), "Application Activated. Monitoring threats...")

    def test_deactivate_app_no_threats(self):
        self.main_app.app_active = True
        self.main_app.detect_active_threats = lambda: False
        self.main_app.deactivate_app()
        self.assertFalse(self.main_app.app_active)
        self.assertEqual(self.main_app.status_label.text(), "Application Deactivated. Press any alphabet key 5 times to activate.")

    def test_deactivate_app_with_threats(self):
        self.main_app.app_active = True
        self.main_app.detect_active_threats = lambda: True
        self.main_app.deactivate_app()
        self.assertTrue(self.main_app.app_active)
        self.assertEqual(self.main_app.status_label.text(), "Threats detected! Cannot deactivate. Monitoring continues.")

    def test_monitor_threats_no_threats(self):
        self.main_app.app_active = True
        self.main_app.monitoring_active = True
        self.main_app.detect_active_threats = lambda: False
        self.main_app.status_label.setText("")
        self.main_app.monitor_threats()
        self.assertEqual(self.main_app.status_label.text(), "No threats detected. Monitoring active.")

    def test_monitor_threats_with_threats(self):
        self.main_app.app_active = False
        self.main_app.monitoring_active = True
        self.main_app.detect_active_threats = lambda: True
        self.main_app.status_label.setText("")
        self.main_app.monitor_threats()
        self.assertEqual(self.main_app.status_label.text(), "Threats detected! Application auto-activated for defense.")
        self.assertTrue(self.main_app.app_active)

if __name__ == "__main__":
    unittest.main()
