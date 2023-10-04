import os
import openai
from dotenv import load_dotenv
from langchain.llms import OpenAI
from langchain import PromptTemplate
from langchain.chains import LLMChain, SimpleSequentialChain

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

prompt1 = PromptTemplate(
   input_variables=["concept"],
   template="""
           You are an expert with coding and programming.
           Explain me the concept of {concept} in a couple of lines.""",
)
chain1 = LLMChain(llm=OpenAI(model_name="text-davinci-003"), prompt=prompt1)

prompt2 = PromptTemplate(
   input_variables=["concept_name"],
   template="""
           Explain me the description of {concept_name} like the user is 5 years old""",
)
chain2 = LLMChain(llm=OpenAI(model_name="text-davinci-003"), prompt= prompt2)

chain_Final = SimpleSequentialChain ( chains=[chain1, chain2] , verbose=True)

explaination = chain_Final.run("Sum of two numbers with example of 2+2")
print(explaination)