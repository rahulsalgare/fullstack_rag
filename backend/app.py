from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from rag import get_answer_and_docs

app = FastAPI()


class Message(BaseModel):
    message: str

@app.post("/chat", description="Chat with the RAG API through this endpoint")
def chat(message: Message):
    response = get_answer_and_docs(message.message)
    response_content = {
        "question": message.message,
        "answer": response["answer"],
        "documents": [doc.dict() for doc in response["context"]]
    }
    return JSONResponse(content=response_content, status_code=200)