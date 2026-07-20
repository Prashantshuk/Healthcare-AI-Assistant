from app.services.rag_service import generate_rag_response


def generate_ai_response(user_message: str) -> str:
    """
    Chat service.
    Right now it simply forwards the request
    to the RAG service.
    """

    return generate_rag_response(user_message)