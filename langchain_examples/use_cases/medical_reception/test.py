from langchain.agents import initialize_agent, AgentType, AgentExecutor
from langchain.memory import ConversationBufferMemory
from langchain.chat_models import ChatOpenAI
from langchain import OpenAI
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
import os
from dotenv import load_dotenv

load_dotenv()

OpenAI.api_key = os.getenv("OPENAI_API_KEY")

# Sample data (replace these with actual data)
agent_random_name = "Dude"
hospital_random_name = "HealthCare Hospital"
hospital_random_address = "123 Medical Avenue, Cityville"
hospital_random_phone = "123-456-7890"
hospital_random_website = "www.healthcare-hospital.com"
agent_random_department = "Reception"

# Jinja template string
template = """
**AGENT CONTEXT:**
This AI agent, named {}, functions as a receptionist at {} Hospital. It specializes in handling inquiries related to health, doctors, hospital services, and matters within the given context.

**GENERAL INFORMATION AVAILABLE:**
- **Hospital Name:** {}
- **Address:** {}
- **Phone Number:** {}
- **Website:** {}
- **Agent Name:** {}
- **Department:** {}

**MESSAGE TO INITIATE CONVERSATION:**
"Hello there, I'm {}, an AI receptionist at {} Hospital."

**Other Emphasized Points to Note for Every Conversational Response:**
- The agent must always initiate the conversation with the provided message.
- Responses should be conversational and helpful, strictly related to health, doctors, hospital services, and the given context.
- If a user asks any unrelated question, respond with: "I am only here to assist you as a hospital receptionist."
"""


# Format the template with the provided data
formatted_template = template.format(agent_random_name, hospital_random_name, hospital_random_name,
                                     hospital_random_address, hospital_random_phone, hospital_random_website,
                                     agent_random_name, agent_random_department, agent_random_name, hospital_random_name)

# Create the buffer memory
memory= ConversationBufferMemory(memory_key="chat_history")

# Create the language model
llm = ChatOpenAI(model_name='gpt-4', temperature=0)

# Create the agent
agent = initialize_agent(
    tools = [],
    llm = llm,
    agent = AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
    memory = memory,
    verbose = True,
    agent_kwargs = {"extra_prompt_messages": [MessagesPlaceholder(variable_name="chat_history")]}
)


resp = agent.run(formatted_template)
print(resp)

while True:
    user_input = str(input("User: "))
    response = agent.run(user_input)
    print("Agent:", response)