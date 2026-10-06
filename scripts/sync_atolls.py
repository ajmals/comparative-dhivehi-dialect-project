#!/usr/bin/env python3
"""
Sync all regional atoll CSV files directly from their shared Google Sheets.
Downloads each spreadsheet via the Google Sheets export API as raw CSV,
validates schema integrity, and updates data/atolls/*.csv.

Optional flag:
  --compile: Automatically rebuilds data/compiled/dhivehi_islands_unified.csv
  --atoll <name/code>: Sync only a specific atoll (e.g. 'HA' or '20_S_seenu_addu')
  --dry-run: Test download without writing to disk
"""

import sys
import os
import json
import argparse
import urllib.request
import csv
import io
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CONFIG_PATH = PROJECT_ROOT / "scripts" / "atoll_sheets_config.json"
ATOLLS_DIR = PROJECT_ROOT / "data" / "atolls"


def load_config():
    if not CONFIG_PATH.exists():
        print(f"Error: Config file not found at {CONFIG_PATH}", file=sys.stderr)
        sys.exit(1)
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def sync_single_atoll(name: str, sheet_id: str, dry_run: bool = False) -> bool:
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            content = resp.read().decode("utf-8")
    except Exception as e:
        print(f"  ✗ {name}: Failed to download ({e})", file=sys.stderr)
        return False

    # Validation
    lines = [line for line in content.splitlines() if line.strip()]
    if not lines or "ID" not in lines[0]:
        print(f"  ✗ {name}: Invalid CSV format received.", file=sys.stderr)
        return False

    reader = csv.reader(io.StringIO(content))
    header = next(reader, [])
    row_count = sum(1 for _ in reader)

    if row_count < 10:
        print(f"  ✗ {name}: Suspicious row count ({row_count} rows). Aborting save.", file=sys.stderr)
        return False

    target_file = ATOLLS_DIR / f"{name}.csv"

    if dry_run:
        print(f"  ✓ [DRY RUN] {name}: {row_count} rows, {len(header)} cols (ID: {sheet_id})")
        return True

    ATOLLS_DIR.mkdir(parents=True, exist_ok=True)
    target_file.write_text(content, encoding="utf-8")
    print(f"  ✓ {name}: Synced {row_count} rows, {len(header)} cols -> {target_file.name}")
    return True


def sync_all(filter_atoll: str = None, compile_after: bool = False, dry_run: bool = False):
    config = load_config()
    sheets = config.get("sheets", {})

    print(f"Starting Atolls Sync ({len(sheets)} configured sheets)...")
    if dry_run:
        print("Note: Running in DRY-RUN mode. No files will be modified.")

    successful = 0
    failed = 0

    for name, sheet_id in sorted(sheets.items()):
        if filter_atoll:
            # Check if filter matches prefix (e.g. '01', 'HA', '01_HA')
            tokens = name.lower().split("_")
            if filter_atoll.lower() not in (name.lower(), tokens[0], tokens[1]):
                continue

        ok = sync_single_atoll(name, sheet_id, dry_run=dry_run)
        if ok:
            successful += 1
        else:
            failed += 1

    print(f"\nSync complete: {successful} successful, {failed} failed.")

    if compile_after and not dry_run and successful > 0:
        print("\nRebuilding unified relational island dataset...")
        try:
            from compile_islands import compile_all
            compile_all()
        except ImportError:
            # Fallback to running compile_islands.py directly
            import subprocess
            subprocess.run([sys.executable, str(PROJECT_ROOT / "scripts" / "compile_islands.py")], check=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Sync regional atoll CSVs from Google Sheets.")
    parser.add_argument("--atoll", type=str, default=None, help="Filter by atoll code or name (e.g., 'HA', '20_S_seenu_addu')")
    parser.add_argument("--compile", action="store_true", help="Automatically run compile_islands.py after syncing")
    parser.add_argument("--dry-run", action="store_true", help="Download and validate without modifying disk")

    args = parser.parse_args()
    sync_all(filter_atoll=args.atoll, compile_after=args.compile, dry_run=args.dry_run)
