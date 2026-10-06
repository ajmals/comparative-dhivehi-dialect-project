#!/usr/bin/env python3
"""
Roll up island-level micro-dialect data into the Master Comparison Dataset.
Calculates the statistical consensus (most common word / mode) across islands
for each dialect region (Addu, Huvadhu, Fuvahmulah) and populates dedicated
Consensus and Contributed column pairs in dhivehi_language_comparision.csv.

Flags:
  --overwrite-contributed: Overwrite Contributed columns with Consensus values
  --verify: Print a divergence report comparing Consensus vs Contributed
"""

import sys
import os
import csv
import argparse
from pathlib import Path
from collections import Counter
from typing import Dict, List, Tuple, Optional

PROJECT_ROOT = Path(__file__).resolve().parent.parent
MASTER_CSV = PROJECT_ROOT / "dhivehi_language_comparision.csv"
ATOLLS_DIR = PROJECT_ROOT / "data" / "atolls"

DIALECT_ATOLL_MAP = {
    "Addu": [ATOLLS_DIR / "20_S_seenu_addu.csv"],
    "Huvadhu": [
        ATOLLS_DIR / "17_GA_gaafu_alifu.csv",
        ATOLLS_DIR / "18_GDh_gaafu_dhaalu.csv",
    ],
    "Fuvahmulah": [ATOLLS_DIR / "19_GN_gnaviyani.csv"],
}


