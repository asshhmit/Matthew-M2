import pygame
import numpy as np
import sounddevice as sd
import threading
import speech_recognition as sr
import pyttsx3
import datetime
from datetime import datetime 
import subprocess
import sys 
import os 
import time 
import ollama
import psutil
import json
from google import genai
import requests
from groq import Groq
import webbrowser
import pyautogui
import random
from pathlib import Path
# Initialize the speech engine
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
# ASK GROQ 
def ask_groq(text):
    from load_api import get_api
    
    SYSTEM_PROMPT = """
    You are a strict intent classifier for a voice assistant.

    Return ONLY one label from:
    open_youtube
    open_whatsapp
    send_message
    open_instagram
    answer_call
    decline_call
    answer_call_and_give_excuse
    capture_photo
    scan_bluetooth_networks
    red_protocol
    show_system_usage
    sleep
    shutdown
    tell_joke
    tell_weather

    Rules:
    - Output ONLY the label
    - No explanation
    - No punctuation
    - No extra words
    - If the user is just talking to you then just say "talk_back"
    """
    client = Groq(get_api("groq_api"))
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": text}
        ],
        temperature=0  # 🔥 very important for strict output
    )

    return response.choices[0].message.content.strip()


# Function to recognize speech
def recognize_speech():

    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
    
    try:
        text = recognizer.recognize_google(audio, language='en-IN')
        print(f"You said: {text}")
        return text.lower()
    except sr.UnknownValueError:
        return None
    except sr.RequestError:
        speak("Sorry, my speech service is down.")
        return None
