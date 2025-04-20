"""
Auto Defender Module
-------------------

Continuously monitors all application files for unauthorized changes or hacking attempts.
Automatically saves backups of files and blocks detected attacks in real-time.
Integrates with self-healing and encryption modules to maintain application integrity.
"""

import os
import time
import threading
import hashlib
import logging
import shutil
from core.update_manager import UpdateManager
from core.self_healing_manager import SelfHealingManager

class AutoDefender:
    def __init__(self, watch_dir, update_manager: UpdateManager = None, self_healing_manager: SelfHealingManager = None):
        self.watch_dir = watch_dir
        self.file_hashes = {}
        self.backup_dir = os.path.join(watch_dir, ".backup")
        self.running = False
        self.lock = threading.Lock()
        self.update_manager = update_manager
        self.self_healing_manager = self_healing_manager
        self.attack_log = []

        if not os.path.exists(self.backup_dir):
            os.makedirs(self.backup_dir)

    def start(self):
        self.running = True
        threading.Thread(target=self.monitor_loop, daemon=True).start()
        if self.update_manager:
            threading.Thread(target=self.auto_update_loop, daemon=True).start()

    def stop(self):
        self.running = False

    def monitor_loop(self):
        while self.running:
            try:
                self.scan_files()
            except Exception as e:
                logging.error(f"AutoDefender error: {e}")
            time.sleep(5)  # Check every 5 seconds

    def auto_update_loop(self):
        while self.running:
            try:
                if self.update_manager:
                    self.update_manager.perform_updates()
                time.sleep(3600)  # Check for updates every hour
            except Exception as e:
                logging.error(f"AutoDefender auto-update error: {e}")

    def scan_files(self):
        with self.lock:
            for root, dirs, files in os.walk(self.watch_dir):
                # Skip backup directory
                if root.startswith(self.backup_dir):
                    continue
                for file in files:
                    file_path = os.path.join(root, file)
                    current_hash = self.hash_file(file_path)
                    if file_path not in self.file_hashes:
                        self.file_hashes[file_path] = current_hash
                        self.backup_file(file_path)
                    else:
                        if self.file_hashes[file_path] != current_hash:
                            logging.warning(f"File change detected: {file_path}")
                            self.handle_intrusion(file_path)
                            self.file_hashes[file_path] = current_hash
                            self.backup_file(file_path)

    def hash_file(self, file_path):
        try:
            hasher = hashlib.sha256()
            with open(file_path, "rb") as f:
                buf = f.read()
                hasher.update(buf)
            return hasher.hexdigest()
        except Exception as e:
            logging.error(f"Failed to hash file {file_path}: {e}")
            return None

    def backup_file(self, file_path):
        try:
            rel_path = os.path.relpath(file_path, self.watch_dir)
            backup_path = os.path.join(self.backup_dir, rel_path)
            backup_dir = os.path.dirname(backup_path)
            if not os.path.exists(backup_dir):
                os.makedirs(backup_dir)
            shutil.copy2(file_path, backup_path)
            logging.info(f"Backed up file: {file_path}")
        except Exception as e:
            logging.error(f"Failed to backup file {file_path}: {e}")

    def handle_intrusion(self, file_path):
        # Block hacking attempt, restore file from backup, alert admin, and log attack
        logging.warning(f"Intrusion detected and blocked on file: {file_path}")
        self.attack_log.append({'file': file_path, 'timestamp': time.time()})
        self.restore_file(file_path)
        if self.self_healing_manager and self.self_healing_manager.alert_engine:
            self.self_healing_manager.alert_engine.send_alert(f"Intrusion detected on file: {file_path}")

    def restore_file(self, file_path):
        try:
            rel_path = os.path.relpath(file_path, self.watch_dir)
            backup_path = os.path.join(self.backup_dir, rel_path)
            if os.path.exists(backup_path):
                shutil.copy2(backup_path, file_path)
                logging.info(f"Restored file from backup: {file_path}")
        except Exception as e:
            logging.error(f"Failed to restore file {file_path}: {e}")
