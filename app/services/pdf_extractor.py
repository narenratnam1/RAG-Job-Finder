"""
PDF Text Extraction Service
"""

from pypdf import PdfReader


def extract_text_from_pdf(file_path: str) -> str:
    """
    Extract all text from a PDF file
    
    Args:
        file_path: Path to the PDF file
    
    Returns:
        str: Combined text from all pages
    """
    try:
        reader = PdfReader(file_path)
        text_parts = []
        
        for page in reader.pages:
            text = page.extract_text()
            if text.strip():
                text_parts.append(text)
        
        return "\n\n".join(text_parts)
    
    except Exception as e:
        raise Exception(f"Failed to extract text from PDF: {str(e)}")
