#!/bin/bash
# Quantum Networking Simulation - Mac Installer Launcher
# Simple one-command installer for Mac

echo "========================================================================"
echo "  QUANTUM NETWORKING SIMULATION - MAC INSTALLER"
echo "========================================================================"
echo ""
echo "This will install Python, Node.js, and Docker Desktop on your Mac."
echo ""
echo "Starting installer..."
echo ""
sleep 2

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Change to script directory
cd "$SCRIPT_DIR"

# Make the main installer executable
chmod +x auto_installer_mac.sh

# Run the installer
./auto_installer_mac.sh

echo ""
echo "========================================================================"
echo "  INSTALLATION COMPLETED"
echo "========================================================================"
echo ""
echo "Press any key to close..."
read -n 1 -s

