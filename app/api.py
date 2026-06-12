from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app.rag import ask_bot

app = FastAPI(
    title="E-commerce RAG Chatbot API",
    description="AI chatbot using scraped e-commerce data and RAG.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    question: str

@app.get("/")
def home():
    return {"message": "Backend is running"}

@app.post("/chat")
def chat(request: ChatRequest):
    return ask_bot(request.question)