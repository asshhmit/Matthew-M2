import speech_recognition as sr 
import pyaudio
import pyttsx3
import time 
import sys 

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

while True:
    user_input = recognize_speech()
    if not user_input:
        continue
    if user_input:
        if "protocol over" in user_input:
            speak("turning the system on again.")
            time.sleep(1)
            speak("everythings functional back again ,boss")
            sys.exit()
        else:
            print(".")