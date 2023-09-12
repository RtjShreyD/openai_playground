import os
import sys

import openai
import playsound
import speech_recognition as sr

from typing import Text
from gtts import gTTS
import pyttsx3

from dotenv import load_dotenv

load_dotenv()

r = sr.Recognizer()
openai.api_key = os.getenv("API_KEY")


def text_to_voice_gtts(text: str):
    # Using the gTTS engine
    accent = 'com.au'
    filename = "tmp.mp3"
    tts = gTTS(text, tld=accent)
    tts.save(filename)
    playsound.playsound(filename)
    os.remove(filename)


def text_to_voice_native(text: str):
    engine = pyttsx3.init()
    engine.setProperty('rate', 125)
    engine.say(text)
    engine.runAndWait()


def get_gpt_response(prompt: str) -> Text:
    chat_gpt3_model_engine = "text-davinci-003"
    results = []
    
    # Stream response from ChatGpt
    for resp in openai.Completion.create(engine=chat_gpt3_model_engine, prompt=prompt, max_tokens=512, n=1, stop=None, temperature=0.5, stream=True):
        text = resp.choices[0].text
        results.append(text)
        sys.stdout.write(text)
        sys.stdout.flush()

    return "".join(results)


def main():
    while True:
        try:
            with sr.Microphone() as source2:
                print("Mic open start speak...")
                
                # adjust noises, wait for 0.2s and start listening
                r.adjust_for_ambient_noise(source2, duration=0.2)
                audio2 = r.listen(source2)

                # Using google speech engine for speech to text conversion
                input_prompt = r.recognize_google(audio2)
                input_prompt = input_prompt.lower()

                print("User :", input_prompt)
                prompt_resp_text = get_gpt_response(input_prompt)

                # Uncomment below to speak via the gtts engine (latency high, quality high)
                # text_to_voice_gtts(prompt_resp_text)

                # Using the native pyttsx engine (latency low, quality low)
                text_to_voice_native(prompt_resp_text)

        except Exception as e:
            print("Unable to request results from ChatGPT - {0}".format(e))


if __name__ == '__main__':
    device_microphones = sr.Microphone.list_microphone_names()
    if device_microphones:
        for index, name in enumerate(device_microphones):
            print("Mic - \"{}\" found, audio_input_device({})".format(index, name))
        main()
    else:
        print("No audio input devices found")