# 👁️ Eye Saver

A simple Python-based eye rest reminder tool for Ubuntu/Linux that helps you follow the 20-20-20 rule and take regular breaks.

## Features

- 🔔 **Regular Reminders**: Notifications every 20 minutes to rest your eyes
- ⏰ **Break Notifications**: After 1 hour (3 cycles), get reminded to take a 5-minute break
- 🚀 **Auto-start**: Runs automatically on system startup
- 📝 **Logging**: Keeps logs of all notifications sent
- 🔄 **Background Service**: Runs silently in the background using systemd

## How It Works

The Eye Saver follows a simple pattern:
1. Every **20 minutes**: You get a notification to look away from the screen (20-20-20 rule)
2. After **60 minutes** (3 cycles): You get a more urgent notification to take a 5-minute break
3. The cycle resets and continues

This follows the recommended eye care practices:
- **20-20-20 rule**: Every 20 minutes, look at something 20 feet away for 20 seconds
- **Hourly breaks**: Take a 5-minute break every hour to rest your eyes and stretch

## Installation

### Prerequisites

- Ubuntu/Linux operating system
- Python 3 (usually pre-installed)
- `notify-send` (libnotify-bin package - the installer will install it if missing)

### Quick Install

1. Clone or download this repository
2. Navigate to the directory:
   ```bash
   cd /home/sheikhahaduzzaman/Code/scripts/eye-saver
   ```

3. Run the installation script:
   ```bash
   chmod +x install.sh
   ./install.sh
   ```

The installation script will:
- Install any missing dependencies
- Make the Python script executable
- Set up a systemd user service
- Enable and start the service automatically

## Usage

Once installed, Eye Saver runs automatically in the background. You don't need to do anything!

### Manual Control

Control the service using these commands:

```bash
# Check if the service is running
systemctl --user status eye-saver.service

# Stop the service
systemctl --user stop eye-saver.service

# Start the service
systemctl --user start eye-saver.service

# Restart the service
systemctl --user restart eye-saver.service

# Disable auto-start on boot
systemctl --user disable eye-saver.service

# Enable auto-start on boot
systemctl --user enable eye-saver.service

# View live logs
journalctl --user -u eye-saver.service -f

# View all logs
journalctl --user -u eye-saver.service
```

### Log Files

Logs are stored in: `~/.local/share/eye-saver/eye-saver.log`

You can view the log file with:
```bash
cat ~/.local/share/eye-saver/eye-saver.log
# or
tail -f ~/.local/share/eye-saver/eye-saver.log
```

## Uninstallation

To remove Eye Saver:

```bash
chmod +x uninstall.sh
./uninstall.sh
```

This will stop and remove the service. Log files will be preserved but can be manually deleted from `~/.local/share/eye-saver/` if desired.

## Customization

You can customize the reminder intervals by editing [eye_saver.py](eye_saver.py):

```python
# Edit these values in the __init__ method
self.short_interval = 20 * 60  # Change 20 to your preferred minutes
self.cycles_until_long_break = 3  # Change 3 to your preferred number of cycles
```

After making changes, restart the service:
```bash
systemctl --user restart eye-saver.service
```

## Troubleshooting

### Notifications not appearing

1. Check if the service is running:
   ```bash
   systemctl --user status eye-saver.service
   ```

2. Check the logs:
   ```bash
   journalctl --user -u eye-saver.service -n 50
   ```

3. Make sure `notify-send` is installed:
   ```bash
   sudo apt-get install libnotify-bin
   ```

4. Test notifications manually:
   ```bash
   notify-send "Test" "This is a test notification"
   ```

### Service not starting on boot

1. Enable the service:
   ```bash
   systemctl --user enable eye-saver.service
   ```

2. Enable lingering (allows user services to run even when not logged in):
   ```bash
   loginctl enable-linger $USER
   ```

### Permission issues

Make sure the Python script is executable:
```bash
chmod +x /home/sheikhahaduzzaman/Code/scripts/eye-saver/eye_saver.py
```

## Why Take Eye Breaks?

Prolonged screen time can lead to:
- Eye strain and fatigue
- Dry eyes
- Headaches
- Blurred vision
- Neck and shoulder pain

Regular breaks help:
- Reduce eye strain
- Prevent computer vision syndrome
- Improve focus and productivity
- Reduce physical discomfort

## License

This project is free to use and modify as needed.

## Contributing

Feel free to submit issues, fork the repository, and create pull requests for any improvements.

---

**Stay healthy, protect your eyes! 👁️✨**
