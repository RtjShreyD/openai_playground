from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.agents import initialize_agent, Tool
from langchain.chains.conversation.memory import ConversationBufferMemory, ConversationBufferWindowMemory
from datetime import datetime, timedelta

import re
import json
import random
import redis

import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

llm = ChatOpenAI(model_name="gpt-4", temperature=0, verbose=True)

redis_client = redis.Redis(host='localhost', port=6379, db=0)

def parse_time(appointment_time):
    # Regular expression to match various time formats
    time_pattern = r"(\d{1,2}):(\d{2})(AM|PM)?"
    match = re.match(time_pattern, appointment_time, re.IGNORECASE)
    
    if match:
        hours, minutes, period = match.groups()
        hours = int(hours)
        minutes = int(minutes)
        
        if period and period.lower() == 'pm' and hours != 12:
            hours += 12
        elif period and period.lower() == 'am' and hours == 12:
            hours = 0
        
        return f"{hours:02d}:{minutes:02d}"
    else:
        raise ValueError("Invalid appointment_time format")


def book_appointment(input_data):
    try:
        input_data = json.loads(input_data)

        session_id = input_data.get('session_id')
        doctor_name = input_data.get('doctor_name')
        appointment_time = parse_time(input_data.get('appointment_time'))
        appointment_day = input_data.get('appointment_day')
        
        # Validate session_id, doctor_name, and appointment_time
        if not session_id or not doctor_name or not appointment_time:
            raise ValueError("Invalid session_id, doctor_name, or appointment_time")
        
        # Deduce appointment_day and appointment_date
        if not appointment_day:
            today = datetime.now().date()
            appointment_day = today.strftime("%A")
        
        # Calculate the appointment_date based on today's date and the appointment_day
        days_ahead = (datetime.strptime(appointment_day, "%A").weekday() - datetime.now().weekday()) % 7
        appointment_date = (datetime.now() + timedelta(days=days_ahead)).strftime("%Y-%m-%d")
        
        # Generate a random 4-digit number for booking ID
        booking_id = random.randint(1000, 9999)
        
        # Store appointment information in Redis
        appointment_info = {
            "session_id": session_id,
            "doctor_name": doctor_name,
            "appointment_time": appointment_time,
            "appointment_date": appointment_date,
            "booking_no": booking_id
        }
        redis_key = f"{session_id}_booking_info"
        json_data = json.dumps(appointment_info)
        redis_client.set(redis_key, json_data)
        
        return f"Appointment scheduled, booking_id is {booking_id}, date is {appointment_date}, time is {appointment_time}"
    
    except ValueError as e:
        return str(e) + ", please confirm the details from the user and try again later"
    
    except Exception as e:
        return "Some error occurred, please try again later"


# ==================================================================


# Loading the doctors list text file and splitting it into chunks
text_document_path = "/home/rtj/Projects/openai_playground/langchain_examples/Sample_Data/sample_doctors.txt"  # Doctors list
loader = TextLoader(text_document_path)
documents = loader.load()
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=50)
texts = text_splitter.split_documents(documents)

# Creating embeddings for doctors list
embeddings = OpenAIEmbeddings()
docsearch = Chroma.from_documents(texts, embeddings, collection_name="names-of-doctors")
names_of_doctors = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=docsearch.as_retriever())


# Loading the packages list text file and splitting it into chunks
text_document_path = "/home/rtj/Projects/openai_playground/langchain_examples/Sample_Data/sample_packages.txt"  # Packages list
loader = TextLoader(text_document_path)
documents = loader.load()
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=50)
texts = text_splitter.split_documents(documents)

# Creating embeddings for packages list
embeddings = OpenAIEmbeddings()
packagesearch = Chroma.from_documents(texts, embeddings, collection_name="names-of-packages")
info_of_packages = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=packagesearch.as_retriever())

agent_name="Uday"
session_id="ACOMPLEXSESSIONID"
hospital_name="Surya Hospital"
today_date = datetime.today().strftime('%Y-%m-%d')
day_of_week = datetime.today().strftime('%A')

hospital_address="Surya Hospital, Gandhi Road, Near Railway Station, Kochi, Kerala, India"
hospital_phone="+91 484 123 4567"
hospital_website="www.suryahospital.com"
agent_department="General Inquiry"


# Initializing the Tools
tools=[Tool(
        name="List of the doctors",
        func=names_of_doctors.run,
        description="useful for when you need to answer questions about the most relevant names of doctors according to their specilisation.This list of doctors belong to given medical facility only.",
        ),
        Tool(
           name="List of the Packages",
           func=info_of_packages.run,
           description="useful when you need to answer questions about the available medical facilities(/packages) available in the given medical facility."
       ),
       Tool(
            name="book_appointment",
            func=book_appointment,
            description='''
                Useful for starting appointment booking procedure. 
                Takes a single input dictionary containing session_id, doctor_name, appointment_time, appointment_day.
                Make sure to convert the appointment_time to 24hr time format or HH:MM AM/PM format before calling this function.
                Returns booking_id, appointment_time, appointment_day, appointment_date contained in a string.
                '''
        )]


CONVERSATIONAL_AGENT_PROMPT = f"""
**AGENT CONTEXT:**
You are an AI agent, named {agent_name}, who functions as a receptionist at {hospital_name} Hospital. 
You specialize in handling inquiries related to health, doctors, hospital services, and matters within the given context.
You are also capable enough to recommend doctors with their specialisation based on the symptoms of the patient.
You are smart enough to use tools to determine a certain type of information requested.

**GENERAL INFORMATION AVAILABLE:**
- **Session_Id:** {session_id}
- **Today's Date:** {today_date}
- **Day of the Week**: {day_of_week}
- **Hospital Name:** {hospital_name}
- **Address:** {hospital_address}
- **Phone Number:** {hospital_phone}
- **Website:** {hospital_website}
- **Agent Name:** {agent_name}
- **Department:** {agent_department}

TOOLS:
------

You have got following tools initialized at your system- List of the doctors, List of the Packages.

>If at any point you want to retrieve names and detials of doctors for particular issue - Use tool : List of the doctors
>If at any point you want to retrieve names and detials of medical packages for particular issue - Use tool : List of the Packages


You must respond according to the previous conversation history and information/action requested by the user.
Do not try to conclude the conversation instead try to be helpful and engage the user into the conversation.

**Other Emphasized Points to Note for Every Conversational Response:**
- The agent must always initiate the conversation with the provided message, no matter what.
- Responses should be conversational and helpful, strictly related to health, doctors, hospital services, and the given context.
- If a user asks any unrelated question, respond with: "I am only here to assist you as a hospital receptionist."
- Keep your responses short in length to retain the user's attention.
- Only generate one response sentence at a time, even if contents of your response is a list summarize it into shortest possible sentence.

**MESSAGE TO INITIATE CONVERSATION:**
"Hello there, I'm {agent_name}, an AI receptionist at {hospital_name} Hospital."

Begin!
"""


# memory = ConversationBufferWindowMemory(
#     memory_key='chat_history',
#     k=3,
#     return_messages=True
# )

memory= ConversationBufferMemory(memory_key="chat_history")
conversational_agent_chain = initialize_agent(
    tools, 
    llm, 
    agent="conversational-react-description",
    memory=memory, 
    verbose=True
    )


print(conversational_agent_chain.run(CONVERSATIONAL_AGENT_PROMPT))

while True:
    human_input = str(input("Human :"))
    resp = conversational_agent_chain.run(human_input)
    print(resp)
    print("\n================================")