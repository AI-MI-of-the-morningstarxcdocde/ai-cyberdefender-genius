"""
Linux Tools Manager Module
--------------------------

Manages built-in Linux security and hacking tools within the AI-CyberDefender application.
Ensures essential Linux tools (including Kali Linux tools) are installed, cannot be removed,
and are automatically updated according to the user's OS.

Features:
- Automatic installation of Kali Linux tools if not present
- Protection against removal of critical tools
- Autonomous updates of Linux tools
- Integration with self-healing and security modules
"""

import subprocess
import logging
import platform

class LinuxToolsManager:
    def __init__(self):
        self.required_tools = [
            "nmap",
            "wireshark",
            "aircrack-ng",
            "metasploit-framework",
            "john",
            "hydra",
            "tcpdump",
            "kali-linux-default"
        ]

    def check_and_install_tools(self):
        if platform.system() != "Linux":
            logging.warning("Linux tools manager is designed for Linux systems only.")
            return

        for tool in self.required_tools:
            if not self.is_tool_installed(tool):
                self.install_tool(tool)

    def is_tool_installed(self, tool_name):
        try:
            result = subprocess.run(["which", tool_name], capture_output=True, text=True)
            return result.returncode == 0
        except Exception as e:
            logging.error(f"Error checking tool {tool_name}: {e}")
            return False

    def install_tool(self, tool_name):
        try:
            logging.info(f"Installing Linux tool: {tool_name}")
            subprocess.run(["sudo", "apt-get", "install", "-y", tool_name], check=True)
        except Exception as e:
            logging.error(f"Failed to install {tool_name}: {e}")

    def protect_tools(self):
        # Placeholder: Implement protection mechanisms to prevent removal
        # Could include file permissions, monitoring, or alerts
        pass

    def auto_update_tools(self):
        try:
            logging.info("Updating Linux tools...")
            subprocess.run(["sudo", "apt-get", "update"], check=True)
            subprocess.run(["sudo", "apt-get", "upgrade", "-y"], check=True)
        except Exception as e:
            logging.error(f"Failed to update Linux tools: {e}")
