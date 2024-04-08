import os
import sys
import time

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
session_messages = [
    {"role": "system", "content": "You are a helpful assistant."},
]


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

def get_response(input_text):
    chat_gpt3_model_engine = "gpt-3.5-turbo" # this is the replacemenet model of davinci
    global session_messages
    
    prompt = session_messages.copy()
    prompt.append({"role": "user", "content": input_text})
    
    try:
        # import pdb
        # pdb.set_trace()
        response = openai.chat.completions.create(
            model=chat_gpt3_model_engine,
            messages=prompt
        )
        # print(response.choices[0].message.content)
        message = response.choices[0].message.content
        session_messages.append({"role": "assistant", "content": message})
        
    except Exception as e:
        print(e)
        print('============= Rate limit reached. Waiting for 20 seconds... =================')
        time.sleep(20)
        message = "Please send your message again...."
    
    return message

def get_gpt_response(prompt: str) -> Text:
    chat_gpt3_model_engine = "gpt-3.5-turbo-instruct" # this is the replacemenet model of davinci
    results = []
    # import pdb
    # pdb.set_trace()
    print(prompt)
    # Stream response from ChatGpt
    for resp in openai.chat.completions.create(model=chat_gpt3_model_engine, messages=prompt, stream=True):
        text = resp.choices[0].message
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
                prompt_resp_text = get_response(input_prompt)
                print(prompt_resp_text)

                # Uncomment below to speak via the gtts engine (latency high, quality high)
                text_to_voice_gtts(prompt_resp_text)

                # Using the native pyttsx engine (latency low, quality low)
                # text_to_voice_native(prompt_resp_text)

        except Exception as e:
            print("Unable to request results from ChatGPT - {0}".format(e))


if __name__ == '__main__':
    # response = get_response("Hello")
    device_microphones = sr.Microphone.list_microphone_names()
    if device_microphones:
        for index, name in enumerate(device_microphones):
            print("Mic - \"{}\" found, audio_input_device({})".format(index, name))
        main()
    else:
        print("No audio input devices found")
        
