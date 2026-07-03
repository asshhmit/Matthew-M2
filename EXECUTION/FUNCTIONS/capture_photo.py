import os
import pywhatkit
import subprocess
import time 
import pyautogui
import shutil
import pyttsx3
from pathlib import Path
import pyaudio
# clear the file first 
def speak(text):
    try:
        engine = pyttsx3.init()
        engine.setProperty('rate', 150)
        voices = engine.getProperty('voices')
        if len(voices) > 1:
            engine.setProperty('voice', voices[1].id)
        engine.say(text)
        engine.runAndWait()
        engine.stop()
    except Exception as e:
        print(f"Speak error: {e}")
folder_path = Path(__file__).resolve().Parents[2] / "DATA" / "PHOTO" / "RECENTLY_CAPTURED" 

for item in os.listdir(folder_path):
    item_path = os.path.join(folder_path, item)

    try:
        if os.path.isfile(item_path) or os.path.islink(item_path):
            os.remove(item_path)  # Delete file
        elif os.path.isdir(item_path):
            shutil.rmtree(item_path)  # Delete folder and its contents
    except Exception as e:
        print(f"Failed to delete {item_path}: {e}")

print("Folder emptied successfully.")

# capture photo 

import cv2
import os
from datetime import datetime

# Folder where the photo will be saved
save_folder = Path(__file__).resolve().Parents[2] / "DATA" / "PHOTO" / "RECENTLY_CAPTURED" 

# Create the folder if it doesn't exist
os.makedirs(save_folder, exist_ok=True)

# Open the webcam
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Could not open the webcam.")
    exit()

print("Press SPACE to capture the photo.")
print("Press ESC to quit.")

while True:
    ret, frame = cap.read()

    if not ret:
        print("Failed to capture frame.")
        break

    cv2.imshow("Camera", frame)

    key = cv2.waitKey(1)
    time.sleep(2)
    speak("smile")
    pyautogui.press("space")
    # SPACE key
    if key == 32:
        # Create a unique filename
        filename = "captured.jpg"
        filepath = os.path.join(save_folder, filename)

        # Save the image
        cv2.imwrite(filepath, frame)
        print(f"Photo saved at:\n{filepath}")
        break

    # ESC key
    elif key == 27:
        print("Cancelled.")
        break

cap.release()
cv2.destroyAllWindows()

# copy photo to clipboard

phone_number = "+919899610964"
message = "Here's the photo"

pywhatkit.sendwhatmsg_instantly(
    phone_number,
    message,
    wait_time=25,      # Wait for WhatsApp Web to load
    #tab_close=True,    # Close the tab after sending
    #close_time=3
)


def copy_file_to_clipboard(file_path):
    subprocess.run(
        ['powershell', '-command',
         f'Set-Clipboard -Path "{file_path}"'],
        shell=True
    )
    print("File copied to clipboard!")
copy = f"{save_folder}/captured.jpg"
copy_file_to_clipboard(copy)
time.sleep(1)
pyautogui.hotkey("ctrl", "v")
time.sleep(2)
pyautogui.press("enter")

time.sleep(2)
os.system("taskkill /F /IM msedge.exe")

speak("sir , i have sent the photo to your whatsapp ")

