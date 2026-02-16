#!/usr/bin/env python3
"""
Eye Saver - A simple eye rest reminder tool
Sends notifications every 20 minutes for eye rest
Every hour (after 3 cycles), sends a 5-minute break notification
"""

import time
import subprocess
import os
import signal
import sys
import json
from datetime import datetime

class EyeSaver:
    def __init__(self):
        self.running = True
        
        # Default configuration
        self.defaults = {
            'short_interval_minutes': 20,
            'cycles_until_long_break': 3,
            'start_hour': 0,
            'end_hour': 24,
            'notifications': {
                'short_break_title': '👁️ Eye Rest Reminder',
                'short_break_message': 'Look away from the screen!\n20-20-20 rule: Look at something 20 feet away for 20 seconds.',
                'long_break_title': '⏰ Time for a Break!',
                'long_break_message': "You've been working for 1 hour!\nTake a 5-minute break to rest your eyes and stretch."
            }
        }
        
        # Load configuration
        config = self.load_config()
        
        # Set configuration values
        self.short_interval = config['short_interval_minutes'] * 60  # Convert to seconds
        self.cycles_until_long_break = config['cycles_until_long_break']
        self.start_hour = config['start_hour']
        self.end_hour = config['end_hour']
        self.notifications = config['notifications']
        self.current_cycle = 0
    
    def get_config_path(self):
        """Get the path to the configuration file"""
        # Try multiple locations in order of priority
        config_locations = [
            os.path.expanduser("~/.config/eye-saver/config.json"),
            os.path.join(os.path.dirname(__file__), "config.json"),
        ]
        
        for config_path in config_locations:
            if os.path.exists(config_path):
                return config_path
        
        # Return the default location even if it doesn't exist
        return config_locations[0]
    
    def load_config(self):
        """Load configuration from file or use defaults"""
        config_path = self.get_config_path()
        
        try:
            if os.path.exists(config_path):
                with open(config_path, 'r') as f:
                    user_config = json.load(f)
                
                # Merge user config with defaults (user config takes precedence)
                config = self.defaults.copy()
                config.update(user_config)
                
                # Handle nested notifications dict
                if 'notifications' in user_config:
                    config['notifications'] = self.defaults['notifications'].copy()
                    config['notifications'].update(user_config['notifications'])
                
                self.log(f"Loaded configuration from: {config_path}")
                return config
            else:
                self.log(f"Config file not found at {config_path}, using defaults")
                return self.defaults.copy()
        
        except json.JSONDecodeError as e:
            self.log(f"Error parsing config file: {e}. Using defaults.")
            return self.defaults.copy()
        except Exception as e:
            self.log(f"Error loading config: {e}. Using defaults.")
            return self.defaults.copy()
        
    def send_notification(self, title, message, urgency="normal", duration=10000):
        """Send desktop notification using notify-send"""
        try:
            subprocess.run([
                'notify-send',
                '-u', urgency,  # urgency level: low, normal, critical
                '-t', str(duration),  # duration in milliseconds
                '-i', 'dialog-information',  # icon
                title,
                message
            ])
            self.log(f"Notification sent: {title} - {message}")
        except Exception as e:
            self.log(f"Error sending notification: {e}")
    
    def log(self, message):
        """Log messages with timestamp"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"[{timestamp}] {message}"
        print(log_message)
        
        # Also write to log file
        log_dir = os.path.expanduser("~/.local/share/eye-saver")
        os.makedirs(log_dir, exist_ok=True)
        log_file = os.path.join(log_dir, "eye-saver.log")
        
        try:
            with open(log_file, 'a') as f:
                f.write(log_message + "\n")
        except Exception as e:
            print(f"Error writing to log file: {e}")
    
    def is_within_active_hours(self):
        """Check if current time is within active hours"""
        current_hour = datetime.now().hour
        return self.start_hour <= current_hour < self.end_hour
    
    def get_seconds_until_active_hours(self):
        """Calculate seconds until the next active period starts"""
        now = datetime.now()
        current_hour = now.hour
        
        if current_hour < self.start_hour:
            # Before start time today
            target = now.replace(hour=self.start_hour, minute=0, second=0, microsecond=0)
            seconds = (target - now).total_seconds()
        else:
            # After end time, wait until start time tomorrow
            from datetime import timedelta
            tomorrow = now + timedelta(days=1)
            target = tomorrow.replace(hour=self.start_hour, minute=0, second=0, microsecond=0)
            seconds = (target - now).total_seconds()
        
        return int(seconds)
    
    def short_break_reminder(self):
        """Send a short eye rest reminder"""
        self.send_notification(
            self.notifications['short_break_title'],
            self.notifications['short_break_message'],
            urgency="normal",
            duration=15000
        )
    
    def long_break_reminder(self):
        """Send a 5-minute break notification"""
        self.send_notification(
            self.notifications['long_break_title'],
            self.notifications['long_break_message'],
            urgency="critical",
            duration=20000
        )
    
    def signal_handler(self, signum, frame):
        """Handle shutdown signals gracefully"""
        self.log("Received shutdown signal. Stopping Eye Saver...")
        self.running = False
        sys.exit(0)
    
    def run(self):
        """Main loop"""
        # Register signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
        
        self.log(f"Eye Saver started (Active hours: {self.start_hour}:00 - {self.end_hour}:00)")
        
        # Only send startup notification if within active hours
        if self.is_within_active_hours():
            self.send_notification(
                "Eye Saver Started",
                f"You'll receive reminders every 20 minutes to rest your eyes.\nActive hours: {self.start_hour}:00 AM - {self.end_hour}:00 PM",
                urgency="low",
                duration=5000
            )
        
        try:
            while self.running:
                # Check if we're within active hours
                if not self.is_within_active_hours():
                    # Calculate time until next active period
                    sleep_time = self.get_seconds_until_active_hours()
                    self.log(f"Outside active hours. Sleeping for {sleep_time/3600:.1f} hours until {self.start_hour}:00")
                    
                    # Reset cycle counter when entering inactive period
                    self.current_cycle = 0
                    
                    # Sleep in smaller chunks to allow for graceful shutdown
                    while sleep_time > 0 and self.running and not self.is_within_active_hours():
                        chunk = min(300, sleep_time)  # Sleep max 5 minutes at a time
                        time.sleep(chunk)
                        sleep_time -= chunk
                    
                    if not self.running:
                        break
                    
                    # We're now in active hours
                    self.log("Entering active hours. Starting notifications.")
                    continue
                
                # Wait for the short interval
                time.sleep(self.short_interval)
                
                if not self.running:
                    break
                
                # Double-check we're still in active hours after sleeping
                if not self.is_within_active_hours():
                    continue
                
                # Increment cycle counter
                self.current_cycle += 1
                
                # Check if it's time for a long break
                if self.current_cycle >= self.cycles_until_long_break:
                    self.long_break_reminder()
                    self.current_cycle = 0  # Reset cycle counter
                else:
                    self.short_break_reminder()
        
        except Exception as e:
            self.log(f"Error in main loop: {e}")
            raise

if __name__ == "__main__":
    saver = EyeSaver()
    saver.run()
