import sys
import time
import os
import requests
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# --- CONFIGURATION ---
# DIRECTORY TO WATCH: We only watch the trap folder to minimize noise.
WATCH_DIRECTORY = os.path.join(os.getcwd(), "sensitive_data")

# DISCORD WEBHOOK: Paste your URL inside the quotes!
WEBHOOK_URL = "https://discord.com/api/webhooks/URL"
# AUTOMATED RESPONSE: Set to True to enable network isolation
# WARNING: This will cut your internet connection when triggered!
ENABLE_RESPONSE = True 

class RansomwareHandler(FileSystemEventHandler):
    """
    Handles file system events. If a canary file is touched, 
    we assume a ransomware attack is in progress.
    """
    
    def on_modified(self, event):
        # We only care about files, not directories
        if not event.is_directory:
            self.trigger_alert(event.src_path, "MODIFIED")

    def on_deleted(self, event):
        if not event.is_directory:
            self.trigger_alert(event.src_path, "DELETED")

    def on_moved(self, event):
        if not event.is_directory:
            self.trigger_alert(event.src_path, f"RENAMED to {event.dest_path}")

    def trigger_alert(self, file_path, action):
        """Sends the alert and triggers the response."""
        
        # 1. CONSOLE ALERT
        print(f"\n[!!!] CRITICAL ALERT: Canary file {action}!")
        print(f"      Target: {file_path}")

        # 2. DISCORD ALERT
        data = {
            "content": "@everyone", 
            "embeds": [{
                "title": "RANSOMWARE ACTIVITY DETECTED",
                "description": f"**Event:** File {action}\n**Path:** `{file_path}`\n**Host:** Windows-Lab-01",
                "color": 16711680  # Red color code
            }]
        }
        try:
            requests.post(WEBHOOK_URL, json=data)
            print("[+] Discord Alert Sent.")
        except Exception as e:
            print(f"[-] Failed to send alert: {e}")

        # 3. AUTOMATED RESPONSE (Tier 2 Capability)
        if ENABLE_RESPONSE:
            self.isolate_host()

    def isolate_host(self):
        """Executes a shell command to disable the network adapter."""
        print("[*] INITIATING HOST ISOLATION PROTOCOL...")
        try:
            # 1. ALERT FIRST (While we still have internet)
            requests.post(WEBHOOK_URL, json={"content": "**AUTOMATED DEFENSE:** Host Network Interface is being disabled NOW."})
            print("[+] Pre-isolation alert sent.")

            # 2. THEN KILL THE NETWORK
            # (Replace "Ethernet" with your actual interface name if different)
            subprocess.run(["netsh", "interface", "set", "interface", "Ethernet", "admin=disable"], check=True)
            print("[+] HOST ISOLATED. Network adapter disabled.")
            
        except Exception as e:
            print(f"[-] Isolation Failed: {e}")

if __name__ == "__main__":
    print(f"[*] RANSOMWARE MONITOR ACTIVE...")
    print(f"[*] Watching Directory: {WATCH_DIRECTORY}")
    print(f"[*] Response Mode: {'ENABLED (Dangerous)' if ENABLE_RESPONSE else 'DISABLED (Safe Mode)'}")
    print("[*] Press Ctrl+C to stop.")

    event_handler = RansomwareHandler()
    observer = Observer()
    observer.schedule(event_handler, path=WATCH_DIRECTORY, recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()