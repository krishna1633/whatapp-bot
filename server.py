from fastapi import FastAPI, Request
import requests
from bot import chatbot

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Hi I'm Findy. I can help you find local classes and academies for your child."}

@app.post("/query")
async def handle_query(request: Request):
    data = await request.json()
    user_query = data.get("query")
    
    if not user_query:
        return {"error": "Query parameter is missing"}, 400
    
    bot_reply = chatbot.get_answer(user_query)
    return {"response": bot_reply}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
