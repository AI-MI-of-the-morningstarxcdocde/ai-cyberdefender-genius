"""
Authentication Manager Module
-----------------------------

Handles user authentication to ensure that only the authorized owner can access
the AI-CyberDefender-GUI application. Provides login functionality and session management.
"""

import hashlib
import json
import os
from typing import Optional

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
    
    def change_password(self, username: str, old_password: str, new_password: str) -> str:
        if username not in self.users:
            return "user_not_found"
        if self.hash_password(old_password) != self.users[username]:
            return "wrong_password"
        if len(new_password) < 8: # TODO: Implement more secure password validation
            return "insecure_password"
        self.users[username] = self.hash_password(new_password)
        with open(self.credentials_file, 'w') as f:
            json.dump(self.users, f)
        return "success"

class Session:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Session, cls).__new__(cls)
            cls._instance.user = None
        return cls._instance

    def set_user(self, username):
        self.user: Optional[str] = username

    def get_user(self):
        return self.user

    # Usage:
    # from session import Session
    # session = Session()
    # session.set_user("admin")
    # print(session.get_user())