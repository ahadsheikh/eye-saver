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
from datetime import datetime

class EyeSaver:
    def __init__(self):
        self.short_interval = 20 * 60  # 20 minutes in seconds
        self.cycles_until_long_break = 3  # After 3 cycles (60 minutes)
        self.current_cycle = 0
        self.running = True
        
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
    
    def short_break_reminder(self):
        """Send a short eye rest reminder"""
        self.send_notification(
            "👁️ Eye Rest Reminder",
            "Look away from the screen!\n20-20-20 rule: Look at something 20 feet away for 20 seconds.",
            urgency="normal",
            duration=15000
        )
    
    def long_break_reminder(self):
        """Send a 5-minute break notification"""
        self.send_notification(
            "⏰ Time for a Break!",
            "You've been working for 1 hour!\nTake a 5-minute break to rest your eyes and stretch.",
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
        
        self.log("Eye Saver started")
        self.send_notification(
            "Eye Saver Started",
            "You'll receive reminders every 20 minutes to rest your eyes.",
            urgency="low",
            duration=5000
        )
        
        try:
            while self.running:
                # Wait for the short interval
                time.sleep(self.short_interval)
                
                if not self.running:
                    break
                
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
