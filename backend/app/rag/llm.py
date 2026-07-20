from langchain_google_genai import ChatGoogleGenerativeAI

from app.core.gemini_config import GOOGLE_API_KEY


def get_llm():
    return ChatGoogleGenerativeAI(
        model="gemini-3.1-flash-lite",
        google_api_key=GOOGLE_API_KEY,
        temperature=0.3,
    )