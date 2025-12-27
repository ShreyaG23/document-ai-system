import io
from fastapi import UploadFile
import docx
from PyPDF2 import PdfReader

async def extract_text_from_document(file: UploadFile):
    """
    Extract text from pdf, docx, txt documents
    
    """
    content = await file.read()

    if file.filename.endswith(".pdf"):
        return extract_pdf(content)
    
    if file.filename.endswith("docx"):
        return extract_docx(content)
    
    if file.filename.endswith(".txt"):
        return content.decode("utf-8", errors="ignore")
    
    return ""

def extract_pdf(content):
    pdf_reader = PdfReader(io.BytesIO(content))
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text() or ""
    return text

def extract_docx(content):
    doc = docx.Document(io.BytesIO(content))
    text = "\n".join([para for para in doc.paragraphs])
    return text