def compute_island_consensus(atoll_files: List[Path]) -> Dict[str, Dict[str, Tuple[str, str, float]]]:
    """
    For a set of atoll CSV files, compute the consensus (mode) term for Latin and Thaana
    for each concept ID.
    Returns: { concept_id: { 'latin': (mode_word, count, pct), 'thaana': (mode_word, count, pct) } }
    """
    data_by_id = {}

    for file_path in atoll_files:
        if not file_path.exists():
            continue
        with open(file_path, mode="r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            fieldnames = reader.fieldnames or []

            # Find island-specific column pairs
            island_names = []
            for col in fieldnames:
                if col.endswith(" - Latin") and col not in ("Standard Male' - Latin", "Benchmark - Latin"):
                    isl = col[:-8]
                    island_names.append(isl)

            for row in reader:
                cid = row.get("ID", "").strip()
                if not cid:
                    continue
                if cid not in data_by_id:
                    data_by_id[cid] = {"latin_tokens": [], "thaana_tokens": [], "bench_latin": "", "bench_thaana": ""}

                bench_lat = row.get("Benchmark - Latin", "").strip()
                bench_tha = row.get("Benchmark - Thaana", "").strip()
                if bench_lat and not data_by_id[cid]["bench_latin"]:
                    data_by_id[cid]["bench_latin"] = bench_lat
                if bench_tha and not data_by_id[cid]["bench_thaana"]:
                    data_by_id[cid]["bench_thaana"] = bench_tha

                for isl in island_names:
                    isl_lat = row.get(f"{isl} - Latin", "").strip() or bench_lat
                    isl_tha = row.get(f"{isl} - Thaana", "").strip() or bench_tha
                    if isl_lat:
                        data_by_id[cid]["latin_tokens"].append(isl_lat)
                    if isl_tha:
                        data_by_id[cid]["thaana_tokens"].append(isl_tha)

    consensus_result = {}
    for cid, rec in data_by_id.items():
        # Compute Latin mode
        lat_tokens = rec["latin_tokens"]
        if lat_tokens:
            counts_lat = Counter(lat_tokens)
            mode_lat, freq_lat = counts_lat.most_common(1)[0]
            pct_lat = round((freq_lat / len(lat_tokens)) * 100, 1)
        else:
            mode_lat, freq_lat, pct_lat = rec["bench_latin"], 0, 0.0

        # Compute Thaana mode
        tha_tokens = rec["thaana_tokens"]
        if tha_tokens:
            counts_tha = Counter(tha_tokens)
            mode_tha, freq_tha = counts_tha.most_common(1)[0]
            pct_tha = round((freq_tha / len(tha_tokens)) * 100, 1)
        else:
            mode_tha, freq_tha, pct_tha = rec["bench_thaana"], 0, 0.0

        consensus_result[cid] = {
            "latin": (mode_lat, freq_lat, pct_lat),
            "thaana": (mode_tha, freq_tha, pct_tha),
        }

    return consensus_result


def rollup(overwrite_contributed: bool = False, verify_only: bool = False):
    if not MASTER_CSV.exists():
        print(f"Error: {MASTER_CSV} not found.", file=sys.stderr)
        sys.exit(1)

    print("Computing consensus from 20 regional atoll datasets...")
    dialect_consensus = {}
    for dialect, paths in DIALECT_ATOLL_MAP.items():
        dialect_consensus[dialect] = compute_island_consensus(paths)
        print(f"  ✓ Processed {dialect} across {len(paths)} atoll file(s)")

    # Read master CSV
    with open(MASTER_CSV, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        original_fields = list(reader.fieldnames or [])
        rows = list(reader)

    # Verification / Divergence report
    divergences = []
    for r in rows:
        cid = r.get("ID", "")
        for dialect in ("Addu", "Huvadhu", "Fuvahmulah"):
            cons_lat = dialect_consensus[dialect].get(cid, {}).get("latin", ("", 0, 0.0))[0]
            # Check existing columns
            contr_lat = (
                r.get(f"{dialect} - Contributed - Latin")
                or r.get(f"{dialect} - Latin")
                or ""
            ).strip()

            if cons_lat and contr_lat and cons_lat.lower() != contr_lat.lower():
                divergences.append({
                    "ID": cid,
                    "English": r.get("English", ""),
                    "Dialect": dialect,
                    "Consensus": cons_lat,
                    "Contributed": contr_lat,
                })

    if verify_only:
        print(f"\n--- Divergence Report: {len(divergences)} concept differences found ---")
        if not divergences:
            print("Consensus and Contributed columns are in 100% agreement!")
        else:
            for d in divergences[:20]:
                print(f"  [{d['ID']}] {d['English']} ({d['Dialect']}): Consensus='{d['Consensus']}' vs Contributed='{d['Contributed']}'")
            if len(divergences) > 20:
                print(f"  ... and {len(divergences) - 20} more.")
        return

    # Construct new output schema with Consensus and Contributed pairs
    # Target columns order:
    # ID, Word List, Category, English,
    # Male' - Latin, Male' - Thaana,
    # Addu - Consensus - Latin, Addu - Consensus - Thaana, Addu - Contributed - Latin, Addu - Contributed - Thaana,
    # Huvadhu - Consensus - Latin, Huvadhu - Consensus - Thaana, Huvadhu - Contributed - Latin, Huvadhu - Contributed - Thaana,
    # Fuvahmulah - Consensus - Latin, Fuvahmulah - Consensus - Thaana, Fuvahmulah - Contributed - Latin, Fuvahmulah - Contributed - Thaana,
    # Maliku - Latin, Maliku - Thaana,
    # Sinhala, Malayalam, Arabic, Notes

    target_fields = [
        "ID", "Word List", "Category", "English",
        "Male' - Latin", "Male' - Thaana",
        "Addu - Consensus - Latin", "Addu - Consensus - Thaana",
        "Addu - Contributed - Latin", "Addu - Contributed - Thaana",
        "Huvadhu - Consensus - Latin", "Huvadhu - Consensus - Thaana",
        "Huvadhu - Contributed - Latin", "Huvadhu - Contributed - Thaana",
        "Fuvahmulah - Consensus - Latin", "Fuvahmulah - Consensus - Thaana",
        "Fuvahmulah - Contributed - Latin", "Fuvahmulah - Contributed - Thaana",
        "Maliku - Latin", "Maliku - Thaana",
        "Sinhala", "Malayalam", "Arabic", "Notes",
    ]

    updated_rows = []
    for r in rows:
        cid = r.get("ID", "")
        new_row = {k: r.get(k, "") for k in target_fields}

        # Process each regional dialect
        for dialect in ("Addu", "Huvadhu", "Fuvahmulah"):
            cons_lat = dialect_consensus[dialect].get(cid, {}).get("latin", ("", 0, 0.0))[0]
            cons_tha = dialect_consensus[dialect].get(cid, {}).get("thaana", ("", 0, 0.0))[0]

            new_row[f"{dialect} - Consensus - Latin"] = cons_lat
            new_row[f"{dialect} - Consensus - Thaana"] = cons_tha

            # Handle Contributed column
            existing_contr_lat = (
                r.get(f"{dialect} - Contributed - Latin")
                or r.get(f"{dialect} - Latin")
                or ""
            ).strip()
            existing_contr_tha = (
                r.get(f"{dialect} - Contributed - Thaana")
                or r.get(f"{dialect} - Thaana")
                or ""
            ).strip()

            if overwrite_contributed:
                new_row[f"{dialect} - Contributed - Latin"] = cons_lat
                new_row[f"{dialect} - Contributed - Thaana"] = cons_tha
            else:
                new_row[f"{dialect} - Contributed - Latin"] = existing_contr_lat or cons_lat
                new_row[f"{dialect} - Contributed - Thaana"] = existing_contr_tha or cons_tha

        updated_rows.append(new_row)

    with open(MASTER_CSV, mode="w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=target_fields)
        writer.writeheader()
        writer.writerows(updated_rows)

    print(f"\nSuccessfully updated {MASTER_CSV.name}!")
    print(f"Columns: {len(target_fields)} fields with Consensus and Contributed pairs.")
    if overwrite_contributed:
        print("Note: Contributed columns were synchronized to match the island consensus.")
    else:
        print(f"Note: Existing contributed community inputs preserved ({len(divergences)} divergence items found).")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Roll up island-level consensus into dhivehi_language_comparision.csv")
    parser.add_argument("--overwrite-contributed", action="store_true", help="Overwrite Contributed columns with Consensus values")
    parser.add_argument("--verify", action="store_true", help="Print verification and divergence report only")

    args = parser.parse_args()
    rollup(overwrite_contributed=args.overwrite_contributed, verify_only=args.verify)
