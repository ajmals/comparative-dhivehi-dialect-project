#!/usr/bin/env python3
"""
Sync Google Sheets data to local CSV file.
Downloads the shared Google Sheet tab directly as a CSV and saves it.
"""

import sys
import urllib.request
from pathlib import Path

SHEET_ID = "1eNV8vGmLK5fiN4gR276K0aZQsV8hcCFjA3XVrmLahTQ"
GID = "690281837"
EXPORT_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid={GID}"

PROJECT_ROOT = Path(__file__).resolve().parent.parent
TARGET_CSV = PROJECT_ROOT / "dhivehi_language_comparision.csv"


def sync():
    print(f"Fetching data from Google Sheets (GID: {GID})...")
    req = urllib.request.Request(EXPORT_URL, headers={"User-Agent": "Mozilla/5.0"})

    try:
        with urllib.request.urlopen(req) as response:
            content = response.read().decode("utf-8")
    except Exception as e:
        print(f"Error downloading Google Sheet: {e}", file=sys.stderr)
        sys.exit(1)

    lines = [line for line in content.splitlines() if line.strip()]
    if not lines or "ID" not in lines[0]:
        print("Error: Downloaded content does not appear to be a valid comparative dataset CSV.", file=sys.stderr)
        sys.exit(1)

    TARGET_CSV.write_text(content, encoding="utf-8")
    print(f"Successfully synced {len(lines) - 1} records to {TARGET_CSV.name}!")


if __name__ == "__main__":
    sync()
