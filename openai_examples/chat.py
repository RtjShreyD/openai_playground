import os
import openai
from dotenv import load_dotenv
import pdb

load_dotenv()

openai.api_key = os.getenv("API_KEY")

response = openai.ChatCompletion.create(
  model="gpt-3.5-turbo",
  messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Who is the Prime Minister of India?"},
        {"role": "assistant", "content": "Narendra Modi is the Prime Minister of India."},
        {"role": "user", "content": "What party does he belong to?"},
    ]
)



# pdb.set_trace()

print(response)