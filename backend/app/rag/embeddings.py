from langchain_google_genai import GoogleGenerativeAIEmbeddings
from app.core.gemini_config import GOOGLE_API_KEY


def get_embeddings():
    return GoogleGenerativeAIEmbeddings(
        model="models/gemini-embedding-001",
        google_api_key=GOOGLE_API_KEY
    )