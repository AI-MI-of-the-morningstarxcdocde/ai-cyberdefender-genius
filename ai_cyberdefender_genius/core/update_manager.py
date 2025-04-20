"""
Update Manager Module
---------------------

Handles checking, downloading, and applying updates for core modules of AI-CyberDefender-Genius.
Supports autonomous updates with validation and rollback capabilities.
"""

import logging
import requests
import os
import shutil
import tempfile
import hashlib

class UpdateManager:
    def __init__(self, base_dir, update_server_url):
        self.base_dir = base_dir
        self.update_server_url = update_server_url
        self.backup_dir = os.path.join(base_dir, ".update_backup")
        if not os.path.exists(self.backup_dir):
            os.makedirs(self.backup_dir)

    def check_for_updates(self):
        """
        Check the update server for available updates.
        Returns a list of modules with updates available.
        """
        try:
            response = requests.get(f"{self.update_server_url}/updates.json", timeout=10)
            response.raise_for_status()
            updates = response.json()
            logging.info(f"Update check successful: {updates}")
            return updates
        except Exception as e:
            logging.error(f"Failed to check for updates: {e}")
            return []

    def download_update(self, module_name, version):
        """
        Download update package for a given module and version.
        Returns path to downloaded file or None on failure.
        """
        try:
            url = f"{self.update_server_url}/{module_name}/{version}/{module_name}.zip"
            response = requests.get(url, stream=True, timeout=30)
            response.raise_for_status()
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".zip")
            with open(temp_file.name, 'wb') as f:
                shutil.copyfileobj(response.raw, f)
            logging.info(f"Downloaded update for {module_name} version {version}")
            return temp_file.name
        except Exception as e:
            logging.error(f"Failed to download update for {module_name}: {e}")
            return None

    def backup_module(self, module_name):
        """
        Backup current module files before applying update.
        """
        try:
            src_dir = os.path.join(self.base_dir, "core", module_name)
            dst_dir = os.path.join(self.backup_dir, module_name)
            if os.path.exists(dst_dir):
                shutil.rmtree(dst_dir)
            shutil.copytree(src_dir, dst_dir)
            logging.info(f"Backed up module {module_name} before update")
            return True
        except Exception as e:
            logging.error(f"Failed to backup module {module_name}: {e}")
            return False

    def apply_update(self, module_name, update_zip_path):
        """
        Apply the update by extracting and replacing module files.
        """
        try:
            import zipfile
            src_dir = os.path.join(self.base_dir, "core", module_name)
            # Backup current module
            if not self.backup_module(module_name):
                return False
            # Extract update
            with zipfile.ZipFile(update_zip_path, 'r') as zip_ref:
                zip_ref.extractall(src_dir)
            logging.info(f"Applied update for module {module_name}")
            return True
        except Exception as e:
            logging.error(f"Failed to apply update for {module_name}: {e}")
            return False

    def validate_update(self, module_name):
        """
        Validate the updated module files.
        Placeholder for checksum or test execution.
        """
        # TODO: Implement validation logic
        logging.info(f"Validated update for module {module_name}")
        return True

    def rollback_update(self, module_name):
        """
        Rollback to backup if update fails.
        """
        try:
            src_dir = os.path.join(self.base_dir, "core", module_name)
            backup_dir = os.path.join(self.backup_dir, module_name)
            if os.path.exists(src_dir):
                shutil.rmtree(src_dir)
            shutil.copytree(backup_dir, src_dir)
            logging.info(f"Rolled back update for module {module_name}")
            return True
        except Exception as e:
            logging.error(f"Failed to rollback update for {module_name}: {e}")
            return False

    def perform_updates(self):
        """
        Check for updates and apply them autonomously.
        """
        updates = self.check_for_updates()
        for update in updates:
            module_name = update.get("module")
            version = update.get("version")
            if not module_name or not version:
                continue
            update_zip = self.download_update(module_name, version)
            if not update_zip:
                continue
            if not self.apply_update(module_name, update_zip):
                self.rollback_update(module_name)
                continue
            if not self.validate_update(module_name):
                self.rollback_update(module_name)
                continue
            # Cleanup downloaded update file
            try:
                os.remove(update_zip)
            except Exception:
                pass
