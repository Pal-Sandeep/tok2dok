from fastapi import APIRouter, Form

from src.utils.pdf_utils import query_pdf_chunks
router = APIRouter()

@router.post("/ask", description="Ask a question about a PDF document")
async def ask_question(
    pdf_id: str = Form(..., description="The ID of the PDF to query"),
    question: str = Form(..., description="The question to ask about the PDF")
):
    answer, sources = query_pdf_chunks(pdf_id, question)
    return {"answer": answer, "sources": [doc.metadata for doc in sources]}
