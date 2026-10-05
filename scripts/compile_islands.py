#!/usr/bin/env python3
"""
Compile all regional atoll CSVs into a single relational, machine-readable dataset.
Inherits from atoll benchmark when an island cell is left blank.
"""

import csv
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
ATOLLS_DIR = PROJECT_ROOT / "data" / "atolls"
ISLANDS_CSV = PROJECT_ROOT / "data" / "reference" / "inhabited_islands_master.csv"
OUTPUT_DIR = PROJECT_ROOT / "data" / "compiled"
OUTPUT_CSV = OUTPUT_DIR / "dhivehi_islands_unified.csv"


def load_island_metadata():
    meta = {}
    with open(ISLANDS_CSV, mode="r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for r in reader:
            key = (r["Atl"].strip(), r["Island_Name"].strip())
            meta[key] = {
                "FCODE": r.get("FCODE", ""),
                "Atoll_Name": r.get("Atoll_Name", ""),
                "Island_Dhivehi": r.get("Island_Dhivehi", ""),
                "Is_Capital": r.get("Is_Capital", "N"),
                "Lat_DD": r.get("Lat_DD", ""),
                "Lon_DD": r.get("Lon_DD", ""),
            }
    return meta


def compile_all():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    island_meta = load_island_metadata()

    atoll_files = sorted(ATOLLS_DIR.glob("*.csv"))
    if not atoll_files:
        print("No atoll CSV files found in data/atolls/")
        return

    output_rows = []

    for file_path in atoll_files:
        parts = file_path.stem.split("_")
        # e.g., 01_HA_haa_alifu -> parts[1] is 'HA'
        atoll_code = parts[1]

        with open(file_path, mode="r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            fieldnames = reader.fieldnames or []

            # Extract island names from columns ending with ' - Latin'
            islands = []
            for col in fieldnames:
                if col.endswith(" - Latin") and col not in ("Standard Male' - Latin", "Benchmark - Latin"):
                    isl_name = col[:-8]
                    islands.append(isl_name)

            for row in reader:
                concept_id = row["ID"]
                category = row["Category"]
                english = row["English"]
                bench_latin = row.get("Benchmark - Latin", "")
                bench_thaana = row.get("Benchmark - Thaana", "")
                male_latin = row.get("Standard Male' - Latin", "")
                male_thaana = row.get("Standard Male' - Thaana", "")
                notes = row.get("Notes", "")

                for isl in islands:
                    isl_latin = row.get(f"{isl} - Latin", "").strip()
                    isl_thaana = row.get(f"{isl} - Thaana", "").strip()

                    # Blank cell inheritance rule
                    if not isl_latin and not isl_thaana:
                        term_latin = bench_latin
                        term_thaana = bench_thaana
                        is_variation = False
                    else:
                        term_latin = isl_latin or bench_latin
                        term_thaana = isl_thaana or bench_thaana
                        is_variation = (isl_latin != bench_latin) or (isl_thaana != bench_thaana)

                    meta = island_meta.get((atoll_code, isl), {})

                    output_rows.append({
                        "Concept_ID": concept_id,
                        "Category": category,
                        "English": english,
                        "Atoll_Code": atoll_code,
                        "Atoll_Name": meta.get("Atoll_Name", ""),
                        "Island_Name": isl,
                        "Island_Dhivehi": meta.get("Island_Dhivehi", ""),
                        "FCODE": meta.get("FCODE", ""),
                        "Is_Capital": meta.get("Is_Capital", "N"),
                        "Term_Latin": term_latin,
                        "Term_Thaana": term_thaana,
                        "Is_Distinct_Variation": "Y" if is_variation else "N",
                        "Male_Reference_Latin": male_latin,
                        "Male_Reference_Thaana": male_thaana,
                        "Benchmark_Latin": bench_latin,
                        "Benchmark_Thaana": bench_thaana,
                        "Lat_DD": meta.get("Lat_DD", ""),
                        "Lon_DD": meta.get("Lon_DD", ""),
                        "Notes": notes,
                    })

    fieldnames = [
        "Concept_ID",
        "Category",
        "English",
        "Atoll_Code",
        "Atoll_Name",
        "Island_Name",
        "Island_Dhivehi",
        "FCODE",
        "Is_Capital",
        "Term_Latin",
        "Term_Thaana",
        "Is_Distinct_Variation",
        "Male_Reference_Latin",
        "Male_Reference_Thaana",
        "Benchmark_Latin",
        "Benchmark_Thaana",
        "Lat_DD",
        "Lon_DD",
        "Notes",
    ]

    with open(OUTPUT_CSV, mode="w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(output_rows)

    print(f"Compiled {len(output_rows)} island concept records into {OUTPUT_CSV.name}")


if __name__ == "__main__":
    compile_all()
