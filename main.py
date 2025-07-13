"""
main.py: FastAPI app for RAG-based legal question answering using company policy PDFs.
"""

import os
from fastapi import FastAPI
from pydantic import BaseModel
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from dotenv import load_dotenv
from contextlib import asynccontextmanager
import requests

# Load environment variables
load_dotenv()

vector_dbs = {}

class Query(BaseModel):
    question: str
    company: str

def build_vectorstore(company: str):
    """Load, split, embed, and index the specified company's PDF."""
    path = f"documents/{company}.pdf"
    loader = PyPDFLoader(path)
    docs = loader.load()
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_documents(docs)
    embedder = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    return FAISS.from_documents(chunks, embedder)

def call_claude_llm(prompt: str) -> str:
    """Send prompt to Claude 3 Sonnet API and return the answer."""
    url = "https://api.anthropic.com/v1/messages"
    api_key = os.getenv("CLAUDE_API_KEY")
    if not api_key:
        return "Error: CLAUDE_API_KEY not set in environment."
    headers = {
        "x-api-key": api_key,
        "anthropic-version": "2023-06-01",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "claude-3-sonnet-20240229",
        "max_tokens": 500,
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }
    try:
        res = requests.post(url, json=payload, headers=headers, timeout=60)
        res.raise_for_status()
        return res.json()["content"][0]["text"]
    except Exception as e:
        return f"Error contacting Claude API: {e}"

@asynccontextmanager
async def lifespan(app: FastAPI):
    """On startup, load and index all PDFs in the documents folder."""
    for file in os.listdir("documents"):
        if file.endswith(".pdf"):
            company = file.replace(".pdf", "").lower()
            vector_dbs[company] = build_vectorstore(company)
    yield

app = FastAPI(lifespan=lifespan)

@app.post("/ask")
async def ask(query: Query):
    """Answer a legal question for a given company using its policy document."""
    company = query.company.lower()
    if company not in vector_dbs:
        return {"error": "Company not found"}
    retriever = vector_dbs[company].as_retriever()
    docs = retriever.invoke(query.question)
    context = "\n\n".join([doc.page_content for doc in docs[:4]])
    prompt = f"""
You are a legal assistant answering user queries only based on the following policy document. Answer concisely and only from the provided context.

{context}

Question: {query.question}
Answer:
"""
    answer = call_claude_llm(prompt)
    return {"answer": answer}