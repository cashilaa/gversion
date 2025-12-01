import json

def create_sample_credentials():
    """Create a sample credentials.json template"""
    
    sample_creds = {
        "installed": {
            "client_id": "your_client_id.apps.googleusercontent.com",
            "project_id": "your_project_id",
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
            "client_secret": "your_client_secret",
            "redirect_uris": ["http://localhost"]
        }
    }
    
    with open('credentials_template.json', 'w') as f:
        json.dump(sample_creds, f, indent=2)
    
    print("Created credentials_template.json")
    print("\nTo get proper credentials:")
    print("1. Go to https://console.cloud.google.com/")
    print("2. Create new project or select existing")
    print("3. Enable Drive API and Sheets API")
    print("4. Go to Credentials > Create Credentials > OAuth 2.0 Client ID")
    print("5. Choose 'Desktop Application' as application type")
    print("6. Download the JSON file and rename to 'credentials.json'")

if __name__ == "__main__":
    create_sample_credentials()