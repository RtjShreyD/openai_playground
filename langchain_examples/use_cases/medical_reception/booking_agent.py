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
# from datetime import datetime, timedelta
# from jinja2 import Template
# import random


from langchain.agents import initialize_agent, Tool
from langchain.chat_models import ChatOpenAI
import json
import random

import os
import re
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

llm = ChatOpenAI(model_name="gpt-4", temperature=0, verbose=True)

def book_appointment(input_string):
    # Use regex to extract values from the input string
    pattern = r"session_id=(\d+) doctor_name=(.*?) appointment_time=(\d{2}:\d{2}) appointment_date=(\d{4}-\d{2}-\d{2})"
    match = re.search(pattern, input_string)
    
    if match:
        session_id = match.group(1)
        doctor_name = match.group(2)
        appointment_time = match.group(3)
        appointment_date = match.group(4)
        
        # Create a dictionary with the extracted values
        appointment_data = {
            "session_id": session_id,
            "doctor_name": doctor_name,
            "appointment_time": appointment_time,
            "appointment_date": appointment_date
        }
        
        # Check if the JSON file exists
        try:
            with open("appointments.json", "r") as file:
                appointments = json.load(file)
        except FileNotFoundError:
            appointments = []
        
        # Add the new appointment data to the list
        appointments.append(appointment_data)
        
        # Write the updated list to the JSON file
        with open("appointments.json", "w") as file:
            json.dump(appointments, file)
        
        # Generate a random 4-digit number
        random_number = random.randint(1000, 9999)
        
        # Return the random number
        return random_number
    else:
        return None




book_appointment_tool = Tool(
    name="book_appointment",
    func=book_appointment,
    description="Stores appointment details in a JSON file and returns a random 4-digit number"
)

agent = initialize_agent([book_appointment_tool], llm)

input_data = {
    "input": "book_appointment session_id=123 doctor_name=Dr. Smith appointment_time=10:00 appointment_date=2022-12-31"
}
output_data = agent.invoke(input_data)

# Print the output
print(output_data["output"])