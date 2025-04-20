"""
Authentication Manager Module
-----------------------------

Handles user authentication to ensure that only the authorized owner can access
the AI-CyberDefender-GUI application. Provides login functionality and session management.
"""

import hashlib
import json
import os

class AuthManager:
    def __init__(self, credentials_file='credentials.json'):
        self.credentials_file = credentials_file
        self.users = self.load_credentials()

    def load_credentials(self):
        if os.path.exists(self.credentials_file):
            with open(self.credentials_file, 'r') as f:
                return json.load(f)
        else:
            # Create default admin user with password 'admin'
            default_user = {
                "admin": self.hash_password("admin")
            }
            with open(self.credentials_file, 'w') as f:
                json.dump(default_user, f)
            return default_user

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def verify_user(self, username, password):
        hashed = self.hash_password(password)
        return self.users.get(username) == hashed

    def add_user(self, username, password):
        self.users[username] = self.hash_password(password)
        with open(self.credentials_file, 'w') as f:
            json.dump(self.users, f)
