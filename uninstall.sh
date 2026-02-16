#!/bin/bash

# Eye Saver Uninstallation Script

set -e

echo "========================================="
echo "  Eye Saver Uninstallation Script"
echo "========================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

SYSTEMD_USER_DIR="$HOME/.config/systemd/user"
SERVICE_FILE="$SYSTEMD_USER_DIR/eye-saver.service"

# Stop the service
echo -e "${GREEN}Stopping Eye Saver service...${NC}"
systemctl --user stop eye-saver.service 2>/dev/null || true

# Disable the service
echo -e "${GREEN}Disabling Eye Saver service...${NC}"
systemctl --user disable eye-saver.service 2>/dev/null || true

# Remove service file
if [ -f "$SERVICE_FILE" ]; then
    echo -e "${GREEN}Removing service file...${NC}"
    rm "$SERVICE_FILE"
fi

# Reload systemd daemon
echo -e "${GREEN}Reloading systemd daemon...${NC}"
systemctl --user daemon-reload

echo ""
echo "========================================="
echo -e "${GREEN}Uninstallation complete!${NC}"
echo "========================================="
echo ""
echo "Note: Log files in ~/.local/share/eye-saver/ were preserved."
echo "You can manually delete them if needed."
echo ""
