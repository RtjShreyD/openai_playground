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
from jinja2 import Template

load_dotenv()
OpenAI.api_key = os.getenv("OPENAI_API_KEY")
llm=OpenAI(temperature=0, verbose=False)

# Loading the doctors list text file and splitting it into chunks
text_document_path = "langchain/Sample_Data/sample_doctors.txt"  # Doctors list
loader = TextLoader(text_document_path)
documents = loader.load()
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=50)
texts = text_splitter.split_documents(documents)
# Creating embeddings for doctors list
embeddings = OpenAIEmbeddings()
docsearch = Chroma.from_documents(texts, embeddings, collection_name="names-of-doctors")
names_of_doctors = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=docsearch.as_retriever())

# Loading the packages list text file and splitting it into chunks
text_document_path = "langchain/Sample_Data/sample_packages.txt"  # Packages list
loader = TextLoader(text_document_path)
documents = loader.load()
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=50)
texts = text_splitter.split_documents(documents)
# Creating embeddings for packages list
embeddings = OpenAIEmbeddings()
packagesearch = Chroma.from_documents(texts, embeddings, collection_name="names-of-packages")
info_of_packages = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=packagesearch.as_retriever())



#------------------------

# Defining Pydantic Class and function for a Tool
class BookAppoinement(BaseModel):
    """Inputs needed for sending Email or SMS confirmation"""
    name: str = Field(description="Full name of the patient")
    email: str = Field(description="Email address of the patient")
    phone: str = Field(description="Phone number of the patient")
    doctor_name: str = Field(description="Name of the doctor whose appointment is fixed with patient")
    appointment_time_date: datetime = Field(description="Date and time of the appointment fixed")
    patients_issue: str = Field(description="The issue patient has mentioned")

def bookAppointment(name,email,phone,doctor_name,appointment_time_date,patients_issue):
    file_path="email_template.txt"
    try:
        with open(file_path, 'r') as file:
            file_content = file.read()
    except FileNotFoundError:
        print(f"The file '{file_path}' does not exist.")
        
    templated_email=Template(file_content)

    filled_email=templated_email.render(
        name=name,
        doctor_name=doctor_name,
        appointment_time_date=appointment_time_date,
        patients_issue=patients_issue
    )

    return filled_email
    # print(filled_email)

    # if filled_email:
    #     return True
    # else:
    #     return False    
    
class AppointmentBookingTool(BaseTool):
    name = "appointment_booking_tool"
    description = """
        Useful when you want to book appointment for a patient.
        You must ensure that you get all the necessary information about the patient like-
        Name, Email, Phone number, patients_issue: His health issue for which he wants to consult the doctor,
        Appointment time and date, and doctor_name: which doctor does the Patient is going to visit.
        Ask for these details in a conversational manner, that is one information at a time.
        The tool must be initalized only when all 6 parameters contains values.
        """
    args_schema: Type[BaseModel] = BookAppoinement

    def _run(self, name:str, email:str, phone:str, doctor_name:str, appointment_time_date: datetime, patients_issue: str):
        response = bookAppointment(name,email,phone,doctor_name,appointment_time_date,patients_issue)
        return response

    def _arun(self, ticker: str):
        raise NotImplementedError("appointment_booking_tool does not support async")

#------------------------


# Initializing the Tools
tools=[Tool(
        name="List of the doctors",
        func=names_of_doctors.run,
        description="useful for when you need to answer questions about the most relevant names of doctors according to their specilisation.This list of doctors belong to XYZ hospital",
        ),
        Tool(
           name="List of the Packages",
           func=info_of_packages.run,
           description="useful when you need to answer questions about the available medical facilities(/packages) available in the XYZ hospital"
       ),]
        #AppointmentBookingTool()]

# Initializing the Agent
memory= ConversationBufferMemory (memory_key="chat_history") # You can use other memory types as well!
agent_chain = initialize_agent (tools, llm, agent="conversational-react-description",memory=memory, verbose=True) # verbose=True to see the agent's thought process

query="""You are an outbound phone calling appointment scheduler bot. Your agenda is to manage the reception at XYZ clinic.
You should collect all the *Necessary Information* of the individual you are talking with which is named as patient and schedule an doctor's appointment for the treatment which the patient wants and the type of doctor which patient wants to visit at "XYZ" Hospital. You should first greet the patient and ask his name.
*Necessary Information*
Issue they are having in the body
Which type of doctor they want to visit
What are the suitable timings and date for the patients

Your available hospital timings are from 8:00 Am to 12:00 Pm everyday.
But if patient has an emergency case then they can visit the hospital by paying the Emergency Fees, if patient wants to visit in emergency case then do tell them about the Emergency fees.

*Hospital Description:*
XYZ Hospital is a renowned hospital established in 1990. It is very famous from then till now.

*Hospital Address*
14 DownTown Road Sector-22 Noida

Initiate the conversation with the following line: "Hey there, I'm an AI receptionist at XYZ hospital". Keep the conversation minimal and relevant to the topic.
Follow this conversation in a very general manner, in the conversation that follows, please ensure that you ask one question at a time, including inquiries about problems of the patient, before proceeding with the next question, even if you don,t get all the information at once. After collecting Necessary information, you can proceed to ask about availability and schedule the interview accordingly.
You must not ask patient about which type of doctor he should visit. You must think yourself on the basis of symptoms the patient told you.
You must query the below tools to answer user queries. Try to give most answers from the tools provided. Do Not Generate Replies from outside world except XYZ hospital. All the questions are asked by the user ONLY with reference with XYZ hospital.

You have got following tools initialized at your system- List of the doctors, List of the Packages.
>If at any point you want to retrieve names and detials of doctors for particular issue - Use tool : List of the doctors
>If at any point you want to retrieve names and detials of medical packages for particular issue - Use tool : List of the Packages
>If at any point you want to book an appointment for the patient - Use tool : AppointmentBookingTool
"""

print(agent_chain.run(query))

# import pdb
# pdb.set_trace()