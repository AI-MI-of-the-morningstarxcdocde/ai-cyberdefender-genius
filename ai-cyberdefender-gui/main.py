import sys
import threading
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget
from PySide6.QtCore import Qt, QTimer
from auth_manager import AuthManager
from firewall_manager import FirewallManager
from ai_cyberdefender_genius.core.self_healing_manager import SelfHealingManager

class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AI-CyberDefender-GUI")
        self.setGeometry(100, 100, 800, 600)

        self.auth_manager = AuthManager()
        self.firewall_manager = FirewallManager()
        self.self_healing_manager = SelfHealingManager(update_manager=None, secure_network=None, alert_engine=None)

        self.monitoring_active = True
        self.app_active = False

        self.init_ui()
        self.init_timers()

        # Start self-healing manager monitoring in background
        self.self_healing_manager.start()

    def init_ui(self):
        self.status_label = QLabel("Application is inactive. Press any alphabet key 5 times to activate.", self)
        self.status_label.setAlignment(Qt.AlignCenter)

        central_widget = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(self.status_label)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.key_press_count = 0
        self.last_key = None

    def init_timers(self):
        self.monitor_timer = QTimer()
        self.monitor_timer.timeout.connect(self.monitor_threats)
        self.monitor_timer.start(5000)  # Check every 5 seconds

    def keyPressEvent(self, event):
        if event.text().isalpha():
            if self.last_key == event.text():
                self.key_press_count += 1
            else:
                self.key_press_count = 1
                self.last_key = event.text()

            if self.key_press_count == 5:
                if not self.app_active:
                    self.activate_app()
                else:
                    self.deactivate_app()
                self.key_press_count = 0

    def activate_app(self):
        self.app_active = True
        self.status_label.setText("Application Activated. Monitoring threats...")

    def deactivate_app(self):
        if not self.detect_active_threats():
            self.app_active = False
            self.status_label.setText("Application Deactivated. Press any alphabet key 5 times to activate.")
        else:
            self.status_label.setText("Threats detected! Cannot deactivate. Monitoring continues.")

    def monitor_threats(self):
        if self.monitoring_active:
            threats_found = self.detect_active_threats()
            if threats_found:
                self.status_label.setText("Threats detected! Monitoring and defense active.")
                if not self.app_active:
                    self.app_active = True
                    self.status_label.setText("Threats detected! Application auto-activated for defense.")
            else:
                if self.app_active:
                    self.status_label.setText("No threats detected. Monitoring active.")

            external_threat = self.check_external_devices()
            if external_threat:
                self.notify_user_external_threat(external_threat)

            apk_attempt = self.check_new_apk_installation()
            if apk_attempt:
                self.handle_apk_installation(apk_attempt)

    def check_new_apk_installation(self):
        import random
        if random.choice([False, False, False, True]):
            return {
                "apk_name": "SuspiciousApp.apk",
                "reason": "Unknown source or unsafe permissions"
            }
        return None

    def handle_apk_installation(self, apk_info):
        message = (
            f"Security Alert: You are attempting to install '{apk_info['apk_name']}'.\n"
            "This app is from an untrusted source and may be unsafe.\n"
            "Please choose to Install or Cancel installation.\n"
            "If installed, the system will monitor it closely and quarantine if threats are detected."
        )
        self.status_label.setText(message)

        user_choice = self.simulate_user_choice()
        if user_choice == "Install":
            self.status_label.setText(f"'{apk_info['apk_name']}' installed. Monitoring for threats.")
            self.monitor_apk(apk_info['apk_name'])
        else:
            self.status_label.setText(f"Installation of '{apk_info['apk_name']}' cancelled.")

    def simulate_user_choice(self):
        import random
        return random.choice(["Install", "Cancel"])

    def monitor_apk(self, apk_name):
        pass

    def detect_active_threats(self):
        return False

def main():
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
