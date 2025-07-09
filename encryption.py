from dbm import error

from cryptography.fernet import Fernet
import os

KEY_FILE = "passkey.key"

def generate_key():
    key = Fernet.generate_key()
    with open(KEY_FILE, "wb") as f:
        f.write(key)
    print(f"[+] Key saved to {KEY_FILE}")

# Load existing key
def load_key():
    if not os.path.exists(KEY_FILE):
        print("[!] Key file missing. Run generate_key() first.")
        return None
    with open(KEY_FILE, "rb") as f:
        return f.read()

# Encrypt a string
def encrypt(message):
    key = load_key()
    if not key:
        return None
    f = Fernet(key)
    return f.encrypt(message.encode()).decode()

# Decrypt a string
def decrypt(token):
    key = load_key()
    if not key:
        return None
    f = Fernet(key)
    return f.decrypt(token.encode()).decode()



