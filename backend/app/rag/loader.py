import pypdf
from langchain_core.documents import Document

def load_pdf(file_path: str):
    try:
        reader = pypdf.PdfReader(file_path)
        docs = []

        for i, page in enumerate(reader.pages):
            try:
                text = page.extract_text() or ""
            except Exception as e:
                print(f"Page {i+1} extraction failed: {e}")
                text = ""
            docs.append(Document(page_content=text, metadata={"page_number": i + 1}))

        print(f"Pages: {len(docs)}")
        for i, d in enumerate(docs[:5]):
            print("=" * 40)
            print(f"Page {i+1}")
            print(repr(d.page_content[:200]))

        non_empty_docs = [d for d in docs if d.page_content.strip()]
        if not non_empty_docs:
            print("WARNING: No text extracted — likely a scanned/image PDF, needs OCR")

        return docs

    except Exception as e:
        print(f"Failed to load PDF: {e}")
        return []