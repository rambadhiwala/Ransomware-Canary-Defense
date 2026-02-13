import subprocess

# REPLACE "Ethernet" WITH YOUR INTERFACE NAME
INTERFACE_NAME = "Ethernet"

try:
    print(f"[*] Attempting to restore interface: {INTERFACE_NAME}...")
    subprocess.run(["netsh", "interface", "set", "interface", INTERFACE_NAME, "admin=enable"], check=True)
    print("[+] SUCCESS: Internet should be back online.")
except Exception as e:
    print(f"[-] FAILED: {e}")
    print("    (Did you run this as Administrator?)")