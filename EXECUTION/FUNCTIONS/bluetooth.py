# Install:
# pip install bleak tabulate

import asyncio
from bleak import BleakScanner
from tabulate import tabulate
import pyttsx3
import pyaudio 
import subprocess
import sys

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
async def scan_bluetooth():

    print("\nScanning for nearby Bluetooth devices...\n")

    devices = await BleakScanner.discover(return_adv=True)

    if not devices:
        print("No Bluetooth devices found.")
        return

    table_data = []

    total_devices = 0
    named_devices = []

    for i, (address, data) in enumerate(devices.items(), start=1):

        device = data[0]
        advertisement = data[1]

        # Get device name
        name = device.name or advertisement.local_name

        if not name:
            name = "Unknown Device"
        else:
            named_devices.append(name)

        total_devices += 1

        # Signal strength
        rssi = advertisement.rssi

        # Manufacturer info
        manufacturer = (
            str(advertisement.manufacturer_data)
            if advertisement.manufacturer_data
            else "N/A"
        )

        # Add row to table
        table_data.append([
            i,
            name,
            device.address,
            f"{rssi} dBm",
            manufacturer
        ])

    # Print table
    print(tabulate(
        table_data,
        headers=[
            "No.",
            "Device Name",
            "MAC Address",
            "Signal",
            "Manufacturer"
        ],
        tablefmt="grid"
    ))

    # Final assistant-style sentence
    print("\n--------------------------------------------------\n")
    text1 = (
        f"sir, I found {total_devices} devices in your area, "
        f"in which I can find the name of only {len(named_devices)} devices.\n"
    )
    print(
        f"sir, I found {total_devices} devices in your area, "
        f"in which I can find the name of only {len(named_devices)} devices.\n"
    )
    speak(text1)

    if named_devices:
        print("The detected named devices are:\n")
        
        for device_name in named_devices:
            print(f"- {device_name}")
            

    else:
        print("None of the nearby devices exposed their names.")
        speak("None of the nearby devices exposed their names.")

    print(
        "\nWhile other devices have no visible names, "
        "I'm showing all available information on your screen sir."
    )
    speak(
        "While other devices didn't exposed their names, "
    )
    speak("I'm showing all available information on your screen sir.")
    from pathlib import Path
    bt2 = Path(__file__).parent / "bluetooth2.py"

    subprocess.run([sys.executable, str(bt2)])
    
    
asyncio.run(scan_bluetooth())