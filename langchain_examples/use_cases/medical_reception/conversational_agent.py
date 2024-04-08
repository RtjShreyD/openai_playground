from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.agents import initialize_agent, Tool, AgentType
from langchain.chains.conversation.memory import ConversationBufferMemory, ConversationBufferWindowMemory
from langchain.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Optional, Type
from datetime import datetime, timedelta
from jinja2 import Template

import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0, verbose=True)

# Loading the doctors list text file and splitting it into chunks
text_document_path = "./langchain_examples/Sample_Data/sample_doctors.txt"  # Doctors list
loader = TextLoader(text_document_path)
documents = loader.load()
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=50)
texts = text_splitter.split_documents(documents)

# Creating embeddings for doctors list
embeddings = OpenAIEmbeddings()
docsearch = Chroma.from_documents(texts, embeddings, collection_name="names-of-doctors")
names_of_doctors = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=docsearch.as_retriever())


# Loading the packages list text file and splitting it into chunks
text_document_path = "./langchain_examples/Sample_Data/sample_packages.txt"  # Packages list
loader = TextLoader(text_document_path)
documents = loader.load()
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=50)
texts = text_splitter.split_documents(documents)

# Creating embeddings for packages list
embeddings = OpenAIEmbeddings()
packagesearch = Chroma.from_documents(texts, embeddings, collection_name="names-of-packages")
info_of_packages = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=packagesearch.as_retriever())


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
       )]

memory = ConversationBufferWindowMemory(
    memory_key='chat_history',
    k=3,
    return_messages=True
)


# memory= ConversationBufferMemory(memory_key="chat_history") # You can use other memory types as well!
agent_chain = initialize_agent(
    tools, 
    llm, 
    agent="conversational-react-description",
    memory=memory, 
    verbose=True, 
    handle_parsing_errors=True      # Used with GPT 3.5
    )


agent_name="Uday"
hospital_name="Surya Hospital"
hospital_address="Surya Hospital, Gandhi Road, Near Railway Station, Kochi, Kerala, India"
hospital_phone="+91 484 123 4567"
hospital_website="www.suryahospital.com"
agent_department="General Inquiry"


RECEPTION_AGENT_PROMPT = f"""
**AGENT CONTEXT:**
You are an AI agent, named {agent_name}, who functions as a receptionist at {hospital_name} Hospital. 
You specialize in handling inquiries related to health, doctors, hospital services, and matters within the given context.
You are also capable enough to recommend doctors with their specialisation based on the symptoms of the patient.
You are smart enough to use tools to determine a certain type of information requested.

**GENERAL INFORMATION AVAILABLE:**
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

print(agent_chain.run(RECEPTION_AGENT_PROMPT))

while True:
    human_input = str(input("Human :"))
    resp = agent_chain.run(human_input)
    print(resp)
    print("\n================================")