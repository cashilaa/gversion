import time
from datetime import datetime
from google_auth import get_google_service
import config

class DriveMonitor:
    def __init__(self):
        self.drive_service = get_google_service('drive', 'v3')
        self.last_check = datetime.now().isoformat()
    
    def get_new_files(self):
        """Get new PDF files from Drive folder"""
        try:
            query = f"'{config.DRIVE_FOLDER_ID}' in parents and mimeType='application/pdf' and modifiedTime > '{self.last_check}'"
            
            results = self.drive_service.files().list(
                q=query,
                fields="files(id, name, modifiedTime, size)"
            ).execute()
            
            files = results.get('files', [])
            self.last_check = datetime.now().isoformat()
            
            return files
        except Exception as e:
            print(f"Error checking for new files: {e}")
            return []
    
    def download_file(self, file_id, filename):
        """Download PDF file from Drive"""
        try:
            request = self.drive_service.files().get_media(fileId=file_id)
            
            with open(f"temp_{filename}", 'wb') as f:
                downloader = request.execute()
                f.write(downloader)
            
            return f"temp_{filename}"
        except Exception as e:
            print(f"Error downloading file {filename}: {e}")
            return None