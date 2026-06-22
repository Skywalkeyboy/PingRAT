from fastapi import FastAPI, Request
import requests

app = FastAPI()

BOT_TOKEN = "8530378499:AAG1_0cr9fDqs2u-jplM7K4snL2rYfKveKE"
CHAT_ID = "6853778599"
API_KEY = "my-secret-key-123"

def send_telegram(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": CHAT_ID, "text": message})

@app.get("/")
def home():
    return {"status": "FastAPI is working"}

@app.get("/test")
def test():
    send_telegram("Message sent from FastAPI")
    return {"message": "Telegram message sent"}

@app.post("/webhook/github")
async def github_webhook(request: Request):
    payload = await request.json()
    repo = payload.get("repository", {}).get("full_name", "Unknown Repo")
    sender = payload.get("sender", {}).get("login", "Unknown User")

    message = f"GitHub Push\nRepo: {repo}\nUser: {sender}"
    send_telegram(message)

    return {"status": "received"}

@app.get("/protected")
def protected(request: Request):
    api_key = request.headers.get("x-api-key")

    if api_key != API_KEY:
        return {"error": "Invalid API key"}

    return {"message": "API key accepted"}

@app.post("/webhook/axiom")
async def axiom_webhook(request: Request):
    payload = await request.json()

    event = payload.get("event", "Axiom Event")
    token = payload.get("token", "Unknown Token")
    wallet = payload.get("wallet", "Unknown Wallet")
    note = payload.get("note", "")

    message = f"Axiom Alert\nEvent: {event}\nToken: {token}\nWallet: {wallet}\nNote: {note}"

    send_telegram(message)

    return {"status": "axiom received"}
