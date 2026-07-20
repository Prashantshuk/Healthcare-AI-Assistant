from langchain_text_splitters import RecursiveCharacterTextSplitter

def split_documents(documents):

    print("Received documents:", len(documents))

    print("First document length:", len(documents[0].page_content))
    print(repr(documents[0].page_content[:500]))

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
    )

    chunks = splitter.split_documents(documents)

    print("Chunks:", len(chunks))

    if chunks:
        print(repr(chunks[0].page_content[:500]))

    return chunks