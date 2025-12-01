import os
import json

def setup_credentials():
    """Setup Google API credentials"""
    print("CV Processor Setup")
    print("=" * 50)
    
    # Check for credentials file
    if not os.path.exists('credentials.json'):
        print("credentials.json not found!")
        print("\nTo get credentials:")
        print("1. Go to Google Cloud Console")
        print("2. Enable Drive API and Sheets API")
        print("3. Create OAuth 2.0 credentials")
        print("4. Download as 'credentials.json'")
        return False
    
    # Get configuration from user
    print("\nConfiguration:")
    
    drive_folder_id = input("Enter Google Drive folder ID: ").strip()
    spreadsheet_id = input("Enter Google Sheets ID: ").strip()
    
    # Update .env file
    env_content = f"""# Google Drive API credentials
GOOGLE_CREDENTIALS_FILE=credentials.json
DRIVE_FOLDER_ID={drive_folder_id}

# Google Sheets configuration
SPREADSHEET_ID={spreadsheet_id}
SHEET_NAME=CV_Data

# Monitoring settings
WATCH_FOLDER=./watch_folder
POLL_INTERVAL=30"""
    
    with open('.env', 'w') as f:
        f.write(env_content)
    
    print("\nConfiguration saved!")
    print("\nRun 'python main.py' to start processing")
    return True

if __name__ == "__main__":
    setup_credentials()