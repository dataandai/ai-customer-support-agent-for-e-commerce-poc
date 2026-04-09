from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from agent import SupportAgent
from typing import List, Dict

app = FastAPI(title="TechMart AI Support API")
agent = SupportAgent()

class ChatRequest(BaseModel):
    message: str
    history: List[Dict] = []

@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    try:
        # Simple history formatting for LangChain
        response = agent.run(request.message, request.history)
        return {"reply": response["output"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)