# CV Processor - Google Sheets Integration

Automatically processes CV/Resume PDFs from Google Drive and extracts contact information to Google Sheets.

## Features

- 📁 Monitors Google Drive folder for new PDFs
- 📄 Extracts text from PDF files
- 🔍 Identifies name, email, and phone number
- 📊 Saves data to Google Sheets
- 🔄 Avoids duplicate processing
- ⚠️ Flags entries needing manual review

## Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Google API Setup:**
   - Enable Drive API and Sheets API in Google Cloud Console
   - Create OAuth 2.0 credentials
   - Download as `credentials.json`

3. **Configure:**
   ```bash
   python setup.py
   ```

4. **Run:**
   ```bash
   python main.py
   ```

## Configuration

Edit `.env` file:
- `DRIVE_FOLDER_ID`: Google Drive folder to monitor
- `SPREADSHEET_ID`: Target Google Sheet ID
- `POLL_INTERVAL`: Check interval in seconds

## Run

```bash
python main.py
```

## Output Format

| Name | Email | Phone | Filename | Timestamp | Source | Status |
|------|-------|-------|----------|-----------|--------|--------|
| John Smith | john@email.com | +15551234567 | resume.pdf | 2024-01-15 10:30:00 | Google Drive | success |

## Status Values

- `success`: All fields extracted
- `manual_review`: Missing or unclear fields
- `failed`: Processing error