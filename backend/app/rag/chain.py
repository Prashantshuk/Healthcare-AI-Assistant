from app.rag.llm import get_llm


def ask_llm(prompt: str):
    llm = get_llm()

    response = llm.invoke(prompt)

    content = response.content

    # Agar Gemini list return kare
    if isinstance(content, list):
        text = ""

        for item in content:
            if isinstance(item, dict):
                text += item.get("text", "")

        return text

    return str(content)