# from langchain.chat_models import ChatOpenAI
# from langchain.document_loaders import TextLoader
# from langchain.text_splitter import CharacterTextSplitter
# from langchain.embeddings.openai import OpenAIEmbeddings
# from langchain.vectorstores import Chroma
# from langchain.chains import RetrievalQA
# from langchain.agents import initialize_agent, Tool, AgentType
# from langchain.chains.conversation.memory import ConversationBufferMemory, ConversationBufferWindowMemory
# from langchain.tools import BaseTool
# from pydantic import BaseModel, Field
# from typing import Optional, Type
from datetime import datetime, timedelta
# from jinja2 import Template
# import random


from langchain.agents import initialize_agent, Tool
from langchain.chat_models import ChatOpenAI
import json
import random

import os
import re
from dotenv import load_dotenv
import redis

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

llm = ChatOpenAI(model_name="gpt-4", temperature=0, verbose=True)

redis_client = redis.Redis(host='localhost', port=6379, db=0)

def book_appointment(input_string):
    # Use regex to extract values from the input string
    pattern = r"session_id=(\d+) doctor_name=(.*?) appointment_time=(\d{2}:\d{2}) appointment_day=(\w+)"
    match = re.search(pattern, input_string)

    # Generate a random 4-digit number
    booking_id = random.randint(1000, 9999)
    
    if match:
        session_id = match.group(1)
        doctor_name = match.group(2)
        appointment_time = match.group(3)
        appointment_day = match.group(4)
        
        # Calculate the appointment_date based on today's date and the appointment_day
        today = datetime.now().date()
        days_ahead = (datetime.strptime(appointment_day, "%A").weekday() - today.weekday()) % 7
        appointment_date = today + timedelta(days=days_ahead)
        appointment_date = appointment_date.strftime("%Y-%m-%d")

        # Create a dictionary with the extracted values
        appointment_info = {
            "session_id": session_id,
            "doctor_name": doctor_name,
            "appointment_time": appointment_time,
            "appointment_date": appointment_date,
            "booking_no" : booking_id
        }
        
        redis_key = f"{session_id}_booking_info"
        json_data = json.dumps(appointment_info)
        redis_client.set(redis_key, json_data)
        
        # Return the random number
        return booking_id, appointment_time, appointment_date
    else:
        return None




book_appointment_tool = Tool(
    name="book_appointment",
    func=book_appointment,
    description="Takes an input string containing session_id, doctor_name, appointment_time, appointment_day and returns booking_id, appointment_time, appointment_day, appointment_date"
)

agent = initialize_agent([book_appointment_tool], llm, verbose=True)

input_data = {
    "input": "book_appointment session_id=1234 doctor_name=Dr. Smith appointment_time=12:00 appointment_day=Monday"
}
output_data = agent.invoke(input_data)

# Print the output
print(output_data)