"""
PDF Generation Service for Resume Tailoring
"""

import os
import re
import tempfile
import logging
from fpdf import FPDF

logger = logging.getLogger(__name__)


def clean_text_for_pdf(text: str) -> str:
    """
    Sanitize text for PDF generation by removing emojis and problematic characters
    
    Args:
        text: Raw text that may contain emojis and special characters
    
    Returns:
        str: Cleaned text safe for PDF generation
    """
    # Remove emojis using regex
    # This pattern matches most emoji ranges
    emoji_pattern = re.compile(
        "["
        "\U0001F600-\U0001F64F"  # emoticons
        "\U0001F300-\U0001F5FF"  # symbols & pictographs
        "\U0001F680-\U0001F6FF"  # transport & map symbols
        "\U0001F1E0-\U0001F1FF"  # flags (iOS)
        "\U00002702-\U000027B0"  # dingbats
        "\U000024C2-\U0001F251"
        "\U0001F900-\U0001F9FF"  # supplemental symbols
        "\U0001FA00-\U0001FAFF"  # more symbols
        "]+",
        flags=re.UNICODE
    )
    text = emoji_pattern.sub('', text)
    
    # Remove markdown bold (**text**)
    text = re.sub(r'\*\*', '', text)
    
    # Remove markdown italic (*text*)
    text = re.sub(r'(?<!\*)\*(?!\*)', '', text)
    
    # Replace special bullet characters with standard dash
    text = text.replace('•', '-')
    text = text.replace('►', '-')
    text = text.replace('▪', '-')
    text = text.replace('◆', '-')
    text = text.replace('✓', 'X')
    text = text.replace('✔', 'X')
    text = text.replace('✗', 'X')
    text = text.replace('✘', 'X')
    
    # Remove other common problematic Unicode characters
    text = text.replace('→', '->')
    text = text.replace('←', '<-')
    text = text.replace('↑', '^')
    text = text.replace('↓', 'v')
    text = text.replace(''', "'")
    text = text.replace(''', "'")
    text = text.replace('"', '"')
    text = text.replace('"', '"')
    text = text.replace('…', '...')
    text = text.replace('—', '-')
    text = text.replace('–', '-')
    
    # Encode to latin-1 with replace to catch any remaining issues
    try:
        text = text.encode('latin-1', errors='replace').decode('latin-1')
    except Exception as e:
        logger.warning(f"Encoding issue during PDF text cleanup: {e}")
        # If encoding fails, try to just remove non-ASCII characters
        text = ''.join(char if ord(char) < 128 else '?' for char in text)
    
    return text


class PDFService:
    """Service for generating PDF documents"""
    
    def __init__(self):
        """Initialize PDF service"""
        pass
    
    def generate_resume_pdf(self, text_content: str, filename: str = "tailored_resume.pdf") -> str:
        """
        Generate a PDF resume from text content
        
        Args:
            text_content: The resume text content to convert to PDF
            filename: The name of the PDF file to generate
        
        Returns:
            str: Path to the generated PDF file
        """
        try:
            # Sanitize text before processing
            cleaned_content = clean_text_for_pdf(text_content)
            logger.info("✓ Text sanitized for PDF generation")
            
            # Create a PDF object
            pdf = FPDF()
            pdf.add_page()
            
            # Set font for title
            pdf.set_font("Arial", "B", 16)
            pdf.cell(0, 10, "Tailored Resume", ln=True, align="C")
            pdf.ln(5)  # Add some spacing
            
            # Set font for body text
            pdf.set_font("Arial", "", 11)
            
            # Add content with proper line breaks
            lines = cleaned_content.split('\n')
            for line in lines:
                # Handle empty lines
                if not line.strip():
                    pdf.ln(3)
                    continue
                
                try:
                    # Check if line is a header (all caps or starts with specific markers)
                    if line.strip().isupper() and len(line.strip()) < 50:
                        pdf.set_font("Arial", "B", 12)
                        pdf.multi_cell(0, 6, line.strip())
                        pdf.set_font("Arial", "", 11)
                    # Check if line starts with bullet point or dash
                    elif line.strip().startswith(('-', '*')):
                        pdf.multi_cell(0, 5, "  " + line.strip())
                    else:
                        pdf.multi_cell(0, 5, line.strip())
                except Exception as e:
                    logger.warning(f"Error adding line to PDF: {e}")
                    # Skip problematic lines
                    continue
            
            # Create temporary directory if it doesn't exist
            temp_dir = tempfile.gettempdir()
            output_path = os.path.join(temp_dir, filename)
            
            # Save PDF to file with error handling
            try:
                pdf.output(output_path)
                logger.info(f"✓ PDF generated successfully: {output_path}")
            except Exception as e:
                logger.error(f"❌ Failed to save PDF: {e}")
                logger.error(f"PDF output path: {output_path}")
                raise
            
            return output_path
        
        except Exception as e:
            logger.error(f"❌ PDF generation failed: {str(e)}")
            logger.error(f"Content preview (first 200 chars): {text_content[:200]}")
            raise Exception(f"Failed to generate PDF: {str(e)}")
