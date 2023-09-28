import os
import openai
from dotenv import load_dotenv
from langchain.llms import OpenAI
from gpt4all import GPT4All
from pathlib import Path
from langchain.document_loaders import TextLoader
from langchain.indexes import VectorstoreIndexCreator
from langchain.chat_models import ChatOpenAI

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# LocalGPModel = GPT4All
# model = GPT4All("orca-mini-3b.ggmlv3.q4_0.bin", allow_download=False)
# model_path = Path.home()/"home"/"sarthaksharma"/".cache"/"gpt4all"

query = "I've pain in my bone, Which doctor should I visit? List me the name of doctors"
print(query)

loader = TextLoader("Sample_Data/sample_doctors.txt")
text=loader.load()
index = VectorstoreIndexCreator().from_loaders([loader])

print(index.query(query, llm=ChatOpenAI())) # LLM wrapper
# print(model.generate(query, max_tokens=150))