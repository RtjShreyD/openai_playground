# Prompt Template
import os
import openai
from dotenv import load_dotenv
from langchain.llms import OpenAI
from langchain import PromptTemplate

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

llm = OpenAI(model_name="text-davinci-003")

template = """
You are an expert with engineering concepts.
Explain me the concept of {concept} in a couple of lines."""

prompt = PromptTemplate(
   input_variables=["concept"],
   template=template,
)

print(llm(prompt.format(concept="Factorial")))