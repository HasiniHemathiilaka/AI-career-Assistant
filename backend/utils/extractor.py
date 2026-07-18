import pdfplumber

def extract_text_from_pdf(pdf_path_or_file):
    """
    Extracts all visible text from a PDF file or file-like object.
    """
    text = ""
    try:
        with pdfplumber.open(pdf_path_or_file) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    except Exception as e:
        print(f"Error reading PDF: {e}")
    
    return text.strip()