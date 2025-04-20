#!/bin/bash
# Installation script for AI-CyberDefender-Genius

echo "Updating package lists..."
sudo apt-get update

echo "Installing Python3 and pip..."
sudo apt-get install -y python3 python3-pip

echo "Installing required Python packages..."
pip3 install -r requirements.txt

echo "Installation complete."
