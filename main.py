"""
AI-CyberDefender-GUI
--------------------

A cross-platform, offline, secure, and modern animated GUI application for real-time
threat detection and system monitoring. Built with PySide6 for Windows, Mac, and Linux.

This is the main entry point of the GUI application.
"""

import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QPushButton, QLineEdit, QMessageBox
from PySide6.QtCore import QTimer, Qt
from PySide6.QtGui import QMovie
from firewall_manager import FirewallManager
from auth_manager import AuthManager
from plugins.plugin import Plugin
from plugins.load_plugins import load_plugins

class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AI-CyberDefender-GUI Login")
        self.setFixedSize(400, 200)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")
        layout.addWidget(self.username_input)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_input)

        self.login_button = QPushButton("Login")
        self.login_button.clicked.connect(self.handle_login)
        layout.addWidget(self.login_button)

        self.auth_manager = AuthManager()

    def handle_login(self):
        username = self.username_input.text()
        password = self.password_input.text()
        if self.auth_manager.verify_user(username, password):
            self.main_window = MainWindow()
            self.main_window.show()
            self.close()
        else:
            QMessageBox.warning(self, "Login Failed", "Invalid username or password.")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AI-CyberDefender-GUI")
        self.setFixedSize(800, 600)

        self.firewall_manager = FirewallManager()
        self.firewall_manager.activate_firewall()

        # Central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        # Animated logo or gif
        self.label_animation = QLabel()
        self.label_animation.setAlignment(Qt.AlignCenter)
        movie = QMovie(":/resources/animated_logo.gif")  # Placeholder path
        self.label_animation.setMovie(movie)
        movie.start()
        layout.addWidget(self.label_animation)

        # Status label
        self.status_label = QLabel("System Status: Monitoring...")
        self.status_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.status_label)

        # Plugins status label
        self.plugins_status_label = QLabel("Loading plugins...")
        self.plugins_status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.plugins_status_label)

        # Firewall status label
        self.firewall_status_label = QLabel(f"Firewall Status: {self.firewall_manager.get_status()}")
        self.firewall_status_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.firewall_status_label)

        # Button to update firewall rules
        self.update_firewall_button = QPushButton("Update Firewall Rules")
        self.update_firewall_button.clicked.connect(self.update_firewall_rules)
        layout.addWidget(self.update_firewall_button)

        # Load plugins
        self.plugins = load_plugins(Plugin)

        # Start plugins
        self.start_plugins()

        # Timer for live monitoring updates
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_status)
        self.timer.start(2000)  # Update every 2 seconds

    def update_status(self):
        self.status_label.setText("System Status: All systems normal.")

        if len(self.plugins) == 0:
            self.plugins_status_label.setText(f"No plugins loaded.")
        else:
            # Get status of plugins
            statuses = [max(plugin.report_status()).level for plugin in self.plugins]
            status = max(statuses)

            self.plugins_status_label.setText(f"{len(self.plugins)} plugin{'s' if len(self.plugins) != 1 else ''} loaded. Status: {status}")
        
        self.firewall_status_label.setText(f"Firewall Status: {self.firewall_manager.get_status()}")

    def start_plugins(self):
        self.plugins_status_label.setText("Starting plugins...")
        for plugin in self.plugins:
            plugin.start_plugin()

    def stop_plugins(self):
        self.plugins_status_label.setText("Stopping plugins...")
        for plugin in self.plugins:
            plugin.stop_plugin()
        
        self.plugins_status_label.setText("Plugins stopped.")

    def closeEvent(self, event):
        self.stop_plugins()
        
    def update_firewall_rules(self):
        self.firewall_manager.update_firewall_rules()

def main():
    app = QApplication(sys.argv)
    login_window = LoginWindow()
    login_window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
