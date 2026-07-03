import pywhatkit
import subprocess
import time
import pyautogui
import speech_recognition as sr 
import pyaudio
import pyttsx3
from groq import Groq
import sys 
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
SYSTEM_PROMPT = """
You are a strict intent classifier for a voice assistant.
-right now the user wants to send a message to someone 
-you just have to understand who do he want to send the message to 
-if you got whom do he wants to message then just say his/her name only 
-if you don't got whom do he wants to message then just say "not_identified"
-if the user wants to send a message to a new number then say "new_number"
-dont say anything else 
-no greetings

Contacts:
-myself
-aryan
-arpita
-maitri
-saachi/sanchi
-stuti
-navya
-naitik
-shuban/shubam
-manish sir
-shakir sir
-mummy
-papa
-didi
-chacha
-chachi
-ayansh/arav
"""
from load_api import get_api

client = Groq(api_key=get_api("groq_api"))

def ask_groq(text):
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": text}
        ],
        temperature=0  # 🔥 very important for strict output
    )

    return response.choices[0].message.content.strip()


speak("whom do you want to send message and what message should i send")
while True:
    speach_input = recognize_speech()
    if not speach_input:
        continue
    understanding = ask_groq(speach_input)
    print(understanding)
    if understanding:

        if "naitik" in understanding:
            print("sending message to naytik")
            speak("what should i say to naitik sir ?")
            message = recognize_speech()
            
            phone_number = "+9199114 36654"
            pywhatkit.sendwhatmsg_instantly(
                phone_number,
                message,
                wait_time=22,      # Wait for WhatsApp Web to load
                #tab_close=True,    # Close the tab after sending
                #close_time=3
            )
            speak("message sent succesfully.")
            sys.exit()

        elif "navya" in understanding:
            print("sending message to navya")
            speak("what should i say to navya sir ?")
            message = recognize_speech()
            
            phone_number = "+918091056792"
            pywhatkit.sendwhatmsg_instantly(
                phone_number,
                message,
                wait_time=22,      # Wait for WhatsApp Web to load
                #tab_close=True,    # Close the tab after sending
                #close_time=3
            )
            speak("message sent succesfully.")
            sys.exit()
        elif "aryan" in understanding:
            print("sending message to aryan")
            speak("what should i say to aryan sir ?")
            message = recognize_speech()
            
            phone_number = "+919205008085"
            pywhatkit.sendwhatmsg_instantly(
                phone_number,
                message,
                wait_time=22,      # Wait for WhatsApp Web to load
                #tab_close=True,    # Close the tab after sending
                #close_time=3
            )
            speak("message sent succesfully.")
            sys.exit()
        elif "stuti" in understanding:
            print("sending message to stuti")
            speak("what should i say to stuti sir ?")
            message = recognize_speech()
            
            phone_number = "+919015832487"
            pywhatkit.sendwhatmsg_instantly(
                phone_number,
                message,
                wait_time=22,      # Wait for WhatsApp Web to load
                #tab_close=True,    # Close the tab after sending
                #close_time=3
            )
            speak("message sent succesfully.")
            sys.exit()
        elif "papa" in understanding:
            speak("what should i say to your father, sir ?")
            message = recognize_speech()
            
            phone_number = "+919015966876"
            pywhatkit.sendwhatmsg_instantly(
                phone_number,
                message,
                wait_time=22,      # Wait for WhatsApp Web to load
                #tab_close=True,    # Close the tab after sending
                #close_time=3
            )
            speak("message sent succesfully.")
            sys.exit()
        elif "mummy" in understanding:
            speak("what should i say to your mother, sir ?")
            message = recognize_speech()
            
            phone_number = "+918178794800"
            pywhatkit.sendwhatmsg_instantly(
                phone_number,
                message,
                wait_time=22,      # Wait for WhatsApp Web to load
                #tab_close=True,    # Close the tab after sending
               # close_time=3
            )
            speak("message sent succesfully.")
            sys.exit()
        elif "didi" in understanding:
            speak("what should i say to your sister, sir ?")
            message = recognize_speech()
            
            phone_number = "+918700720026"
            pywhatkit.sendwhatmsg_instantly(
                phone_number,
                message,
                wait_time=22,      # Wait for WhatsApp Web to load
                #tab_close=True,    # Close the tab after sending
                #close_time=3
            )
            speak("message sent succesfully.")
            sys.exit()

        elif "myself" in understanding:
            speak("what message should i send to your number, sir ?")
            message = recognize_speech()
            
            phone_number = "+919899610964"
            pywhatkit.sendwhatmsg_instantly(
                phone_number,
                message,
                wait_time=22,      # Wait for WhatsApp Web to load
                #tab_close=True,    # Close the tab after sending
                #close_time=3
            )
            speak("message sent succesfully.")
            sys.exit()


        elif "new_number" in understanding:
            speak("what should i say to , sir ?")
            message = recognize_speech()
            
            
            phone_number = "+918091056792"
            pywhatkit.sendwhatmsg_instantly(
                phone_number,
                message,
                wait_time=25,      # Wait for WhatsApp Web to load
                #tab_close=True,    # Close the tab after sending
                #close_time=3
            )
            speak("message sent succesfully.")
            sys.exit()
        else:
            print("not able to understand the reciever's name ")
            














phone_number = "+919899610964"
message = "Hello from Python!"

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

copy_file_to_clipboard(r"C:\Users\pcper\Downloads\filessssss\z.prototype\captured_photo.png")
pyautogui.hotkey("ctrl", "v")
time.sleep(2)
pyautogui.press("enter")
