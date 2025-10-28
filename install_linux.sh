#!/bin/bash
# Quantum Networking Simulation - Linux Installer Launcher
# Simple one-command installer for Linux

echo "========================================================================"
echo "  QUANTUM NETWORKING SIMULATION - LINUX INSTALLER"
echo "========================================================================"
echo ""
echo "This will install Python, Node.js, and Docker on your Linux system."
echo "You need sudo privileges to continue."
echo ""
echo "Starting installer..."
echo ""
sleep 2

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Change to script directory
cd "$SCRIPT_DIR"

# Make the main installer executable
chmod +x auto_installer_linux.sh

# Check if running with sudo
if [ "$EUID" -ne 0 ]; then
    echo "Requesting sudo privileges..."
    sudo "$SCRIPT_DIR/auto_installer_linux.sh"
else
    ./auto_installer_linux.sh
fi

echo ""
echo "========================================================================"
echo "  INSTALLATION COMPLETED"
echo "========================================================================"
echo ""
echo "Press any key to close..."
read -n 1 -s

