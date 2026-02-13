import os
import sys

# CONFIGURATION
# We use a directory that looks legitimate but isn't critical to the OS.
# In a real deployment, this might be hidden deep in C:\Users\Public
CANARY_DIR = os.path.join(os.getcwd(), "sensitive_data") 

# These filenames are designed to trigger ransomware heuristics (scoring algorithms)
# Ransomware prioritizes files that look like high-value data.
CANARY_FILES = [
    "passwords.xlsx",
    "Q3_financial_report.docx",
    "employee_ssn_database.csv",
    "executive_salaries.pdf",
    "crypto_wallet_keys.txt"
]

def create_canary_directory():
    """Creates the directory and sets it as hidden (Windows only)."""
    try:
        if not os.path.exists(CANARY_DIR):
            os.makedirs(CANARY_DIR)
            print(f"[+] Created directory: {CANARY_DIR}")
            
            # WINDOWS ONLY: Set the directory to 'Hidden' to avoid accidental user deletion
            # This makes it a better trap—normal users won't see it, but ransomware scripts will.
            if sys.platform == 'win32':
                os.system(f'attrib +h "{CANARY_DIR}"')
                print(f"[+] Attribute set to HIDDEN for: {CANARY_DIR}")
        else:
            print(f"[*] Directory already exists: {CANARY_DIR}")

    except Exception as e:
        print(f"[-] Error creating directory: {e}")

def create_dummy_files():
    """Populates the directory with bait files containing dummy data."""
    print("[*] Generating canary files...")
    for filename in CANARY_FILES:
        filepath = os.path.join(CANARY_DIR, filename)
        
        try:
            with open(filepath, "w") as f:
                # We write a unique signature so we can track file integrity later if needed
                f.write(f"This is a canary file for Ransomware detection. Do not touch. ID: {filename}")
            print(f"    -> Generated: {filename}")
        except IOError as e:
            print(f"[-] Could not create {filename}: {e}")

if __name__ == "__main__":
    print("--- RANSOMWARE CANARY GENERATOR v1.0 ---")
    create_canary_directory()
    create_dummy_files()
    print("--- TRAP SET SUCCESSFULLY ---")