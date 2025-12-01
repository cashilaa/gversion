import PyPDF2
import re
import os

class PDFExtractor:
    def __init__(self):
        self.email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        self.phone_pattern = r'(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
        self.skip_words = ['curriculum', 'vitae', 'resume', 'cv', 'polytechnic', 'university', 'college', 'designer', 'engineer', 'manager', 'developer', 'analyst', 'graphics', 'personal', 'contact', 'information', 'profile', 'objective', 'summary']
    
    def extract_text(self, pdf_path):
        """Extract text from PDF"""
        try:
            with open(pdf_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                text = ""
                for page in reader.pages:
                    text += page.extract_text() + "\n"
            
            os.remove(pdf_path)  
            return text.strip()
        except Exception as e:
            print(f"Error extracting text from {pdf_path}: {e}")
            return ""
    
    def extract_name(self, text):
        """Robust name detector"""
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        
        # Pattern 1: Explicit NAME: labels anywhere in document
        name_label_patterns = [
            r'(?:name|full\s*name|candidate\s*name)[:]\s*([A-Za-z\s\-\.]{3,50})',
            r'([A-Za-z\s\-\.]{3,50})\s*-\s*(?:cv|resume|curriculum)',
        ]
        
        for pattern in name_label_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE | re.MULTILINE)
            for match in matches:
                candidate = self.clean_name(match)
                if self.is_valid_name(candidate):
                    return candidate
        
        # Pattern 2: Look for names in first 15 lines
        for line in lines[:15]:
            candidate = self.clean_name(line)
            if self.is_valid_name(candidate):
                # Extra validation for first lines
                if len(candidate.split()) >= 2 and len(candidate) >= 6:
                    return candidate
        
        # Pattern 3: ALL CAPS names (common in CVs)
        caps_pattern = r'\b([A-Z]{2,}\s+[A-Z]{2,}(?:\s+[A-Z]{2,})?)\b'
        caps_matches = re.findall(caps_pattern, text)
        for match in caps_matches:
            candidate = self.clean_name(match)
            if self.is_valid_name(candidate) and len(candidate.split()) <= 4:
                return candidate
        
        return ''
    
    def clean_name(self, name_str):
        """Clean and normalize name string"""
        if not name_str:
            return ''
        
        cleaned = ' '.join(name_str.split())
        
        # Remove common prefixes/suffixes
        prefixes = ['mr', 'mrs', 'ms', 'dr', 'prof']
        suffixes = ['jr', 'sr', 'ii', 'iii']
        
        words = cleaned.lower().split()
        words = [w for w in words if w not in prefixes]
        
        # Convert to title case
        return ' '.join(word.capitalize() for word in words if word.isalpha() or '-' in word)
    
    def is_valid_name(self, name_str):
        """Check if string is a valid name"""
        if not name_str or len(name_str) < 3:
            return False
        
        # Must contain only letters, spaces, hyphens, dots
        if not re.match(r'^[A-Za-z\s\-\.]+$', name_str):
            return False
        
        # Check against skip words
        name_lower = name_str.lower()
        if any(skip in name_lower for skip in self.skip_words):
            return False
        
        words = name_str.split()
        if not (2 <= len(words) <= 4):
            return False
        
        if any(len(word) < 2 or len(word) > 20 for word in words):
            return False
        
        return True
    
    def extract_fields(self, text):
        """Extract name, email, phone from text"""
        result = {
            'name': '',
            'email': '',
            'phone': '',
            'status': 'success'
        }
    
        email_match = re.search(self.email_pattern, text, re.IGNORECASE)
        if email_match:
            result['email'] = email_match.group()
        
        phone_match = re.search(self.phone_pattern, text)
        if phone_match:
            result['phone'] = re.sub(r'[^\d+]', '', phone_match.group())
        
        result['name'] = self.extract_name(text)
        
        missing_fields = [k for k, v in result.items() if k != 'status' and not v]
        if missing_fields:
            result['status'] = 'manual_review'
        
        return result