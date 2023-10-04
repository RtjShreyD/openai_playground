import os
import openai
import signal
import sys
import time
import pdb
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("API_KEY")
model_engine = "gpt-3.5-turbo" # you can change this to any other engine like "curie" or "babbage"

session_messages = [
    {"role": "system", "content": "You are a helpful assistant."},
]

def signal_handler(sig, frame):
    print('\nSession cancelled.')
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

def get_response(input_text):
    global session_messages
    
    prompt = session_messages.copy()
    prompt.append({"role": "user", "content": input_text})
    
    try:
        response = openai.ChatCompletion.create(
            model=model_engine,
            messages=prompt,
            temperature=0.7,
            max_tokens=1024,
            stop=None,
            timeout=60,
        )

        message = response.choices[0]['message']['content']
        session_messages.append({"role": "assistant", "content": message})
        
    except openai.error.RateLimitError:
        print('============= Rate limit reached. Waiting for 20 seconds... =================')
        time.sleep(20)
        message = "Please send your message again...."
    
    return message

while True:
    try:
        print('-----------------------------------------------------')
        user_input = input("You: ")
        response = get_response(user_input)
        print("Assistant: {}".format(response))
        print('-----------------------------------------------------')
    
    except KeyboardInterrupt:
        signal_handler(signal.SIGINT, None)
