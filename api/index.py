import os

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from google import genai
from pydantic import BaseModel
from slowapi import Limiter
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address


GEMINI_API_KEY = os.environ["GEMINI_API_KEY"]
MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
ALLOWED_ORIGINS = [
    origin.strip()
    for origin in os.getenv(
        "ALLOWED_ORIGINS",
        "http://localhost:8000,http://127.0.0.1:8000",
    ).split(",")
    if origin.strip()
]

client = genai.Client(api_key=GEMINI_API_KEY)
limiter = Limiter(key_func=get_remote_address)

app = FastAPI()
app.state.limiter = limiter

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=False,
    allow_methods=["POST", "GET", "OPTIONS"],
    allow_headers=["*"],
)


class Message(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    messages: list[Message]


@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=429,
        content={"error": "Rate limit exceeded. Try again in a minute."},
    )


@app.get("/")
async def root():
    return {"ok": True, "service": "gemini-chatbot"}


@app.get("/health")
async def health():
    return {"ok": True}


@app.post("/chat")
@limiter.limit("15/minute")
async def chat(request: Request, body: ChatRequest):
    chat_session = client.chats.create(model=MODEL)
    reply = ""

    for message in body.messages:
        if message.role == "user":
            response = chat_session.send_message(message.content)
            reply = response.text or ""

    return {"reply": reply}
