import speech_recognition as sr
import os
from dotenv import load_dotenv

load_dotenv()

# obtain audio from the microphone
r = sr.Recognizer()
with sr.Microphone() as source:
    print("Say something!")
    audio = r.listen(source)


# recognize speech using Whisper API
OPENAI_API_KEY = os.getenv("API_KEY")

try:
    print(f"{r.recognize_whisper_api(audio, api_key=OPENAI_API_KEY)}")
except sr.RequestError as e:
    print("Could not request results from Whisper API")