from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QPushButton, QHBoxLayout, QListWidget, QTextEdit
from PySide6.QtCore import Qt
import sys

class DashboardApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AI-CyberDefender-Genius Dashboard")
        self.setGeometry(100, 100, 1000, 700)
        self.init_ui()

    def init_ui(self):
        main_widget = QWidget()
        main_layout = QVBoxLayout()

        header = QLabel("AI-CyberDefender-Genius Dashboard")
        header.setAlignment(Qt.AlignCenter)
        header.setStyleSheet("font-size: 28px; font-weight: bold; color: #2c3e50; margin: 20px;")

        self.status_label = QLabel("System Status: Secure")
        self.status_label.setStyleSheet("font-size: 18px; color: #27ae60; margin-bottom: 10px;")

        self.alerts_list = QListWidget()
        self.alerts_list.setStyleSheet("""
            background-color: #ecf0f1;
            border: 1px solid #bdc3c7;
            font-size: 16px;
            padding: 10px;
        """)

        self.details_text = QTextEdit()
        self.details_text.setReadOnly(True)
        self.details_text.setStyleSheet("""
            background-color: #ffffff;
            border: 1px solid #bdc3c7;
            font-size: 14px;
            padding: 10px;
        """)

        buttons_layout = QHBoxLayout()
        refresh_button = QPushButton("Refresh Status")
        refresh_button.setStyleSheet("background-color: #2980b9; color: white; font-size: 16px; padding: 10px;")
        refresh_button.clicked.connect(self.refresh_status)

        clear_alerts_button = QPushButton("Clear Alerts")
        clear_alerts_button.setStyleSheet("background-color: #c0392b; color: white; font-size: 16px; padding: 10px;")
        clear_alerts_button.clicked.connect(self.clear_alerts)

        buttons_layout.addWidget(refresh_button)
        buttons_layout.addWidget(clear_alerts_button)

        main_layout.addWidget(header)
        main_layout.addWidget(self.status_label)
        main_layout.addWidget(self.alerts_list)
        main_layout.addWidget(self.details_text)
        main_layout.addLayout(buttons_layout)

        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

        # Load initial data
        self.load_alerts()

    def load_alerts(self):
        # Placeholder: Load alerts from logs or database
        sample_alerts = [
            "USB Device XYZ connected - Potential malware detected",
            "Suspicious APK installation attempt blocked",
            "Network performance degraded - Auto repair initiated",
            "Self-healing module updated successfully"
        ]
        self.alerts_list.addItems(sample_alerts)

    def refresh_status(self):
        # Placeholder: Refresh system status
        self.status_label.setText("System Status: Secure (Last checked just now)")
        self.details_text.setText("All systems operational. No active threats detected.")

    def clear_alerts(self):
        self.alerts_list.clear()
        self.details_text.clear()

def main():
    app = QApplication(sys.argv)
    window = DashboardApp()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