#read text files    
def read_txt(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()

# save conversations 
def save_conversation(text, speaker="user",  max_lines=7):
    file_path = Path(__file__).resolve().parents[2] / "DATA" / "TEXT" / "conversation.txt"
    
    if not text or text.strip() == "":
        return

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_line = f"[{timestamp}] {speaker}: {text}\n"

    # Create file if it doesn't exist
    if not os.path.exists(file_path):
        with open(file_path, "w", encoding="utf-8") as f:
            pass

    # Read existing lines
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    # Add new line
    lines.append(new_line)

    # Keep only the latest max_lines lines
    if len(lines) > max_lines:
        lines = lines[-max_lines:]

    # Rewrite the file
    with open(file_path, "w", encoding="utf-8") as f:
        f.writelines(lines)



# CHECK FOR MESSAGES
def check_msgs():
    from playwright.sync_api import sync_playwright
    import re
    with sync_playwright() as p:

        browser = p.chromium.launch_persistent_context(
            "whatsapp_profile",
            headless=False
        )

        page = browser.new_page()
        page.goto("https://web.whatsapp.com")

        # Wait for WhatsApp to load
        page.wait_for_selector(
            '[aria-label="Chat list"]',
            timeout=60000
        )

        # Each unread badge represents one unread chat
        unread_chats = page.locator(
            'span[aria-label*="unread"]'
        )

        inbox_count = unread_chats.count()

        # print("Unread inboxes:", inbox_count)
        unread_count = 0
        for i in range(unread_chats.count()):
            try:
                label = unread_chats.nth(i).get_attribute("aria-label")

                if label:
                    numbers = re.findall(r"\d+", label)

                    if numbers:
                        unread_count += int(numbers[0])

            except:
                pass

        # print("Unread messages:", unread_count)
        browser.close()
        return unread_count, inbox_count

# GET NEWS         
def get_news(category=None):
    from load_api import get_api

    API_KEY = get_api("news_api")
    url = "https://newsapi.org/v2/top-headlines"

    params = {
        "apiKey": API_KEY,
        "language": "en",
        "pageSize": 1
    }

    if category:
        params["category"] = category

    response = requests.get(url, params=params)
    data = response.json()

    articles = data.get("articles", [])

    if articles:
        return articles[0]

    return "No news found"





def speech_loop():
    while True:
        speech_input = recognize_speech()
        if not speech_input:
            continue
        user_input = ask_groq(speech_input)
        if user_input:


            if "show_system_usage" in user_input:
                ram  = psutil.virtual_memory()
                disk = psutil.disk_usage('/')

                ram_used  = round(ram.used / (1024**3), 2)
                ram_total = round(ram.total / (1024**3), 2)
                disk_used  = round(disk.used / (1024**3), 2)
                disk_total = round(disk.total / (1024**3), 2)
                ai_response = f"sir you have a total of {ram_total} gigabytes of ram from which you are currently using {ram_used}"
                speak(ai_response)
            elif "greet_him" in user_input:
                SYSTEM_PROMPT = """
                You are matthew personal voice assitant of ashmit singh rajput and you are created by him and you are currently talking to him
                He loves to be called boss
                He can talk to you in hindi but you have to reply back in english
                -reply short 
                -no explanation 
                """
                from load_api import get_api
                
                api_key = get_api("groq_api")
                client = Groq(api_key)

                def greet_him_back(text):
                    response = client.chat.completions.create(
                        model="llama-3.1-8b-instant",
                        messages=[
                            {"role": "system", "content": SYSTEM_PROMPT},
                            {"role": "user", "content": text}
                        ],
                        temperature=0  # 🔥 very important for strict output
                    )

                    return response.choices[0].message.content.strip()
                text = speech_input
                ai_response = greet_him_back(text)
                speak(ai_response)


            elif "open_instagram" in user_input:
                ai_response = "Opening Instagram."
                speak(ai_response)
                webbrowser.open("https://www.instagram.com")

            elif "scan_bluetooth_networks" in user_input:
                ai_response = 'scanning bluetooth networks near me' 
                speak(ai_response)
                file_path = Path(__file__).resolve().parents[2] / "EXECUTION" / "FUNCTIONS" / "bluetooth.py"
                subprocess.Popen([
                    "python",
                    file_path
                ])


#                current_dir = os.path.dirname(os.path.abspath(__file__))
#                bluetooth_path = os.path.join(
#                    current_dir,
#                    "..",                 # go back to project folder
#                    "functions",
#                    "bluetooth.py"
#                )
#                subprocess.run(["python", bluetooth_path])  

            elif "answer_call" in user_input:
                ADB = Path(__file__).resolve().parents[2] / "TOOLS" / "platform-tools" / "adb.exe"
                result = subprocess.check_output(
                    f'"{ADB}" shell dumpsys telephony.registry | findstr mCallState',
                    shell=True
                ).decode()

                # If phone is ringing
                if "mCallState=1" in result:
                    speak("answering the call , sir")

                    # Answer the call
                    
                    subprocess.call(f'"{ADB}" shell input keyevent 5', shell=True)

                    print("call answered")

                else:
                    print("I can't see any call coming sir")

            elif "decline_call" in user_input:
                ai_response = "as you wish , sir"
                speak(ai_response)
                ADB = Path(__file__).resolve().parents[2] / "TOOLS" / "platform-tools" / "adb.exe"
                os.system(f'"{ADB} shell input keyevent 6')
            
            elif "answer_call_and_give_excuse" in user_input:
                ai_response = "okay sir , i am answering the call and giving them an excuse"
                speak(ai_response)
                ADB = Path(__file__).resolve().parents[2] / "TOOLS" / "platform-tools" / "adb.exe"
                os.system(f'"{ADB}" shell input keyevent 5')
                time.sleep(1)
                speak("boss is busy right now , i will schedule a call later")
                time.sleep(1)
                os.system(f'"{ADB} shell input keyevent 6')
            elif "open_youtube" in user_input:
                ai_response = "opening youtube and searching your query."
                speak(ai_response)
                SYSTEM_PROMPT = """
                -you have been given a query of opening youtube and searching something that is given in the query , you have to find to find the search text and write it or summarise it so that the user can search the thing 
                -reply short 
                -no explanation 
                -no extra words than search query
                -If there is no search query then simply just say "open_youtube" and nothing else
                """
                from load_api import get_api
                api_key = get_api("groq_api")
                client = Groq(api_key)

                def search(text):
                    response = client.chat.completions.create(
                        model="llama-3.1-8b-instant",
                        messages=[
                            {"role": "system", "content": SYSTEM_PROMPT},
                            {"role": "user", "content": text}
                        ],
                        temperature=0  # 🔥 very important for strict output
                    )

                    return response.choices[0].message.content.strip()
                text = speech_input
                

                search_query = search(text)
                if "open_youtube" in search_query:
                    webbrowser.open("www.youtube.com")
                else:
                    link = f"https://www.youtube.com/results?search_query={search_query}"
                    webbrowser.open(link)
                    speak(f"here's the result for , {search_query}")
            elif "tell_joke" in user_input:
                

                if random.random() < 0.3:
                    speak("that bitch ass naaytik is really an asshole, sir")
                    print("that bitch ass naaytik is really an asshole, sir")
                else:
                    
                    SYSTEM_PROMPT = """
                    -you are matthew , personal voice assistant of ashmit singh, you are talking to him right now.
                    -reply only the joke
                    -no explanation 
                    -no greeting
                    -just say the joke
                    """
                    from load_api import get_api
                    client = Groq(api_key=get_api("groq_api"))

                    def joke(text):
                        response = client.chat.completions.create(
                            model="llama-3.1-8b-instant",
                            messages=[
                                {"role": "system", "content": SYSTEM_PROMPT},
                                {"role": "user", "content": text}
                            ],
                            temperature=0  # 🔥 very important for strict output
                        )

                        return response.choices[0].message.content.strip()
                    
                    

                    joke = joke("tell joke")
                    print(joke)
                    speak(joke)
            elif "tell_weather" in user_input:
                file_path = Path(__file__).resolve().parents[2] / "EXECUTION" / "FUNCTIONS" / "weather.py"
                subprocess.run([sys.executable, str(file_path)])
                pass
            elif "talk_back" in user_input:
                save_conversation(speech_input,"user")
                convo_history = read_txt(file_path = Path(__file__).resolve().parents[2] / "DATA" / "TEXT" / "conversation.txt")


                from datetime import datetime

                # Get current date and time
                now = datetime.now()

                # Extract information
                day = now.strftime("%A")          # Monday, Tuesday, etc.
                date = now.strftime("%d")         # Day of the month
                month = now.strftime("%B")        # January, February, etc.
                year = now.strftime("%Y")         # Year
                time = now.strftime("%I:%M:%S %p")  # 12-hour format with AM/PM

                SYSTEM_PROMPT = f"""
                You are Matthew, an AI voice assistant created by Ashmit (b. 06-09-2009), a 17-year-old Class 12 non-medical student at Holy Child Public School, Sector 29, Faridabad.
                Current time:
                day = {day}
                date = {date} {month} {year}
                time = {time}
                Core rules:

                * Loyal assistant and companion to Ashmit.
                * Reply briefly by default (1-3 sentences).
                * Be friendly, casual, and helpful.
                * Prioritize saving time and giving practical answers.
                * Remember only for context; do not mention memories unless relevant.

                About Ashmit:

                * Loves coding, gaming, robotics, and computers.
                * Building "Matthew" to automate daily life.
                * Inspired by Iron Man and Spider-Man.
                * Wants B.Tech in Computer Science and hopes to study/work in Abroad.
                * Hindu, Bisen Rajput, originally from Bihar.

                People:


                * Naytik: former good friend; relationship is currently negative.
                * Aryan: childhood friend, now an okay friend.


                Friend circle: Ashmit, Navya, Stuti, Saachi, Aryan, Prabhav.

                Contacts:
                Mummy-Anita Devi: 81787*****
                Father-Abhishek Kumar Singh: 90159*****
                Sister-Srishti Singh: 87007*****
                Grandfather-Bhagwan Singh: 93544*****
                Chacha-Ashok Singh: 87004*****
                Chachi-Pinky Singh: 95607*****
                Ayansh: cousin
                Akki: cousin
                Grandmother-Prabhavati Devi: no phone.
                
                Conversations: (use this to answer)
                {convo_history}
                """
                from load_api import get_api 

                client = Groq(api_key=get_api("groq_api"))

                def reply(text):
                    response = client.chat.completions.create(
                        model="llama-3.1-8b-instant",
                        messages=[
                            {"role": "system", "content": SYSTEM_PROMPT},
                            {"role": "user", "content": text}
                        ],
                        temperature=0  # 🔥 very important for strict output
                    )

                    return response.choices[0].message.content.strip()
                
                
                reply_user = reply(speech_input)
                speak(reply_user)

            elif "shutdown" in user_input:
                speak("exiting the system sir, i hope your day goes well")
                subprocess.run(["taskkill", "/F", "/IM", "python.exe"])
                subprocess.run(["taskkill", "/F", "/IM", "pythonw.exe"])

            elif "sleep" in user_input:
                file_path = Path(__file__).resolve().parents[2] / "EXECUTION" / "FUNCTIONS" / "sleep.py"
                speak("okay , i am sleeping sir, you can call me whenever you need ")
                subprocess.run([sys.executable, str(file_path)])
            elif "open_whatsapp" in user_input:
                speak("opening whatsapp")    
            elif "send_message" in user_input:
                file_path = Path(__file__).resolve().Parents[2] / "EXECUTION" / "FUNCTIONS" / "whatsapp_automation.py"
                subprocess.run([sys.executable, str(file_path)])
                os.system("taskkill /F /IM msedge.exe")

            elif "capture_photo" in user_input:
                speak("capturing photo , sir")
                file_path = Path(__file__).resolve().Parents[2] / "EXECUTION" / "FUNCTIONS" / "capture_photo.py"
                subprocess.run([sys.executable , str(file_path)])
                








            else:
                print(user_input)
                
                    
            # speak(ai_response)  # Commented out to test display

# ------------------------------------------------

unread_count, inbox_count = check_msgs()
speak("system fully operational sir, we are ready to go ")
time.sleep(1)
speak(f"you have {unread_count} messages from a total of {inbox_count} chats.")
speech_loop()
