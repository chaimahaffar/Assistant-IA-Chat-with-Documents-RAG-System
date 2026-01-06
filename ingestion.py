from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import os

def load_documents(path: str) -> list[Document]:
    loader = PyPDFDirectoryLoader(path)
    return loader.load()


#chunking
def split_documents(documents: list[Document]) -> list[Document]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )
    chunks = splitter.split_documents(documents)

    for c in chunks:
        c.page_content = (
            f"Source: {c.metadata.get('source')} "
            f"Page: {c.metadata.get('page')}\n"
            + c.page_content
        )
    return chunks

def get_embeddings():
    return GoogleGenerativeAIEmbeddings(
        model="models/gemini-embedding-001",
        google_api_key=os.environ["GOOGLE_API_KEY"]
    )









