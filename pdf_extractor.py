import PyPDF2
import re
import os

class PDFExtractor:
    def __init__(self):
        self.phone_pattern = r'(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
        self.skip_words = ['curriculum', 'vitae', 'resume', 'cv', 'polytechnic', 'university', 'college', 'designer', 'engineer', 'manager', 'developer', 'analyst', 'graphics', 'personal', 'contact', 'information', 'profile', 'objective', 'summary']
        
        # Section headers to ignore (French/English)
        self.banned_sections = [
            'profile professionnel', 'experiences professionnelles', 'formation universitaire',
            'adresse maroc', 'comptences pro', 'competences professionnelles', 'formation',
            'experience', 'education', 'skills', 'langues', 'languages', 'certifications',
            'projets', 'projects', 'references', 'loisirs', 'hobbies', 'coordonnees',
            'contact details', 'personal details', 'informations personnelles'
        ]
    
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
    
    def extract_name_from_filename(self, filename):
        """Extract name from PDF filename"""
        # Remove file extension
        name = filename.replace('.pdf', '').replace('.PDF', '')
        
        # Clean common CV-related words from filename
        cv_words = ['cv', 'resume', 'curriculum', 'vitae', '_', '-']
        for word in cv_words:
            name = re.sub(rf'\b{word}\b', ' ', name, flags=re.IGNORECASE)
        
        # Clean and validate
        cleaned = self.clean_name(name)
        if self.is_valid_name(cleaned):
            return cleaned
        return ''
    
    def extract_name(self, text, filename=''):
        """Robust name detector prioritizing document titles"""
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        
        # Pattern 1: Document title/header (first 6 lines with high priority)
        for i, line in enumerate(lines[:6]):
            candidate = self.clean_name(line)
            if self.is_valid_name(candidate) and not self.is_section_header(candidate):
                words = candidate.split()
                if len(words) >= 2 and len(candidate) >= 6:
                    # Highest priority for first 3 lines
                    if i <= 2 and len(words) <= 4:
                        return candidate
                    # Medium priority for lines 4-6
                    elif i <= 5 and len(words) <= 3:
                        return candidate
        
        # Pattern 2: ALL CAPS names (common CV titles)
        caps_pattern = r'\b([A-Z]{2,}\s+[A-Z]{2,}(?:\s+[A-Z]{2,})?)\b'
        caps_matches = re.findall(caps_pattern, text)
        for match in caps_matches:
            candidate = self.clean_name(match)
            if self.is_valid_name(candidate) and len(candidate.split()) <= 4:
                return candidate
        
        # Pattern 3: Explicit NAME: labels anywhere in document
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
        
        # Pattern 4: Look for names in remaining first 15 lines
        for line in lines[5:15]:
            candidate = self.clean_name(line)
            if self.is_valid_name(candidate):
                if len(candidate.split()) >= 2 and len(candidate) >= 6:
                    return candidate
        
        # Pattern 5: Fallback to filename if available
        if filename:
            filename_name = self.extract_name_from_filename(filename)
            if filename_name:
                return filename_name
        
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
    
    def is_section_header(self, text):
        """Check if text is a section header to ignore"""
        text_lower = text.lower().strip()
        return any(banned in text_lower for banned in self.banned_sections)
    
    def extract_email(self, text):
        """Extract exactly ONE email address following specific rules"""
        if not text:
            return ''
        
        email_pattern = r'[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        matches = re.findall(email_pattern, text, re.IGNORECASE)
        
        if not matches:
            return ''
        
        valid_emails = []
        for match in matches:
            cleaned = re.match(r'^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', match)
            if cleaned:
                email = cleaned.group().lower()
                domain = email.split('@')[1]
                if self.is_valid_domain(domain):
                    valid_emails.append(email)
        
        if not valid_emails:
            return ''
        
        personal_emails = [e for e in valid_emails if not e.endswith('@indeedemail.com')]
        indeed_emails = [e for e in valid_emails if e.endswith('@indeedemail.com')]
        
        if personal_emails:
            return personal_emails[0]
        elif indeed_emails:
            return indeed_emails[0]
        
        return ''
    
    def is_valid_domain(self, domain):
        """Check if domain is valid"""
        common_domains = ['gmail.com', 'outlook.com', 'icloud.com', 'yahoo.com', 'hotmail.com', 'indeedemail.com']
        
        if domain in common_domains:
            return True
        
        if '.' in domain and len(domain.split('.')[-1]) >= 2:
            return True
        
        return False
    
    def extract_phone(self, text):
        """Extract exactly ONE Moroccan phone number"""
        if not text:
            return ''
        
        # Find all potential phone patterns
        phone_patterns = [
            r'\+212[67]\d{8}',
            r'212[67]\d{8}',
            r'0[567]\d{8}',
            r'\+212[\s\-\.]*[67][\s\-\.]*\d[\s\-\.]*\d[\s\-\.]*\d[\s\-\.]*\d[\s\-\.]*\d[\s\-\.]*\d[\s\-\.]*\d[\s\-\.]*\d',
            r'212[\s\-\.]*[67][\s\-\.]*\d[\s\-\.]*\d[\s\-\.]*\d[\s\-\.]*\d[\s\-\.]*\d[\s\-\.]*\d[\s\-\.]*\d[\s\-\.]*\d',
            r'0[\s\-\.]*[567][\s\-\.]*\d[\s\-\.]*\d[\s\-\.]*\d[\s\-\.]*\d[\s\-\.]*\d[\s\-\.]*\d[\s\-\.]*\d[\s\-\.]*\d'
        ]
        
        matches = []
        for pattern in phone_patterns:
            matches.extend(re.findall(pattern, text))
        
        if not matches:
            return ''
        
        # Clean and normalize
        valid_phones = []
        for match in matches:
            digits = re.sub(r'[^\d+]', '', match)
            
            if len(digits) < 8:
                continue
            
            # Normalize to +212 format
            if digits.startswith('+212'):
                normalized = digits
            elif digits.startswith('212'):
                normalized = '+' + digits
            elif digits.startswith('06') or digits.startswith('07') or digits.startswith('05'):
                normalized = '+212' + digits[1:]
            else:
                continue
            
            if len(normalized) == 13 and normalized[4] in '567':
                valid_phones.append(normalized)
        
        # Prefer mobile numbers (06, 07)
        mobile_phones = [p for p in valid_phones if p[4] in '67']
        if mobile_phones:
            return mobile_phones[0]
        elif valid_phones:
            return valid_phones[0]
        
        return ''
    
    def extract_fields(self, text, filename=''):
        """Extract name, email, phone from text"""
        result = {
            'name': '',
            'email': '',
            'phone': '',
            'status': 'success'
        }
    
        result['email'] = self.extract_email(text)
        
        result['phone'] = self.extract_phone(text)
        
        result['name'] = self.extract_name(text, filename)
        
        missing_fields = [k for k, v in result.items() if k != 'status' and not v]
        if missing_fields:
            result['status'] = 'manual_review'
        
        return result