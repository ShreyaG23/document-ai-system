from fastapi import APIRouter, Form, UploadFile, HTTPException, File
from src.services.document_service import extract_text_from_document
from src.services.summarization_service import summarize_text
from typing import Optional
router = APIRouter()

@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    """
    Upload a pdf, docx, or text file and extract text.
    
    """
    allowed_types = ["application/pdf",
                     "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                     "text/plain"]
    if file.content_type not in allowed_types:
        raise HTTPException(status_code = 400, detail="Unsupported file type")
    
    extracted_text = await extract_text_from_document(file)

    return{
        "filename": file.filename,
        "content": extracted_text[:1000] #limit preview for safety
    }

@router.post("/summarize")
async def summarize_endpoint(
    file: Optional[UploadFile] = File(None),
    text: Optional[str] = Form(None),
    max_length:int = Form(250),
    min_length:int = Form(100),
):
    """
    summarize either files or raw text, if both are there it will only summarize file data
    """

    #prefer file is provided
    if file is not None:
        #validate file content-type optionally
        extracted_text = await extract_text_from_document(file)
        to_summarize = extracted_text
    else:
        to_summarize = text
    
    summary = summarize_text(to_summarize, max_length=max_length, min_length=min_length)
    return {"summary": summary}
