from dotenv import load_dotenv
import openai
import os
from langchain import OpenAI
from langchain.chat_models import ChatOpenAI
from configs.config import configs
from langchain.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.agents import initialize_agent, Tool, AgentType
from langchain.chains.conversation.memory import ConversationBufferMemory
from langchain.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Optional, Type
from datetime import datetime, timedelta


load_dotenv()
OpenAI.api_key = os.getenv("OPENAI_API_KEY")
llm=OpenAI(temperature=0, verbose=True)

# Loading the doctors list text file and splitting it into chunks
text_document_path = "Sample_Data/sample_doctors.txt"  # Doctors list
loader = TextLoader(text_document_path)
documents = loader.load()
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=50)
texts = text_splitter.split_documents(documents)

# Creating embeddings for doctors list
embeddings = OpenAIEmbeddings()
docsearch = Chroma.from_documents(texts, embeddings, collection_name="names-of-doctors")
names_of_doctors = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=docsearch.as_retriever())

# Initializing the Tools
tools=[Tool(
        name="List of the doctors",
        func=names_of_doctors.run,
        description="useful for when you need to answer questions about the most relevant names of doctors according to their specilisation.This list of doctors belong to XYZ hospital",
        ),]

# Initializing the Agent
memory= ConversationBufferMemory (memory_key="chat_history") # You can use other memory types as well!
agent_chain = initialize_agent (tools, llm, agent="conversational-react-description",memory=memory, verbose=True) # verbose=True to see the agent's thought process

query="""You are an outbound phone calling appointment scheduler bot. Your agenda is to manage the reception at XYZ clinic.
You should collect all the *Necessary Information* of the individual you are talking with which is named as patient and schedule an doctor's appointment for the treatment which the patient wants and the type of doctor which patient wants to visit at "XYZ" Hospital. You should first greet the patient and ask his name.
*Necessary Information*
Issue they are having in the body
What are the suitable timings and date for the patients

You must not ask patient about which type of doctor he should visit. You must think yourself on the basis of symptoms the patient told you.
You must query the below tools to answer user queries. Try to give most answers from the tools provided. Do Not Generate Replies from outside world except XYZ hospital. All the questions are asked by the user ONLY with reference with XYZ hospital.

You have got following tools initialized at your system- List of the doctors, List of the Packages.
>If at any point you want to retrieve names and detials of doctors for particular issue - Use tool : List of the doctors
"""

print(agent_chain.run(query))

# import pdb
# pdb.set_trace()