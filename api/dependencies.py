from langchain_community.vectorstores import Chroma
import os
from langchain_google_genai import (
    ChatGoogleGenerativeAI,
    GoogleGenerativeAIEmbeddings
)


PERSIST_DIR = "chroma_db"

# Embeddings
embeddings =  GoogleGenerativeAIEmbeddings(
    model="models/gemini-embedding-001",
    google_api_key=os.environ["GOOGLE_API_KEY"]
)


PERSIST_DIR = "chroma_db"

def get_vector_db():
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/gemini-embedding-001",
        google_api_key=os.environ["GOOGLE_API_KEY"]
    )

    db = Chroma(
        persist_directory=PERSIST_DIR,
        embedding_function=embeddings
    )
    return db

# Gemini LLM
llm = ChatGoogleGenerativeAI(
    model="models/gemini-2.5-flash",
    temperature=0
)
