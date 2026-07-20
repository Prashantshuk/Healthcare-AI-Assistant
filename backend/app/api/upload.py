import os
from typing import List

from fastapi import APIRouter, UploadFile, File
from app.rag.loader import load_pdf
from app.rag.splitter import split_documents
from app.rag.vectorstore import create_vectorstore

router = APIRouter(
    prefix="/upload",
    tags=["Upload"]
)

UPLOAD_FOLDER = "data/uploads"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@router.post("/")
async def upload_pdf(files: List[UploadFile] = File(...)):

    all_chunks = []

    for file in files:

        file_path = os.path.join(UPLOAD_FOLDER, file.filename)

        with open(file_path, "wb") as buffer:
            buffer.write(await file.read())

        # Load PDF
        documents = load_pdf(file_path)

        # Safety check
        if not documents or not any(d.page_content.strip() for d in documents):
            continue

        # Split into chunks
        chunks = split_documents(documents)
        print(f"{file.filename} -> {len(chunks)} chunks")

        all_chunks.extend(chunks)

    if not all_chunks:
        return {
            "error": "No valid text found in the uploaded PDFs."
        }

    # Create one FAISS index using all PDFs
    create_vectorstore(all_chunks)

    return {
        "message": "PDFs uploaded and indexed successfully",
        "total_files": len(files),
        "total_chunks": len(all_chunks)
    }