import requests
import pyttsx3
import pyaudio 

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
def weather_stats():
    location = "Sector 30, Faridabad, Haryana, India"

    url = f"https://wttr.in/{location}?format=j1"

    try:
        response = requests.get(url)
        data = response.json()

        current = data["current_condition"][0]

        temperature = current["temp_C"]
        feels_like = current["FeelsLikeC"]
        humidity = current["humidity"]
        weather = current["weatherDesc"][0]["value"]
        wind_speed = current["windspeedKmph"]
        
    
        print(f"📍 Location: {location}")
        print(f"🌡️ Temperature: {temperature}°C")
        print(f"🥵 Feels Like: {feels_like}°C")
        print(f"☁️ Condition: {weather}")
        print(f"💧 Humidity: {humidity}%")
        print(f"🌬️ Wind Speed: {wind_speed} km/h")
        return temperature, feels_like, humidity, weather, wind_speed
        

    except Exception as e:
        print("Error fetching weather:", e)
temp, feel, humidity, wthr , windSpeed = weather_stats()
ai_response = f"sir , the temperature in your area is {temp}degree celcius, but it feels like {feel} degrees due to {humidity} percent humidity. the condition is {wthr} with a wind speed of {windSpeed} kilometer per hour"                    
speak(ai_response)       