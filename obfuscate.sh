#!/bin/bash
# Obfuscation script for AI-CyberDefender-GUI Python source code
# Uses pyarmor to obfuscate the source files for code protection

# Check if pyarmor is installed
if ! command -v pyarmor &> /dev/null
then
    echo "pyarmor could not be found, installing..."
    pip install pyarmor
fi

# Define source and output directories
SRC_DIR="."
DIST_DIR="dist_obfuscated"

# Remove previous obfuscated output if exists
rm -rf $DIST_DIR

# Obfuscate the source code
pyarmor obfuscate --output $DIST_DIR main.py auth_manager.py firewall_manager.py

echo "Obfuscation complete. Obfuscated files are in the $DIST_DIR directory."
