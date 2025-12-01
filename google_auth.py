from google.oauth2 import service_account
from googleapiclient.discovery import build
import os
import config

def get_google_service(service_name, version):
    """Authenticate and return Google API service using service account"""
    if not os.path.exists(config.GOOGLE_CREDENTIALS_FILE):
        print(f"Error: {config.GOOGLE_CREDENTIALS_FILE} not found!")
        exit(1)
    
    try:
        creds = service_account.Credentials.from_service_account_file(
            config.GOOGLE_CREDENTIALS_FILE, scopes=config.SCOPES)
        return build(service_name, version, credentials=creds)
    except Exception as e:
        print(f"Error loading credentials: {e}")
        exit(1)