import os
from dotenv import load_dotenv
import openai
from langchain.agents import initialize_agent  #initialize the agents from langchain.agents
from langchain.agents import load_tools        #Loading the tools from langchain.agents
from langchain.llms import OpenAI
#llm =_OpenAI()
#load_dotenv()
#openai.api_key =os.getenv("OPENAI_API_KEY")    #your openai_api_key
llm =OpenAI()
tool_names=["llm-math"]                        #we are using math model of llm for calculations
tools=load_tools(tool_names, llm=llm)

agent= initialize_agent(
    tools=tools, llm=llm, agent="zero-shot-react-description", verbose=True
)
agent.run("What is 15 multiplied by 15")   #prompt to be provided that what basically you want from AI to provide you back.