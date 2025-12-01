import PyPDF2
import re
import os

class PDFExtractor:
    def __init__(self):
        self.email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        self.phone_pattern = r'(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
        self.skip_words = ['curriculum', 'vitae', 'resume', 'cv', 'polytechnic', 'university', 'college', 'designer', 'engineer', 'manager', 'developer', 'analyst']
        self.name_patterns = [
            r'Name[:\s]+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)',
            r'^([A-Z][a-z]+(?:\s+[A-Z][a-z]+){1,3})(?:\s|$)',
            r'([A-Z][A-Z\s]{10,30})'
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
                candidate_name = name_match.group(1).strip().title()
                # Check if name contains skip words
                if not any(skip_word in candidate_name.lower() for skip_word in self.skip_words):
                    result['name'] = candidate_name
                    break
        
        # If no name found, search through first few lines
        if not result['name']:
            for line in lines[:5]:
                if len(line.split()) >= 2 and len(line.split()) <= 4:
                    if not any(skip_word in line.lower() for skip_word in self.skip_words):
                        if re.match(r'^[A-Z][a-z]+(?:\s+[A-Z][a-z]+)+', line):
                            result['name'] = line.title()
                            break
        
        # Set status based on missing fields
        missing_fields = [k for k, v in result.items() if k != 'status' and not v]
        if missing_fields:
            result['status'] = 'manual_review'
        
        return result