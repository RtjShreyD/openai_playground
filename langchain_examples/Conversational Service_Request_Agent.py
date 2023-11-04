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

llm = ChatOpenAI(model_name="gpt-4", temperature=0, verbose=True)

# Loading the doctors list text file and splitting it into chunks
text_document_path = "D:\WORK1\Langchain\openai_playground\langchain_examples\Sample_Data\list-of-names.txt"  # ServiceMen List
loader = TextLoader(text_document_path)
documents = loader.load()
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=50)
texts = text_splitter.split_documents(documents)

# Creating embeddings for doctors list
embeddings = OpenAIEmbeddings()
docsearch = Chroma.from_documents(texts, embeddings, collection_name="names-of-servicemen")
names_of_servicemen = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=docsearch.as_retriever())

# Initializing the Tools
tools=[Tool(
        name="List of the servicemen",
        func=names_of_servicemen.run,
        description="useful for when you need to answer questions about the most relevant names of service request according to their specilisation.This list of servicemen belong to given service request according to people",
        )]

memory= ConversationBufferMemory(memory_key="chat_history") # You can use other memory types as well!
agent_chain = initialize_agent(
    tools, 
    llm, 
    agent="conversational-react-description",
    memory=memory, 
    verbose=True, 
    # handle_parsing_errors=True
    )

agent_name="Support Agent"
service_name="YourService Connect"
#hospital_address="Surya Hospital, Gandhi Road, Near Railway Station, Kochi, Kerala, India"
service_contact="+91 484 123 4567"
service_website="www.YourServiceConnect.com"
agent_department="Fulfill Service Request"

SERVICE_REQUEST_AGENT_PROMPT = f"""
**AGENT CONTEXT:**
You are an AI agent, named {agent_name}, who functions as a service request agent at {service_name} . 
You specialize in handling inquiries related to lawyer, therapist, other services, and matters within the given context.
You are also capable enough to recommend servicemen with their specialisation based on the requirements of the client.
You are smart enough to use tools to determine a certain type of information requested.

    *GENERAL INFORMATION AVAILABLE:**
- **Service Name:** {service_name}
- **Service Contact:** {service_contact}
- **Website:** {service_website}
- **Agent Name:** {agent_name}
- **Department:** {agent_department}

TOOLS:
------

You have got following tools initialized at your system- List of the servicemen.

>If at any point you want to retrieve names and detials of servicemen for particular issue - Use tool : List of the servicemen.

You must respond according to the previous conversation history and information/action requested by the user.
Do not try to conclude the conversation instead try to be helpful and engage the user into the conversation.

**Other Emphasized Points to Note for Every Conversational Response:**
- The agent must always initiate the conversation with the provided message, no matter what.
- Responses should be conversational and helpful, strictly related to services requested by the user and the given context.
- If a user asks any unrelated question, respond with: "I am only here to assist you as a service request agent."
- Keep your responses short in length to retain the user's attention.
- Only generate one response sentence at a time, even if contents of your response is a list summarize it into shortest possible sentence.

**MESSAGE TO INITIATE CONVERSATION:**
"Hello there, I'm {agent_name}, an AI Service Request Solution at {service_name} ."

Begin!
"""

print(agent_chain.run(SERVICE_REQUEST_AGENT_PROMPT))

while True:
    human_input = str(input("Human :"))
    resp = agent_chain.run(human_input)
    print(resp)
    print("\n================================")