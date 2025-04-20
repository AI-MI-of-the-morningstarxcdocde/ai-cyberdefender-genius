import os
import platform
from datetime import datetime, timezone
import socket
import threading
import time
import logging
from core.update_manager import UpdateManager
from core.self_healing_manager import SelfHealingManager

class AutoFileManager:
    def __init__(self, base_dir, update_manager: UpdateManager = None, self_healing_manager: SelfHealingManager = None):
        self.base_dir = base_dir
        self.log_file = os.path.join(self.base_dir, 'logs', 'daily_activity.log')
        os.makedirs(os.path.dirname(self.log_file), exist_ok=True)
        self.env_info_file = os.path.join(self.base_dir, 'logs', 'environment_info.log')
        self.os_name = platform.system()
        self.os_version = platform.version()
        self.update_manager = update_manager
        self.self_healing_manager = self_healing_manager
        self.running = False

    def start(self):
        self.running = True
        threading.Thread(target=self.auto_update_loop, daemon=True).start()

    def stop(self):
        self.running = False

    def auto_update_loop(self):
        while self.running:
            try:
                if self.update_manager:
                    self.update_manager.perform_updates()
                time.sleep(3600)  # Check for updates every hour
            except Exception as e:
                logging.error(f"AutoFileManager auto-update error: {e}")

    def log_daily_activity(self, activity):
        # Use timezone-aware datetime for UTC now
        timestamp = datetime.now(timezone.utc).isoformat()
        log_entry = f"{timestamp} - {activity} (OS: {self.os_name} {self.os_version})\n"
        with open(self.log_file, 'a') as f:
            f.write(log_entry)

    def log_environment_info(self):
        """
        Automatically log environment information such as OS, hostname, IP address, and Python version.
        """
        info = {
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'os': self.os_name,
            'os_version': self.os_version,
            'hostname': socket.gethostname(),
            'ip_address': socket.gethostbyname(socket.gethostname()),
            'python_version': platform.python_version(),
        }
        with open(self.env_info_file, 'a') as f:
            f.write(str(info) + '\n')

    def get_os_info(self):
        """
        Return a user-friendly string describing the OS.
        """
        return f"{self.os_name} version {self.os_version}"

    def explain_os_protection(self):
        """
        Provide a simple explanation to the user about how this system protects their OS.
        """
        explanation = (
            f"This AI-CyberDefender system is designed to protect your {self.get_os_info()} environment. "
            "It monitors system activities, detects threats, and responds automatically to keep your system safe."
        )
        return explanation
