from dotenv import load_dotenv
import os

load_dotenv()

configs = {
    "OPENAI_API_KEY" : os.getenv("OPENAI_API_KEY")
    # "PINECONE_API_KEY" : os.getenv("PINECONE_API_KEY"),
    # "PINECONE_ENV" : os.getenv("PINECONE_ENV"),
    # "SERPAPI_API_KEY" : os.getenv("SERPAPI_API_KEY"),
    # "TIKA_SERVER_JAR" : os.getenv("TIKA_SERVER_JAR"),
    # "TIKA_PATH" : os.getenv("TIKA_PATH"),
    # "MAX_RETRY" : os.getenv("MAX_RETRY")
}