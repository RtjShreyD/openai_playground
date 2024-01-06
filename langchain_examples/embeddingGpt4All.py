from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.llms import GPT4All
from langchain.document_loaders import WebBaseLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import GPT4AllEmbeddings
from langchain.vectorstores import Chroma
from langchain.retrievers.multi_query import MultiQueryRetriever

template = """Question: {question}
Answer: Let's think step by step."""

prompt = PromptTemplate(template=template, input_variables=["question"])

local_path = (
    "/home/sarthaksharma/.cache/gpt4all/ggml-all-MiniLM-L6-v2-f16.bin"  # replace with your desired local file path
)

callbacks = [StreamingStdOutCallbackHandler()]      # Callbacks support token-wise streaming

# If you want to use a custom model add the backend parameter
# Check https://docs.gpt4all.io/gpt4all_python.html for supported backends
llm = GPT4All(model=local_path, backend="gptj", callbacks=callbacks, verbose=True)


loader = TextLoader("Sample_Data/sample_doctors.txt")
data = loader.load()

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=50)
all_splits = text_splitter.split_documents(data)

embedding=GPT4AllEmbeddings()
vectorstore = Chroma.from_documents(documents=all_splits, embedding=embedding)

retriever_from_llm = MultiQueryRetriever.from_llm(  
    retriever=vectorstore.as_retriever(), llm=llm
)

question = "Rohan has pain in his ears, which doctor should he consult?"

unique_docs = retriever_from_llm.get_relevant_documents(query=question)
print(len(unique_docs))
print(unique_docs)