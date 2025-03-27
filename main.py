import cv2
import os
from tkinter import Tk
from tkinter.filedialog import askopenfilename
from time import sleep
import keyboard
import subprocess
import threading
from PIL import Image
from io import BytesIO
import time
import matplotlib.pyplot as plt
import numpy as np

def android_sleep():
    """Put the Android phone to sleep (like pressing the power button)."""
    try:
        print("Putting the Android phone to sleep...")
        os.system("adb shell input keyevent 26")  # Keyevent 26 simulates the power button
        print("The phone is now in sleep mode.")
    except Exception as e:
        print(f"Error: {e}")

def install_apk(apk_path):
    """Install an APK on the Android phone."""
    try:
        if not os.path.exists(apk_path):
            print("Error: APK file not found.")
            return
        print(f"Installing APK from {apk_path}...")
        os.system(f"adb install {apk_path}")
        print("APK installed successfully.")
    except Exception as e:
        print(f"Error: {e}")

def unlock_phone(password):
    """Unlock the Android phone using a password."""
    try:
        print("Unlocking the phone...")
        # Wake up the phone
        os.system("adb shell input keyevent 26")  # Simulate pressing the power button
        os.system("adb shell input swipe 500 1000 500 500")  # Simulate swipe to unlock
        # Enter the password
        for char in password:
            os.system(f"adb shell input text {char}")
        os.system("adb shell input keyevent 66")  # Simulate pressing 'Enter'
        print("The phone is now unlocked.")
    except Exception as e:
        print(f"Error: {e}")

def select_file():
    """Open a file explorer to select a file, starting in the Downloads directory."""
    try:
        Tk().withdraw()  # Hide the root Tkinter window
        downloads_path = os.path.expanduser("~/Downloads")  # Get the Downloads directory
        file_path = askopenfilename(
            title="Select an APK file",
            initialdir=downloads_path,  # Start in the Downloads directory
            filetypes=[("APK files", "*.apk"), ("All files", "*.*")]
        )
        if file_path:
            print(f"Selected file: {file_path}")
            return file_path
        else:
            print("No file selected.")
            return None
    except Exception as e:
        print(f"Error: {e}")
        return None

def open_android_file_explorer():
    """Open the Google Files app on the Android phone."""
    try:
        print("Opening the Google Files app on the Android phone...")
        os.system("adb shell am start -n com.google.android.apps.nbu.files/.home.HomeActivity")  # Directly launches the Google Files app
        print("Google Files app opened.")
    except Exception as e:
        print(f"Error: {e}")

def keyboard_control():
    """Control the Android phone's keyboard via ADB."""
    try:
        print("\nKeyboard Control Options:")
        print("1 - Type text")
        print("2 - Press Back button")
        print("3 - Press Home button")
        print("4 - Press Enter")
        print("5 - Exit Keyboard Control")
        
        while True:
            choice = input("Enter your choice: ")
            
            if choice == "1":
                text = input("Enter the text to type: ")
                os.system(f"adb shell input text \"{text}\"")  # Simulate typing text
                print(f"Typed: {text}")
            elif choice == "2":
                os.system("adb shell input keyevent 4")  # Simulate pressing the Back button
                print("Pressed Back button.")
            elif choice == "3":
                os.system("adb shell input keyevent 3")  # Simulate pressing the Home button
                print("Pressed Home button.")
            elif choice == "4":
                os.system("adb shell input keyevent 66")  # Simulate pressing the Enter key
                print("Pressed Enter.")
            elif choice == "5":
                print("Exiting Keyboard Control...")
                break
            else:
                print("Invalid choice. Please try again.")
    except Exception as e:
        print(f"Error: {e}")

def record_keyboard_typing():
    """Record keyboard typing in real life and send keys to the Android phone."""
    print("Recording keyboard typing. Press 'Right Shift + Q' to stop.")
    buffer = []  # Buffer to batch key presses
    stop_event = threading.Event()

    def send_to_android():
        """Send buffered keys to the Android phone."""
        while not stop_event.is_set():
            if buffer:
                # Join buffered keys into a single string and send them
                text = ''.join(buffer)
                buffer.clear()
                try:
                    subprocess.run(["adb", "shell", "input", "text", text], check=True)
                except subprocess.CalledProcessError as e:
                    print(f"Error sending keys to Android: {e}")
            stop_event.wait(0.1)  # Wait briefly to batch inputs

    def record_event(event):
        """Record key events and add them to the buffer."""
        if event.event_type == "down":
            if len(event.name) == 1:  # Only handle printable characters
                buffer.append(event.name)
            elif event.name == "space":
                buffer.append(" ")  # Add a space
            elif event.name == "enter":
                try:
                    subprocess.run(["adb", "shell", "input", "keyevent", "66"], check=True)  # Keyevent 66 simulates Enter
                except subprocess.CalledProcessError as e:
                    print(f"Error sending Enter to Android: {e}")
            elif event.name == "backspace":
                try:
                    subprocess.run(["adb", "shell", "input", "keyevent", "67"], check=True)  # Keyevent 67 simulates Backspace
                except subprocess.CalledProcessError as e:
                    print(f"Error sending Backspace to Android: {e}")

            # Stop recording when 'Right Shift + Q' is pressed
            if event.name == 'q' and keyboard.is_pressed('right shift'):
                print("Stopping recording...")
                stop_event.set()  # Signal the sender thread to stop
                keyboard.unhook_all()  # Unhook all listeners

    # Start a background thread to send buffered keys to the Android phone
    sender_thread = threading.Thread(target=send_to_android, daemon=True)
    sender_thread.start()

    # Hook the keyboard to record events
    keyboard.hook(record_event)
    # Wait indefinitely until the recording is stopped
    keyboard.wait()

def main():
    while True:
        print("\nChoose an option:")
        print("1 - Put Android phone connected via USB to sleep")
        print("2 - Install an APK on the Android phone")
        print("3 - Unlock the phone using a password")
        print("4 - Open the Google Files app")
        print("5 - Keyboard Control")
        print("6 - Record keyboard typing (stop with Right Shift + Q)")
        print("7 - Exit")
        
        choice = input("Enter your choice: ")
        
        if choice == "1":
            android_sleep()
            sleep(2)
            os.system("clear")
        elif choice == "2":
            apk_path = select_file()
            if apk_path:
                install_apk(apk_path)
                sleep(2)
                os.system("clear")
        elif choice == "3":
            password = input("Enter the password to unlock the phone: ")
            unlock_phone(password)
            sleep(2)
            os.system("clear")
        elif choice == "4":
            open_android_file_explorer()
            sleep(2)
            os.system("clear")
        elif choice == "5":
            keyboard_control()
            sleep(2)
            os.system("clear")
        elif choice == "6":
            record_keyboard_typing()
            sleep(2)
            os.system("clear")
        elif choice == "7":
            print("Exiting the program...")
            break
        else:
            print("Invalid choice. Please try again.")
            sleep(2)
            os.system("clear")

if __name__ == "__main__":
    main()