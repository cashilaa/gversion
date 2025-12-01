import time
from drive_monitor import DriveMonitor
from pdf_extractor import PDFExtractor
from sheets_manager import SheetsManager
import config

class CVProcessor:
    def __init__(self):
        self.drive_monitor = DriveMonitor()
        self.pdf_extractor = PDFExtractor()
        self.sheets_manager = SheetsManager()
    
    def process_cv(self, file_info):
        """Process a single CV file"""
        filename = file_info['name']
        file_id = file_info['id']
        
        print(f"Processing: {filename}")
        
        # Check for duplicates
        if self.sheets_manager.check_duplicate(filename):
            print(f"Skipping duplicate: {filename}")
            return
        
        # Download file
        temp_path = self.drive_monitor.download_file(file_id, filename)
        if not temp_path:
            print(f"Failed to download: {filename}")
            return
        
        # Extract text
        text = self.pdf_extractor.extract_text(temp_path)
        if not text:
            print(f"Failed to extract text: {filename}")
            return
        
        # Extract fields
        extracted_data = self.pdf_extractor.extract_fields(text)
        
        # Save to sheets
        success = self.sheets_manager.add_cv_data(extracted_data, filename)
        
        if success:
            print(f"Processed: {filename} - Status: {extracted_data['status']}")
        else:
            print(f"Failed to save: {filename}")
    
    def run(self):
        """Main processing loop"""
        print("CV Processor started...")
        print(f"Monitoring Drive folder every {config.POLL_INTERVAL} seconds")
        
        while True:
            try:
                new_files = self.drive_monitor.get_new_files()
                
                if new_files:
                    print(f"Found {len(new_files)} new files")
                    for file_info in new_files:
                        self.process_cv(file_info)
                
                time.sleep(config.POLL_INTERVAL)
                
            except KeyboardInterrupt:
                print("\nStopping CV Processor...")
                break
            except Exception as e:
                print(f"Error in main loop: {e}")
                time.sleep(config.POLL_INTERVAL)

if __name__ == "__main__":
    processor = CVProcessor()
    processor.run()