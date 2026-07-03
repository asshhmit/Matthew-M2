# =========================================================
# BLUETOOTH SCANNER GUI WITH DOUBLE CLAP EXIT
#
# FEATURES:
# ✔ Auto Bluetooth Scanning
# ✔ Popup GUI Window
# ✔ Tabular Device Information
# ✔ Real Bluetooth Names
# ✔ Signal Strength
# ✔ Manufacturer Data
# ✔ Assistant-style Summary
# ✔ Double Clap to Close Window
#
# INSTALL MODULES:
# pip install bleak sounddevice numpy
# =========================================================

import asyncio
import tkinter as tk
from tkinter import ttk
from bleak import BleakScanner
import threading
import sounddevice as sd
import numpy as np
import time

# =========================================================
# WINDOW SETUP
# =========================================================

root = tk.Tk()
root.title("Bluetooth Network Scanner")
root.geometry("1000x550")
root.configure(bg="#1e1e1e")

# ---------------------------------------------------------

title = tk.Label(
    root,
    text="Nearby Bluetooth Devices",
    font=("Arial", 20, "bold"),
    bg="#1e1e1e",
    fg="white"
)

title.pack(pady=10)

# =========================================================
# TABLE SETUP
# =========================================================

columns = (
    "No.",
    "Device Name",
    "MAC Address",
    "Signal Strength",
    "Manufacturer"
)

tree = ttk.Treeview(
    root,
    columns=columns,
    show="headings",
    height=15
)

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=180)

tree.pack(fill="both", expand=True, padx=10, pady=10)

# =========================================================
# STATUS LABEL
# =========================================================

status_label = tk.Label(
    root,
    text="Starting Bluetooth scan...",
    font=("Arial", 11),
    bg="#1e1e1e",
    fg="lightgreen",
    justify="left",
    wraplength=950
)

status_label.pack(pady=10)

# =========================================================
# BLUETOOTH SCAN FUNCTION
# =========================================================

async def bluetooth_scan():

    devices = await BleakScanner.discover(return_adv=True)

    total_devices = 0
    named_devices = []

    for i, (address, data) in enumerate(devices.items(), start=1):

        device = data[0]
        advertisement = data[1]

        # -------------------------------------------------
        # DEVICE NAME
        # -------------------------------------------------

        name = device.name or advertisement.local_name

        if not name:
            name = "Unknown Device"
        else:
            named_devices.append(name)

        # -------------------------------------------------
        # SIGNAL STRENGTH
        # -------------------------------------------------

        signal = f"{advertisement.rssi} dBm"

        # -------------------------------------------------
        # MANUFACTURER DATA
        # -------------------------------------------------

        manufacturer = (
            str(advertisement.manufacturer_data)
            if advertisement.manufacturer_data
            else "N/A"
        )

        total_devices += 1

        # -------------------------------------------------
        # INSERT INTO TABLE
        # -------------------------------------------------

        tree.insert(
            "",
            "end",
            values=(
                i,
                name,
                device.address,
                signal,
                manufacturer
            )
        )

    # =====================================================
    # FINAL SUMMARY MESSAGE
    # =====================================================

    if named_devices:

        names_text = ", ".join(named_devices)

        final_message = (
            f"Hey sir, I found {total_devices} devices in your area, "
            f"in which I can find the name of only "
            f"{len(named_devices)} devices.\n\n"
            f"Detected named devices:\n{names_text}\n\n"
            f"While other devices have no visible names, "
            f"I'm showing all available information "
            f"on your screen sir."
        )

    else:

        final_message = (
            f"Hey sir, I found {total_devices} devices nearby, "
            f"but none exposed their Bluetooth names."
        )

    status_label.config(text=final_message)

# =========================================================
# DOUBLE CLAP DETECTION
# =========================================================

# =========================================================
# IMPROVED DOUBLE CLAP DETECTION
# =========================================================

def detect_double_clap():

    clap_count = 0
    last_clap_time = 0
    cooldown_time = 0

    SAMPLE_RATE = 44100

    # Increase this if environment is noisy
    THRESHOLD = 12.1

    # Max gap between 2 claps
    CLAP_GAP = 0.8

    # Prevent multiple detections
    COOLDOWN = 2

    # -----------------------------------------------------

    def audio_callback(indata, frames, time_info, status):

        nonlocal clap_count
        nonlocal last_clap_time
        nonlocal cooldown_time

        current_time = time.time()

        # Audio volume intensity
        volume_norm = np.linalg.norm(indata) * 10

        # Ignore during cooldown
        if current_time - cooldown_time < COOLDOWN:
            return

        # Strong clap detected
        if volume_norm > THRESHOLD:

            print(f"Clap Intensity: {volume_norm:.2f}")

            # Detect fast second clap
            if current_time - last_clap_time <= CLAP_GAP:

                clap_count += 1

            else:
                clap_count = 1

            last_clap_time = current_time

            print(f"Clap Count: {clap_count}")

            # Double clap success
            if clap_count >= 2:

                print("DOUBLE CLAP DETECTED")
                print("Closing Bluetooth Scanner...")

                cooldown_time = current_time
                clap_count = 0

                root.after(0, root.destroy)

    # -----------------------------------------------------

    with sd.InputStream(
        callback=audio_callback,
        channels=1,
        samplerate=SAMPLE_RATE,
        blocksize=1024
    ):

        while True:
            sd.sleep(50)

# =========================================================
# THREAD FUNCTIONS
# =========================================================

def start_scan():
    asyncio.run(bluetooth_scan())

def start_clap_detection():
    detect_double_clap()

# =========================================================
# START THREADS
# =========================================================

# Auto Bluetooth Scan
threading.Thread(
    target=start_scan,
    daemon=True
).start()

# Double Clap Detection
threading.Thread(
    target=start_clap_detection,
    daemon=True
).start()

# =========================================================
# RUN WINDOW
# =========================================================

root.mainloop()