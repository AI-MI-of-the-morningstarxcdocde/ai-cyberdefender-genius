#!/bin/bash
# Build and deployment automation script for AI-CyberDefender-GUI
# This script obfuscates the source code, packages the app with PyInstaller,
# and prepares a signed executable for distribution.

# Step 1: Obfuscate source code using pyarmor
echo "Starting code obfuscation..."
./obfuscate.sh

# Step 2: Package the obfuscated code with PyInstaller
echo "Packaging application with PyInstaller..."
pyinstaller --clean --onefile --windowed --name AI-CyberDefender-GUI ai-cyberdefender-gui/dist_obfuscated/main.py

# Step 3: Code signing (placeholder)
echo "Code signing step - please sign the executable manually or integrate your signing tool here."

# Step 4: Cleanup
echo "Cleaning up build artifacts..."
rm -rf build __pycache__ ai-cyberdefender-gui.spec

echo "Build and deployment process completed."
