# app/services/file_reader.py

import fitz  # PyMuPDF
import docx
from fastapi import UploadFile
import os

def get_file_extension(filename: str) -> str:
    return filename.split('.')[-1].lower()

async def extract_text(file: UploadFile) -> str:
    ext = get_file_extension(file.filename)

    if ext == "pdf":
        return await extract_pdf_text(file)
    elif ext == "docx":
        return await extract_docx_text(file)
    elif ext == "txt":
        return await extract_txt_text(file)
    else:
        raise ValueError("Unsupported file format")

async def extract_pdf_text(file: UploadFile) -> str:
    contents = await file.read()
    doc = fitz.open(stream=contents, filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text

async def extract_docx_text(file: UploadFile) -> str:
    contents = await file.read()
    with open("temp.docx", "wb") as f:
        f.write(contents)

    doc = docx.Document("temp.docx")
    text = "\n".join([para.text for para in doc.paragraphs])
    os.remove("temp.docx")
    return text

async def extract_txt_text(file: UploadFile) -> str:
    contents = await file.read()
    return contents.decode("utf-8")
