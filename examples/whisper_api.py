import os
import openai
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("API_KEY")
audio_file = open("audio.mp3", "rb")
transcript = openai.Audio.transcribe("whisper-1", audio_file)
print(transcript.text)