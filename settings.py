from PySide6.QtWidgets import QMainWindow, QListWidget, QPushButton, QVBoxLayout, QWidget, QLabel, QLineEdit, QMessageBox
from PySide6.QtCore import Qt

from auth_manager import AuthManager, Session

class SettingsWindow(QMainWindow):
    def __init__(self, parent=None):
        super(SettingsWindow, self).__init__(parent)

        self.auth_manager = AuthManager()

        self.setWindowTitle("Settings")
        self.setGeometry(100, 100, 400, 300)

        layout = QVBoxLayout()
        central_widget = QWidget(self)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.list_widget = QListWidget()
        layout.addWidget(self.list_widget)

        # --- Change Password Section ---
        password_section = QVBoxLayout()
        password_label = QLabel("Change Password")
        password_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        password_section.addWidget(password_label)

        self.old_password_input = QLineEdit()
        self.old_password_input.setPlaceholderText("Old Password")
        self.old_password_input.setEchoMode(QLineEdit.EchoMode.Password)
        password_section.addWidget(self.old_password_input)

        self.new_password_input = QLineEdit()
        self.new_password_input.setPlaceholderText("New Password")
        self.new_password_input.setEchoMode(QLineEdit.EchoMode.Password)
        password_section.addWidget(self.new_password_input)

        self.change_password_button = QPushButton("Change Password")
        self.change_password_button.clicked.connect(self.change_password)
        password_section.addWidget(self.change_password_button)

        layout.addLayout(password_section)

    def change_password(self):
        session = Session()

        if not self.old_password_input.text() or not self.new_password_input.text():
            QMessageBox.warning(self, "Input Error", "Please fill in both fields.")
            return
        
        if not session.user:
            QMessageBox.warning(self, "Authentication Error", "You must be logged in to change your password.")
            return
        
        result = self.auth_manager.change_password(
            session.user,
            self.old_password_input.text(),
            self.new_password_input.text()
        )
        
        if result == "success":
            QMessageBox.information(self, "Success", "Password changed successfully.")
            self.old_password_input.clear()
            self.new_password_input.clear()
        else:
            error_messages = {
                "user_not_found": "User not found.",
                "wrong_password": "Old password is incorrect.",
                "insecure_password": "New password must be at least 8 characters long."
            }
            QMessageBox.warning(self, "Error", error_messages.get(result, "An unknown error occurred."))