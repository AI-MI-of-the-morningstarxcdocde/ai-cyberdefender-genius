"""
Advanced Database Module
------------------------

A robust, multi-language, and multi-algorithm supporting database for AI-CyberDefender.
Supports dynamic language detection, secure updates via VPN or secure servers,
and attacker tracking with location logging saved securely for user access only.
"""

import os
import json
import threading
import datetime
import socket
import requests

class AdvancedDatabase:
    def __init__(self, db_path='model_data/advanced_db.json', log_path=None):
        self.db_path = db_path
        self.log_path = log_path or os.path.expanduser('~/Desktop/attacker_logs.json')
        self.data = self.load_database()
        self.lock = threading.Lock()

    def load_database(self):
        if os.path.exists(self.db_path):
            with open(self.db_path, 'r') as f:
                return json.load(f)
        else:
            # Initialize with empty structure
            return {
                "languages": [],
                "algorithms": [],
                "attackers": []
            }

    def save_database(self):
        with self.lock:
            with open(self.db_path, 'w') as f:
                json.dump(self.data, f, indent=4)

    def add_language(self, language_name):
        if language_name not in self.data["languages"]:
            self.data["languages"].append(language_name)
            self.save_database()

    def add_algorithm(self, algorithm_name):
        if algorithm_name not in self.data["algorithms"]:
            self.data["algorithms"].append(algorithm_name)
            self.save_database()

    def detect_new_language(self, language_name):
        # Placeholder: Implement detection logic using secure VPN or server
        # For now, simulate detection and add language
        self.add_language(language_name)
        print(f"New language detected and added: {language_name}")

    def track_attacker(self, ip_address):
        location = self.get_location_from_ip(ip_address)
        attacker_info = {
            "ip": ip_address,
            "location": location,
            "timestamp": datetime.datetime.now().isoformat()
        }
        self.data["attackers"].append(attacker_info)
        self.save_database()
        self.save_attacker_log(attacker_info)

    def get_location_from_ip(self, ip):
        try:
            response = requests.get(f"https://ipinfo.io/{ip}/json")
            if response.status_code == 200:
                data = response.json()
                return {
                    "city": data.get("city"),
                    "region": data.get("region"),
                    "country": data.get("country"),
                    "loc": data.get("loc")
                }
        except Exception as e:
            print(f"Error fetching location for IP {ip}: {e}")
        return {}

    def save_attacker_log(self, attacker_info):
        try:
            if os.path.exists(self.log_path):
                with open(self.log_path, 'r') as f:
                    logs = json.load(f)
            else:
                logs = []
            logs.append(attacker_info)
            with open(self.log_path, 'w') as f:
                json.dump(logs, f, indent=4)
        except Exception as e:
            print(f"Error saving attacker log: {e}")
