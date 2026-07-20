from app.rag.chain import ask_llm
from app.rag.vectorstore import load_vectorstore


def generate_rag_response(query: str) -> str:

    # Load FAISS vector database
    vectorstore = load_vectorstore()

    # Retrieve top 4 relevant chunks
    docs = vectorstore.similarity_search(query, k=4)

    # Combine retrieved text
    context = "\n\n".join(doc.page_content for doc in docs)

    # Prompt for LLM
    prompt = f"""
You are a Healthcare AI Assistant.

Answer ONLY using the context provided below.

If the answer is not present in the context, reply exactly:

"I couldn't find this information in the uploaded document."

--------------------
Context:
{context}
--------------------

Question:
{query}

Answer:
"""

    return ask_llm(prompt)