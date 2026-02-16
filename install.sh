#!/bin/bash

# Eye Saver Installation Script
# This script installs and configures the Eye Saver service

set -e

echo "========================================="
echo "  Eye Saver Installation Script"
echo "========================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
SERVICE_FILE="$SCRIPT_DIR/eye-saver.service"
PYTHON_SCRIPT="$SCRIPT_DIR/eye_saver.py"

# Check if running on Linux
if [[ "$OSTYPE" != "linux-gnu"* ]]; then
    echo -e "${RED}Error: This script is designed for Linux systems.${NC}"
    exit 1
fi

# Check if notify-send is available
if ! command -v notify-send &> /dev/null; then
    echo -e "${YELLOW}Warning: notify-send not found.${NC}"
    echo "Installing libnotify-bin..."
    sudo apt-get update
    sudo apt-get install -y libnotify-bin
fi

# Make the Python script executable
echo -e "${GREEN}Making Python script executable...${NC}"
chmod +x "$PYTHON_SCRIPT"

# Create systemd user directory if it doesn't exist
SYSTEMD_USER_DIR="$HOME/.config/systemd/user"
mkdir -p "$SYSTEMD_USER_DIR"

# Copy service file to systemd user directory
echo -e "${GREEN}Installing systemd service...${NC}"
cp "$SERVICE_FILE" "$SYSTEMD_USER_DIR/eye-saver.service"

# Reload systemd daemon
echo -e "${GREEN}Reloading systemd daemon...${NC}"
systemctl --user daemon-reload

# Enable the service to start on boot
echo -e "${GREEN}Enabling service to start on boot...${NC}"
systemctl --user enable eye-saver.service

# Start the service
echo -e "${GREEN}Starting Eye Saver service...${NC}"
systemctl --user start eye-saver.service

# Check service status
echo ""
echo -e "${GREEN}Checking service status...${NC}"
systemctl --user status eye-saver.service --no-pager || true

echo ""
echo "========================================="
echo -e "${GREEN}Installation complete!${NC}"
echo "========================================="
echo ""
echo "Useful commands:"
echo "  - Check status:    systemctl --user status eye-saver.service"
echo "  - Stop service:    systemctl --user stop eye-saver.service"
echo "  - Start service:   systemctl --user start eye-saver.service"
echo "  - Restart service: systemctl --user restart eye-saver.service"
echo "  - Disable service: systemctl --user disable eye-saver.service"
echo "  - View logs:       journalctl --user -u eye-saver.service -f"
echo ""
echo "Log file location: ~/.local/share/eye-saver/eye-saver.log"
echo ""
