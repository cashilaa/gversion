import os
from dotenv import load_dotenv

load_dotenv()

# Google API Configuration
GOOGLE_CREDENTIALS_FILE = os.getenv('GOOGLE_CREDENTIALS_FILE', 'credentials.json')
DRIVE_FOLDER_ID = os.getenv('DRIVE_FOLDER_ID')
SPREADSHEET_ID = os.getenv('SPREADSHEET_ID')
SHEET_NAME = os.getenv('SHEET_NAME', 'CV_Data')

# File monitoring
WATCH_FOLDER = os.getenv('WATCH_FOLDER', './watch_folder')
POLL_INTERVAL = int(os.getenv('POLL_INTERVAL', 30))

# Google API Scopes
SCOPES = [
    'https://www.googleapis.com/auth/drive.readonly',
    'https://www.googleapis.com/auth/spreadsheets'
]