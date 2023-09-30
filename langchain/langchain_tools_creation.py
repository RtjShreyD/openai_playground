from langchain.chat_models import ChatOpenAI
from langchain.chains import create_tagging_chain, create_tagging_chain_pydantic, TransformChain, LLMChain, SimpleSequentialChain
from langchain.prompts import ChatPromptTemplate, PromptTemplate
from langchain.llms import OpenAI
from dotenv import load_dotenv
import openai
import os
from enum import Enum
from pydantic import BaseModel, Field
from typing import Optional, Type
from datetime import datetime, timedelta
from langchain.tools import BaseTool
from langchain.agents import AgentType
from langchain.chat_models import ChatOpenAI
from langchain.agents import initialize_agent

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo-0613")

def special_sum(n1,n2):
    res=int(n1)+int(n2)+100
    return res

class Special_Sum(BaseModel):
    """Inputs for special_sum operation"""
    num1: int = Field(description="Input number 1")
    num2: int = Field(description="Input number 2")

class SpecialSumTool(BaseTool):
    name = "special_sum_tool"
    description = """
        Useful when you want to add two numbers by special sum method.
        """
    args_schema: Type[BaseModel] = Special_Sum

    def _run(self, num1:int, num2: int):
        response = special_sum(num1, num2)
        return response

    def _arun(self, ticker: str):
        raise NotImplementedError("get_stock_performance does not support async")
    
tools=[SpecialSumTool()]
agent = initialize_agent(tools, llm, agent=AgentType.OPENAI_FUNCTIONS, verbose=True)
agent.run("What is the special sum of 2 and 4")