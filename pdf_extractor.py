import PyPDF2
import re
import os

class PDFExtractor:
    def __init__(self):
        self.email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        self.phone_pattern = r'(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
        self.name_patterns = [
            r'^([A-Z][a-z]+ [A-Z][a-z]+)',
            r'Name[:\s]+([A-Z][a-z]+ [A-Z][a-z]+)',
            r'^([A-Z][A-Z\s]+)$'
        ]
    
    def extract_text(self, pdf_path):
        """Extract text from PDF"""
        try:
            with open(pdf_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                text = ""
                for page in reader.pages:
                    text += page.extract_text() + "\n"
            
            os.remove(pdf_path)  # Clean up temp file
            return text.strip()
        except Exception as e:
            print(f"Error extracting text from {pdf_path}: {e}")
            return ""
    
    def extract_fields(self, text):
        """Extract name, email, phone from text"""
        result = {
            'name': '',
            'email': '',
            'phone': '',
            'status': 'success'
        }
        
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        
        # Extract email
        email_match = re.search(self.email_pattern, text, re.IGNORECASE)
        if email_match:
            result['email'] = email_match.group()
        
        # Extract phone
        phone_match = re.search(self.phone_pattern, text)
        if phone_match:
            result['phone'] = re.sub(r'[^\d+]', '', phone_match.group())
        
        # Extract name (try multiple patterns)
        for pattern in self.name_patterns:
            name_match = re.search(pattern, text, re.MULTILINE)
            if name_match:
                result['name'] = name_match.group(1).title()
                break
        
        # If no name found, use first non-empty line
        if not result['name'] and lines:
            result['name'] = lines[0][:50]  # Limit length
        
        # Set status based on missing fields
        missing_fields = [k for k, v in result.items() if k != 'status' and not v]
        if missing_fields:
            result['status'] = 'manual_review'
        
        return result