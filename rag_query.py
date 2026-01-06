import os
import google.generativeai as genai
from ingestion import load_documents, split_documents, get_embeddings
from vector_store import build_or_update_chroma_db
from langchain_community.llms import Ollama

# 🔹 INITIALISATION UNE SEULE FOIS
documents = load_documents("data")
chunks = split_documents(documents)


embeddings = get_embeddings()
db = build_or_update_chroma_db(chunks, embeddings)

genai.configure(api_key=os.environ["GOOGLE_API_KEY"])


PROMPT_TEMPLATE = """
You are a question-answering system.

You MUST answer the question using ONLY the information from the context.
Do NOT use any external knowledge.

Context:
{context}

Question:
{question}

If the answer is not explicitly stated in the context, say:
"The information is not available in the provided documents."
"""

def get_db():
    return db

def query_rag(user_question: str) -> str:
    db = get_db()

    results = db.similarity_search_with_score(user_question, k=5)

    if not results:
        return "No relevant information found in the documents."

    context_text = "\n\n".join(doc.page_content for doc, _ in results)

    prompt = PROMPT_TEMPLATE.format(
        context=context_text,
        question=user_question
    )

    model = Ollama(model="phi")
    response = model.invoke(prompt)

    return response.text if hasattr(response, "text") else str(response)


""" if __name__ == "__main__":
    # 🔹 Initialisation UNE SEULE FOIS
    documents = load_documents("data")
    chunks = split_documents(documents)
    embeddings = get_embeddings()
    db = build_or_update_chroma_db(chunks, embeddings)

    genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

    # 🔹 Boucle interactive
    while True:
        question = input("\nAsk a question (or type 'exit'): ")

        if question.lower() in ["exit", "quit"]:
            break

        query_rag(question) """
