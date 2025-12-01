import os
from pdf_extractor import PDFExtractor

def test_extraction():
    """Test PDF extraction with sample text"""
    extractor = PDFExtractor()
    
    # Sample CV text for testing
    sample_text = """
    John Smith
    Software Engineer
    
    Email: john.smith@email.com
    Phone: +1 (555) 123-4567
    
    Experience:
    - 5 years in Python development
    - Expert in web applications
    """
    
    result = extractor.extract_fields(sample_text)
    
    print("Test Results:")
    print(f"Name: {result['name']}")
    print(f"Email: {result['email']}")
    print(f"Phone: {result['phone']}")
    print(f"Status: {result['status']}")
    
    return result

def create_test_folder():
    """Create test folder structure"""
    os.makedirs('test_cvs', exist_ok=True)
    print("Created test_cvs folder")
    print("Add PDF files here for testing")

if __name__ == "__main__":
    print("CV Processor Test Suite")
    print("=" * 30)
    
    test_extraction()
    create_test_folder()
    
    print("\nTests completed!")