import os
import openai
from dotenv import load_dotenv
from langchain.llms import OpenAI
from pathlib import Path
from langchain.document_loaders import TextLoader
from langchain.indexes import VectorstoreIndexCreator
from langchain.chat_models import ChatOpenAI
# Making agent perform some action
from langchain.agents import load_tools
from langchain.agents import initialize_agent

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
llm = OpenAI(temperature=0)

tools = load_tools(["terminal"], llm=llm)
print(tools[0].name, tools[0].description)

# Initializing the agent
agent = initialize_agent(tools, llm, agent="zero-shot-react-description", verbose=True)

# print(agent.agent.llm_chain.prompt.template)      #Printing default Prompt

query="Get me the size of Present Working directory on my system. You are not supposed to make any directories if they don't exists."
agent.run(query)

query2="I want you to run a file with the following command : 'python sum_func.py {num1} {num2}' , using the terminal tool and get me the result of passing the following numbers- '12' and '55'"
"""
The code in sum_func.py is given below-

import sys

def add_numbers(num1, num2):
    return num1 + num2 + 1000

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <number1> <number2>")
    else:
        try:
            number1 = float(sys.argv[1])
            number2 = float(sys.argv[2])
            result = add_numbers(number1, number2)
            print(f"The sum of {number1} and {number2} is {result}")
        except ValueError:
            print("Error: Please enter valid numbers.")
"""
agent.run(query2)