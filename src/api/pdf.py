import logging
# app/api/pdf.py

from fastapi import Form, UploadFile, APIRouter, Depends, File, HTTPException
from fastapi.responses import JSONResponse
from src.api.deps import get_current_user
from src.db import models, database
from sqlalchemy.orm import Session
from uuid import uuid4
from fastapi import status
import os
from PyPDF2 import PdfReader
import textwrap
from src.services.vector_store import index_chunks_with_langchain

from src.db.models import PDF
from src.utils.pdf_utils import extract_text_from_pdf, index_chunks_qdrant, load_and_split_pdf

router = APIRouter()

UPLOAD_DIR = "uploaded_pdfs"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def chunk_text(text, max_length=500):
    return textwrap.wrap(text, max_length)


@router.post("/upload_and_index/")
async def upload_pdf(file: UploadFile, pdf_id: str = Form(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")
    try:
        chunks = load_and_split_pdf(file, pdf_id)
        index_chunks_qdrant(chunks, pdf_id)
        return {"status": "indexed", "chunks": len(chunks)}
    except Exception as e:
        logging.error(f"Error in upload_and_index: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/upload")
async def upload_pdf_first(file: UploadFile = File(...), db: Session = Depends(database.get_db)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")

    try:
        # Step 1: Read PDF content
        pdf_text = extract_text_from_pdf(file)
        if not pdf_text:
            raise ValueError("Could not extract text from PDF")
        
        # Step 2: Store PDF metadata
        new_pdf = PDF(filename=file.filename, content=pdf_text, upload_path="/")
        db.add(new_pdf)
        db.commit()
        db.refresh(new_pdf)
        
        # Step 3: Send text to Langchain for chunking + embedding + storage
        index_chunks_with_langchain([pdf_text], pdf_id=new_pdf.id, db=db)
        
        return {
            "message": "PDF uploaded and chunks indexed successfully",
            "pdf_id": new_pdf.id,
            "filename": file.filename
        }
        
    except Exception as e:
        logging.error(f"Error in PDF upload: {str(e)}", exc_info=True)
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(
            status_code=500,
            detail=f"Failed to process PDF: {str(e)}"
        )
