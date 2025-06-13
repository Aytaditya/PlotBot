from fastapi import FastAPI, Request
from pydantic import BaseModel
from fastapi import Query
from rag_pipeline import run_rag
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()



app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to specific origins in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Business RAG API"}

@app.post("/ask")
def ask_question(question: str):
    try:
        answer = run_rag(question)
        return {"question":question, "answer": answer}
    except Exception as e:
        return {"error": str(e)}
