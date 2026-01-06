from fastapi import FastAPI
from api.schema import QueryRequest, QueryResponse
from rag_query import query_rag

app = FastAPI(title="RAG API")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/query", response_model=QueryResponse)
def query(request: QueryRequest):
    answer = query_rag(request.question)
    return {"answer": answer}


