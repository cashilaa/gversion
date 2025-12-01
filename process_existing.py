from drive_monitor import DriveMonitor
from pdf_extractor import PDFExtractor
from sheets_manager import SheetsManager
import config

def process_all_files():
    """Process all PDF files in the Drive folder"""
    drive_monitor = DriveMonitor()
    pdf_extractor = PDFExtractor()
    sheets_manager = SheetsManager()
    
    try:
        # Get all PDF files 
        query = f"'{config.DRIVE_FOLDER_ID}' in parents and mimeType='application/pdf'"
        
        results = drive_monitor.drive_service.files().list(
            q=query,
            fields="files(id, name, modifiedTime, size)"
        ).execute()
        
        files = results.get('files', [])
        print(f"Found {len(files)} PDF files in folder")
        
        for file_info in files:
            filename = file_info['name']
            file_id = file_info['id']
            
            print(f"Processing: {filename}")
            
            # Check for duplicates
            if sheets_manager.check_duplicate(filename):
                print(f"Skipping duplicate: {filename}")
                continue
            
            # Download file
            temp_path = drive_monitor.download_file(file_id, filename)
            if not temp_path:
                print(f"Failed to download: {filename}")
                continue
            
            # Extract text
            text = pdf_extractor.extract_text(temp_path)
            if not text:
                print(f"Failed to extract text: {filename}")
                continue
            
            # Extract fields
            extracted_data = pdf_extractor.extract_fields(text)
            
            # Save to sheets
            success = sheets_manager.add_cv_data(extracted_data, filename)
            
            if success:
                print(f"Processed: {filename} - Status: {extracted_data['status']}")
            else:
                print(f"Failed to save: {filename}")
        
        print(f"\nCompleted processing {len(files)} files")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    process_all_files()