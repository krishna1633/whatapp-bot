from fastapi import FastAPI, Request
import requests
from bot import chatbot
from dotenv import load_dotenv
import os

app = FastAPI()

# Load environment variables from .env file
load_dotenv()

ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")
WHATSAPP_API_URL = os.getenv("WHATSAPP_API_URL")

@app.get("/")
def home():
    return {"message": "WhatsApp Business Bot is running!"}

# WhatsApp Webhook Verification
@app.get("/webhook")
def verify_token(request: Request):
    mode = request.query_params.get("hub.mode")
    token = request.query_params.get("hub.verify_token")
    challenge = request.query_params.get("hub.challenge")

    if mode == "subscribe" and token == VERIFY_TOKEN:
        return int(challenge)
    return {"error": "Verification failed"}, 403

# WhatsApp Message Handling
@app.post("/webhook")
async def receive_whatsapp_message(request: Request):
    data = await request.json()
    
    # Extract WhatsApp message
    try:
        messages = data["entry"][0]["changes"][0]["value"]["messages"]
        for message in messages:
            if "text" in message:
                user_query = message["text"]["body"]
                sender_id = message["from"]

                # Get bot's response
                bot_reply = chatbot.get_answer(user_query)

                # Send response back to WhatsApp
                send_whatsapp_message(sender_id, bot_reply)
    except KeyError:
        pass  # Ignore non-message events
    
    return {"status": "received"}

def send_whatsapp_message(to, text):
    """Sends a message via the WhatsApp API."""
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "text",
        "text": {"body": text}
    }
    requests.post(WHATSAPP_API_URL, json=payload, headers=headers)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
