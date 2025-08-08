#Extract text from PDF, DOCX or TXT.
# utils/extractor.py
import fitz  # PyMuPDF
import docx2txt
import os
from typing import Tuple

def extract_text_from_pdf_bytes(file_bytes: bytes) -> str:
    doc = fitz.open(stream=file_bytes, filetype="pdf")
    pages = []
    for page in doc:
        pages.append(page.get_text())
    return "\n".join(pages)

def extract_text_from_docx_bytes(file_bytes: bytes, filename_hint="uploaded.docx") -> str:
    # docx2txt expects a filename on disk; write a temp file
    tmp_path = os.path.join("/tmp", filename_hint)
    with open(tmp_path, "wb") as f:
        f.write(file_bytes)
    try:
        text = docx2txt.process(tmp_path)
    finally:
        try:
            os.remove(tmp_path)
        except:
            pass
    return text

def extract_text_from_file(uploaded_file) -> Tuple[str, str]:
    """
    uploaded_file: Streamlit uploaded file-like object or (bytes, name)
    returns (text, file_type)
    """
    name = getattr(uploaded_file, "name", None)
    data = uploaded_file.read() if hasattr(uploaded_file, "read") else uploaded_file[0]
    if name and name.lower().endswith(".pdf"):
        text = extract_text_from_pdf_bytes(data)
        return text, "pdf"
    if name and name.lower().endswith(".docx"):
        text = extract_text_from_docx_bytes(data, filename_hint=name)
        return text, "docx"
    # assume txt or fallback
    try:
        text = data.decode("utf-8")
    except Exception:
        text = ""
    return text, "txt"
