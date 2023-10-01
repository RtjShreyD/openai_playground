from configs.config import configs
from langchain import OpenAI 
from langchain.chat_models import ChatOpenAI
# from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain.agents import initialize_agent
from langchain.agents import Tool
# from langchain.tools import BaseTool
from langchain.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.chains.conversation.memory import ConversationBufferMemory

OpenAI.api_key = configs.get("OPENAI_API_KEY")

# Set up the turbo LLM
turbo_llm = ChatOpenAI(
    temperature=0,
    model_name='gpt-3.5-turbo',
    verbose=True
)

embeddings = OpenAIEmbeddings()

# Loading the doctors list text file and splitting it into chunks
text_document_path = "Sample_Data/sample_doctors.txt"  # Doctors list
loader = TextLoader(text_document_path)
documents = loader.load()
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=50)
texts = text_splitter.split_documents(documents)

# Creating embeddings for doctors list
docsearch = Chroma.from_documents(texts, embeddings, collection_name="names-of-doctors")
names_of_doctors = RetrievalQA.from_chain_type(llm=turbo_llm, chain_type="stuff", retriever=docsearch.as_retriever())

# Loading the packages list text file and splitting it into chunks
text_document_path = "Sample_Data/sample_packages.txt"  # Packages list
loader = TextLoader(text_document_path)
documents = loader.load()
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=50)
texts = text_splitter.split_documents(documents)

packagesearch = Chroma.from_documents(texts, embeddings, collection_name="names-of-packages")
info_of_packages = RetrievalQA.from_chain_type(llm=turbo_llm, chain_type="stuff", retriever=packagesearch.as_retriever())

import os
import json

def book_patient_appointment(details):
    try:
        if not isinstance(details, dict):
            return "Aborting...Details not parsable."

        if not os.path.exists('appointments'):
            os.makedirs('appointments')
        
        file_path = 'appointments/appointments.json'

        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                appointments_list = json.load(file)
        else:
            appointments_list = []

        appointments_list.append(details)
        
        with open(file_path, 'w') as file:
            json.dump(appointments_list, file, indent=4)
        
        return "Appointment booked successfully!"

    except Exception as e:
        return "Unexpected error occured while trying to book. Please try again later."
    


name = "book_an_appointment"
description = '''Useful when you need to book/schedule an appointment for a patient with a doctor at your premises
        Input should be a json string in the following format -
        "{
                'patient_name' : <patient_name>,
                'patient_email' : <patient_email>,
                'patient_phone' : <patient_phone_number>,
                'patient_case' : <patient_case_description>,
                'doctor_name' : <name_of_doctor_to_visit>,
                'department_name' : <department_name>,
                'appointment_date' : <date_of_appointment_in_dd/mm/yy>,
                'appointment_time' : <time_of_appointment_in_hh:mm am/pm>,
                'send_email' : <whether_to_send_email_or_not>,
                'send_sms' : <whether_to_send_sms_or_not>
        }"
        You must ensure that you get all the necessary information about the patient and appointment mentioned above before using this tool.
        Ask for these details in a conversational manner, that is one information at a time.
        The tool must be initalized only when all 10 parameters contains values.'''

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
       ),
       Tool(name=name, func=book_patient_appointment, description=description)]

memory= ConversationBufferMemory(memory_key="chat_history")
agent_chain = initialize_agent(tools, turbo_llm, agent="conversational-react-description",memory=memory, verbose=True)

fixed_prompt = """You are Kyle, an outbound phone calling appointment scheduler bot.

Your agenda is to manage the reception at XYZ clinic. 

You are capable enough to provide them general information regarding which doctors from your clinic they should visit based on their symptoms and 

While conversing with the individual, if at any time the individual or patient needs to schedule a doctor's appointment, you should collect all the *Necessary Information* of the individual you are talking with which is named as patient and schedule an doctor's appointment for the treatment which the patient wants and the type of doctor which patient wants at your hospital. 
In that case you should first greet the patient and ask or confirm his name. Then continue to gather all the *Necessary Information* one by one in a conversational manner.

*Necessary Information*
- patient_name
- patient_email
- patient_phone number
- patient_case_description
- doctor_name
- department_name
- appointment_date
- appointment_time
- whether_to_send_email_confirmation
- whether_to_send_sms_confirmation

You should initiate the conversation with the following line: 
 "Hi I am Kyle, an AI chatbot talking on behalf of XYZ clinic, please let me know how may I help you ?".

Your available hospital timings are from 8:00 Am to 10:00 Pm everyday.
But if patient has an emergency case then they can visit the hospital by paying the Emergency Fees, if patient wants to visit in emergency case then do tell them about the Emergency fees ie 2000 INR.

*Hospital Description:*
XYZ Hospital is a renowned hospital established in 1990. It was established by Dr XYZ, for catering the need to quality medical treatment accross the city of Noida.

*Hospital Address*
14 DownTown Road Sector-22 Noida

You must not ask patient about which type of doctor he should visit. You must think yourself on the basis of symptoms the patient told you.
Try to give most answers from the tools provided. Do Not Generate Replies from outside world except XYZ hospital. All the questions are asked by the user ONLY with reference with XYZ hospital."""

print(agent_chain.run(fixed_prompt))

import pdb
pdb.set_trace()
