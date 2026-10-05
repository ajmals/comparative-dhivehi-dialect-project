#!/usr/bin/env python3
"""
Upload atoll CSVs to Google Drive as native Google Sheets.
Requires:
  pip install google-api-python-client google-auth-oauthlib google-auth-httplib2
  credentials.json in the project root or passed via CLI.
"""

import sys
import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CREDENTIALS_FILE = PROJECT_ROOT / "credentials.json"
ATOLLS_DIR = PROJECT_ROOT / "data" / "atolls"


def main():
    if not CREDENTIALS_FILE.exists():
        print(f"Error: {CREDENTIALS_FILE.name} not found.")
        print("\nTo use automated Google Drive upload via Python:")
        print("1. Go to Google Cloud Console (https://console.cloud.google.com).")
        print("2. Enable the Google Drive API.")
        print("3. Create an OAuth 2.0 Client ID (Desktop app) and download 'credentials.json'.")
        print("4. Place 'credentials.json' in this project root (it is git-ignored).")
        print("\nAlternatively:")
        print("- Open Google Drive in browser, enable 'Convert uploaded files to Google Docs editor format' in Settings, and drag-and-drop data/atolls/.")
        sys.exit(1)

    try:
        from google.oauth2.credentials import Credentials
        from google_auth_oauthlib.flow import InstalledAppFlow
        from google.auth.transport.requests import Request
        from googleapiclient.discovery import build
        from googleapiclient.http import MediaFileUpload
    except ImportError:
        print("Error: Missing Google client libraries.")
        print("Run: pip install google-api-python-client google-auth-oauthlib google-auth-httplib2")
        sys.exit(1)

    SCOPES = ["https://www.googleapis.com/auth/drive.file"]
    creds = None
    token_file = PROJECT_ROOT / "token.json"

    if token_file.exists():
        creds = Credentials.from_authorized_user_file(str(token_file), SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(str(CREDENTIALS_FILE), SCOPES)
            creds = flow.run_local_server(port=0)
        with open(token_file, "w") as token:
            token.write(creds.to_json())

    service = build("drive", "v3", credentials=creds)

    folder_metadata = {
        "name": "Comparative Dhivehi Dialect - Regional Atolls",
        "mimeType": "application/vnd.google-apps.folder",
    }
    folder = service.files().create(body=folder_metadata, fields="id").execute()
    folder_id = folder.get("id")
    print(f"Created Google Drive Folder ID: {folder_id}")

    csv_files = sorted(ATOLLS_DIR.glob("*.csv"))
    for f in csv_files:
        print(f"Uploading {f.name}...")
        file_metadata = {
            "name": f.stem,
            "parents": [folder_id],
            "mimeType": "application/vnd.google-apps.spreadsheet",  # Auto-converts CSV to Google Sheet
        }
        media = MediaFileUpload(str(f), mimetype="text/csv", resumable=True)
        uploaded = service.files().create(body=file_metadata, media_body=media, fields="id, webViewLink").execute()
        print(f" -> Created Sheet: {uploaded.get('webViewLink')}")

    print("\nAll 20 atoll sheets successfully created and converted!")


if __name__ == "__main__":
    main()
