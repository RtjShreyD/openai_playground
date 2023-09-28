import os
import openai
from dotenv import load_dotenv
from langchain.llms import OpenAI
from langchain import PromptTemplate
from langchain.chains import LLMChain, SimpleSequentialChain

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

prompt = PromptTemplate(input_variables=["concept"], template="""
           You are an expert with coding and programming.
           Explain me the concept of {concept} in a couple of lines.""")
chain = LLMChain(llm=OpenAI(model_name="text-davinci-003"), prompt=prompt)
explaination = chain.run("Multiplication")

#----------------------------------------------------------------
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings     
import pinecone         # Pinecone is a vector database/ Vector Indexing
from langchain.vectorstores import Pinecone   

text_splitter = RecursiveCharacterTextSplitter(
   chunk_size=200, 
   chunk_overlap = 10,
)

text = text_splitter.create_documents([explaination])
# print(text)
line1= text[0].page_content
# print(line1)

embeddings = OpenAIEmbeddings(model_name="ada")
query_result_vector = embeddings.embed_query(line1)  # data converted into vector form
# print(query_result_vector)

# initialize Pinecone
pinecone.init(
   api_key=os.getenv("PINECONE_API_KEY"),
   environment=os.getenv("PINECONE_ENVIRONMENT")
)

index_name="langchain-quickstart"
search = Pinecone.from_documents(text, embeddings, index_name=index_name)

query_p = "What is sum of 2+2"
result = search.similarity_search(query_p)
print(result)