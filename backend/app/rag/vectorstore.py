import time
from app.rag.embeddings import get_embeddings
from langchain_community.vectorstores import FAISS

embeddings = get_embeddings()


def create_vectorstore(chunks, batch_size=90, delay=61):
    vectorstore = None

    for i in range(0, len(chunks), batch_size):
        batch = chunks[i:i + batch_size]
        print(f"Embedding batch {i // batch_size + 1}: {len(batch)} chunks")

        if vectorstore is None:
            vectorstore = FAISS.from_documents(batch, embeddings)
        else:
            batch_store = FAISS.from_documents(batch, embeddings)
            vectorstore.merge_from(batch_store)

        if i + batch_size < len(chunks):
            print(f"Waiting {delay}s for rate limit reset...")
            time.sleep(delay)

    vectorstore.save_local("faiss_index")
    print("✅ FAISS index saved successfully.")

    return vectorstore


def load_vectorstore():
    vectorstore = FAISS.load_local(
        "faiss_index",
        embeddings,
        allow_dangerous_deserialization=True
    )

    return vectorstore