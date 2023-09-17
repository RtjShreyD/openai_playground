from langchain.document_loaders import WebBaseLoader


loader = WebBaseLoader("https://lilianweng.github.io/posts/2023-06-23-agent/")
data = loader.load()

from langchain.text_splitter import RecursiveCharacterTextSplitter

text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=0)
all_splits = text_splitter.split_documents(data)

from langchain.vectorstores import Chroma
from langchain.embeddings import GPT4AllEmbeddings

vectorstore = Chroma.from_documents(documents=all_splits, embedding=GPT4AllEmbeddings())

question = "What are the approaches to Task Decomposition?"
docs = vectorstore.similarity_search(question)
len(docs)

import pdb
pdb.set_trace()