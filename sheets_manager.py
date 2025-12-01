from datetime import datetime
from google_auth import get_google_service
import config

class SheetsManager:
    def __init__(self):
        self.sheets_service = get_google_service('sheets', 'v4')
        self.setup_sheet()
    
    def setup_sheet(self):
        """Create sheet and headers if needed"""
        try:
            # Try to create the sheet first
            try:
                self.sheets_service.spreadsheets().batchUpdate(
                    spreadsheetId=config.SPREADSHEET_ID,
                    body={
                        'requests': [{
                            'addSheet': {
                                'properties': {
                                    'title': config.SHEET_NAME
                                }
                            }
                        }]
                    }
                ).execute()
                print(f"Created sheet: {config.SHEET_NAME}")
            except:
                pass  # Sheet already exists
            
            # Add headers
            headers = [['Name', 'Email', 'Phone', 'Filename', 'Timestamp', 'Source', 'Status']]
            self.sheets_service.spreadsheets().values().update(
                spreadsheetId=config.SPREADSHEET_ID,
                range=f"{config.SHEET_NAME}!A1:G1",
                valueInputOption='RAW',
                body={'values': headers}
            ).execute()
            print("Sheet setup complete")
        except Exception as e:
            print(f"Error setting up sheet: {e}")
            print("Make sure to share the Google Sheet with: cvdata@cvdata-479407.iam.gserviceaccount.com")
    
    def add_cv_data(self, extracted_data, filename):
        """Add CV data to sheet"""
        try:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            row_data = [[
                extracted_data.get('name', ''),
                extracted_data.get('email', ''),
                extracted_data.get('phone', ''),
                filename,
                timestamp,
                'Google Drive',
                extracted_data.get('status', 'success')
            ]]
            
            self.sheets_service.spreadsheets().values().append(
                spreadsheetId=config.SPREADSHEET_ID,
                range=f"{config.SHEET_NAME}!A:G",
                valueInputOption='RAW',
                insertDataOption='INSERT_ROWS',
                body={'values': row_data}
            ).execute()
            
            return True
        except Exception as e:
            print(f"Error adding data to sheet: {e}")
            return False
    
    def check_duplicate(self, filename):
        """Check if filename already exists"""
        try:
            result = self.sheets_service.spreadsheets().values().get(
                spreadsheetId=config.SPREADSHEET_ID,
                range=f"{config.SHEET_NAME}!D:D"
            ).execute()
            
            filenames = [row[0] for row in result.get('values', []) if row]
            return filename in filenames
        except Exception as e:
            print(f"Error checking duplicates: {e}")
            return False