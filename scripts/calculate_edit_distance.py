#!/usr/bin/env python3
"""
Calculate edit distance (Levenshtein) and similarity metrics across Dhivehi dialects 
and comparative reference languages using Latin transliterations.

Input: dhivehi_language_comparision.csv (READ-ONLY)
Outputs:
  - data/concept_edit_distances.csv (Concept-by-concept wide table with closest matches and distances)
  - data/concept_pairwise_distances.csv (Tidy long-format table of all pairwise comparisons)
  - data/dialect_distance_summary_matrix.csv (Corpus-wide aggregate average distance matrix)
"""

import os
import re
import csv
from itertools import combinations
from typing import List, Dict, Tuple, Optional

# Define Dialects and Comparison Languages
DHIVEHI_DIALECTS = [
    ("Male'", "Male' - Latin"),
    ("Addu", "Addu - Latin"),
    ("Huvadhu", "Huvadhu - Latin"),
    ("Fuvahmulah", "Fuvahmulah - Latin"),
    ("Maliku", "Maliku - Latin"),
]

FOREIGN_LANGUAGES = [
    ("Sinhala", "Sinhala"),
    ("Malayalam", "Malayalam"),
    ("Arabic", "Arabic"),
]

ALL_ENTITIES = DHIVEHI_DIALECTS + FOREIGN_LANGUAGES
DHIVEHI_KEYS = [name for name, _ in DHIVEHI_DIALECTS]
ALL_KEYS = [name for name, _ in ALL_ENTITIES]


def levenshtein_distance(s1: str, s2: str) -> int:
    """Compute standard Levenshtein distance between two strings."""
    if s1 == s2:
        return 0
    if len(s1) == 0:
        return len(s2)
    if len(s2) == 0:
        return len(s1)

    v0 = list(range(len(s2) + 1))
    v1 = [0] * (len(s2) + 1)

    for i in range(len(s1)):
        v1[0] = i + 1
        for j in range(len(s2)):
            cost = 0 if s1[i] == s2[j] else 1
            v1[j + 1] = min(v1[j] + 1, v0[j + 1] + 1, v0[j] + cost)
        v0, v1 = v1, v0

    return v0[len(s2)]


def clean_word(token: str) -> str:
    """Clean individual word token for comparison."""
    # Remove parenthesized notes like (pl.), (adj.)
    token = re.sub(r"\(.*?\)", "", token)
    # Remove punctuation, hyphens, and whitespace
    token = token.strip(" ,?!.*\"'[]-–—")
    if token in ("-", "--", "---", "N/A", "n/a", "?", "???"):
        return ""
    return token.strip()


def parse_word_list(cell_value: Optional[str]) -> List[str]:
    """Parse a cell containing slash-separated words into a clean list of words."""
    if not cell_value:
        return []
    raw_tokens = cell_value.split("/")
    cleaned = []
    for t in raw_tokens:
        w = clean_word(t)
        if w:
            cleaned.append(w)
    return cleaned


def find_best_match(words_a: List[str], words_b: List[str]) -> Optional[Dict]:
    """
    Find the pair (w_a, w_b) with minimum edit distance and maximum similarity.
    Returns dictionary with details or None if either word list is empty.
    """
    if not words_a or not words_b:
        return None

    best_match = None
    min_norm_dist = float("inf")
    min_raw_dist = float("inf")

    for wa in words_a:
        for wb in words_b:
            wa_lower = wa.lower()
            wb_lower = wb.lower()
            raw_dist = levenshtein_distance(wa_lower, wb_lower)
            max_len = max(len(wa_lower), len(wb_lower))
            norm_dist = raw_dist / max_len if max_len > 0 else 0.0
            sim_pct = round((1.0 - norm_dist) * 100, 2)

            # Pick pair with lowest normalized distance (tie-break on raw distance)
            if (norm_dist < min_norm_dist) or (norm_dist == min_norm_dist and raw_dist < min_raw_dist):
                min_norm_dist = norm_dist
                min_raw_dist = raw_dist
                best_match = {
                    "word_a": wa,
                    "word_b": wb,
                    "raw_dist": raw_dist,
                    "norm_dist": round(norm_dist, 4),
                    "sim_pct": sim_pct,
                }

    return best_match


def process_dataset(input_csv: str, output_dir: str):
    """Read source dataset and generate comparison outputs without modifying input."""
    if not os.path.exists(input_csv):
        raise FileNotFoundError(f"Input file not found: {input_csv}")

    os.makedirs(output_dir, exist_ok=True)

    rows = []
    with open(input_csv, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)

    print(f"Loaded {len(rows)} concepts from '{input_csv}'.")

    # Data structures for output
    concept_wide_rows = []
    pairwise_rows = []
    matrix_accum = {
        (d1, d2): {"total_norm_dist": 0.0, "total_sim": 0.0, "count": 0}
        for d1 in ALL_KEYS
        for d2 in ALL_KEYS
        if d1 != d2
    }

    for row in rows:
        concept_id = row.get("ID", "").strip()
        word_list = row.get("Word List", "").strip()
        category = row.get("Category", "").strip()
        english = row.get("English", "").strip()

        # Extract parsed words for each dialect / language
        entity_words = {}
        for name, col_name in ALL_ENTITIES:
            entity_words[name] = parse_word_list(row.get(col_name, ""))

        wide_row = {
            "ID": concept_id,
            "Word List": word_list,
            "Category": category,
            "English": english,
            "Male'_Word": "/".join(entity_words["Male'"]),
        }

        # 1. Compare Male' to all other Dhivehi dialects and foreign languages
        male_words = entity_words["Male'"]
        closest_dhivehi_dialect = []
        best_dhivehi_sim = -1.0
        best_dhivehi_dist = float("inf")

        closest_foreign_lang = []
        best_foreign_sim = -1.0
        best_foreign_dist = float("inf")

        for other_name, _ in ALL_ENTITIES:
            if other_name == "Male'":
                continue

            match = find_best_match(male_words, entity_words[other_name])
            other_clean = other_name.replace(" ", "_").replace("'", "")
            col_prefix = f"Male_vs_{other_clean}"

            if match:
                wide_row[f"{col_prefix}_Best_Pair"] = f"{match['word_a']} ~ {match['word_b']}"
                wide_row[f"{col_prefix}_Raw_Dist"] = match["raw_dist"]
                wide_row[f"{col_prefix}_Norm_Dist"] = match["norm_dist"]
                wide_row[f"{col_prefix}_Sim_Pct"] = match["sim_pct"]

                # Check Dhivehi regional closeness to Male'
                if other_name in DHIVEHI_KEYS:
                    if match["sim_pct"] > best_dhivehi_sim:
                        best_dhivehi_sim = match["sim_pct"]
                        best_dhivehi_dist = match["raw_dist"]
                        closest_dhivehi_dialect = [other_name]
                    elif match["sim_pct"] == best_dhivehi_sim:
                        closest_dhivehi_dialect.append(other_name)
                else:
                    # Check Foreign closeness to Male'
                    if match["sim_pct"] > best_foreign_sim:
                        best_foreign_sim = match["sim_pct"]
                        best_foreign_dist = match["raw_dist"]
                        closest_foreign_lang = [other_name]
                    elif match["sim_pct"] == best_foreign_sim:
                        closest_foreign_lang.append(other_name)
            else:
                wide_row[f"{col_prefix}_Best_Pair"] = ""
                wide_row[f"{col_prefix}_Raw_Dist"] = ""
                wide_row[f"{col_prefix}_Norm_Dist"] = ""
                wide_row[f"{col_prefix}_Sim_Pct"] = ""

        # Summary flags for Male' comparison
        if best_dhivehi_sim >= 0:
            wide_row["Male_Closest_Dhivehi_Dialect"] = "/".join(closest_dhivehi_dialect)
            wide_row["Male_Closest_Dhivehi_Sim_Pct"] = best_dhivehi_sim
            wide_row["Male_Closest_Dhivehi_Raw_Dist"] = best_dhivehi_dist
        else:
            wide_row["Male_Closest_Dhivehi_Dialect"] = ""
            wide_row["Male_Closest_Dhivehi_Sim_Pct"] = ""
            wide_row["Male_Closest_Dhivehi_Raw_Dist"] = ""

        if best_foreign_sim >= 0:
            wide_row["Male_Closest_Foreign_Lang"] = "/".join(closest_foreign_lang)
            wide_row["Male_Closest_Foreign_Sim_Pct"] = best_foreign_sim
            wide_row["Male_Closest_Foreign_Raw_Dist"] = best_foreign_dist
        else:
            wide_row["Male_Closest_Foreign_Lang"] = ""
            wide_row["Male_Closest_Foreign_Sim_Pct"] = ""
            wide_row["Male_Closest_Foreign_Raw_Dist"] = ""

        if best_dhivehi_sim >= 0 and best_foreign_sim >= 0:
            if best_dhivehi_sim > best_foreign_sim:
                wide_row["Male_Is_Dhivehi_Dialect_Closer"] = "Yes (Dialect closer)"
            elif best_dhivehi_sim < best_foreign_sim:
                wide_row["Male_Is_Dhivehi_Dialect_Closer"] = "No (Foreign closer)"
            else:
                wide_row["Male_Is_Dhivehi_Dialect_Closer"] = "Equal"
        else:
            wide_row["Male_Is_Dhivehi_Dialect_Closer"] = ""

        # 2. Add all intra-Dhivehi dialect comparisons and track overall closest dialect pair
        overall_closest_dhivehi_pairs = []
        overall_best_dhivehi_sim = -1.0
        overall_best_dhivehi_words = []

        all_dhivehi_pairs = list(combinations(DHIVEHI_KEYS, 2))
        for d1, d2 in all_dhivehi_pairs:
            match = find_best_match(entity_words[d1], entity_words[d2])
            c1 = d1.replace(' ', '_').replace("'", '')
            c2 = d2.replace(' ', '_').replace("'", '')
            pair_col = f"{c1}_vs_{c2}"
            if match:
                wide_row[f"{pair_col}_Best_Pair"] = f"{match['word_a']} ~ {match['word_b']}"
                wide_row[f"{pair_col}_Raw_Dist"] = match["raw_dist"]
                wide_row[f"{pair_col}_Norm_Dist"] = match["norm_dist"]
                wide_row[f"{pair_col}_Sim_Pct"] = match["sim_pct"]

                if match["sim_pct"] > overall_best_dhivehi_sim:
                    overall_best_dhivehi_sim = match["sim_pct"]
                    overall_closest_dhivehi_pairs = [f"{d1} ⟷ {d2}"]
                    overall_best_dhivehi_words = [f"{match['word_a']} ~ {match['word_b']}"]
                elif match["sim_pct"] == overall_best_dhivehi_sim:
                    overall_closest_dhivehi_pairs.append(f"{d1} ⟷ {d2}")
                    overall_best_dhivehi_words.append(f"{match['word_a']} ~ {match['word_b']}")
            else:
                wide_row[f"{pair_col}_Best_Pair"] = ""
                wide_row[f"{pair_col}_Raw_Dist"] = ""
                wide_row[f"{pair_col}_Norm_Dist"] = ""
                wide_row[f"{pair_col}_Sim_Pct"] = ""

        if overall_best_dhivehi_sim >= 0:
            wide_row["Overall_Closest_Dhivehi_Pair"] = " / ".join(overall_closest_dhivehi_pairs)
            wide_row["Overall_Closest_Dhivehi_Sim_Pct"] = overall_best_dhivehi_sim
            wide_row["Overall_Closest_Dhivehi_Words"] = " / ".join(overall_best_dhivehi_words)
        else:
            wide_row["Overall_Closest_Dhivehi_Pair"] = ""
            wide_row["Overall_Closest_Dhivehi_Sim_Pct"] = ""
            wide_row["Overall_Closest_Dhivehi_Words"] = ""

        concept_wide_rows.append(wide_row)

        # 3. Build Long Pairwise Records
        all_unique_pairs = list(combinations(ALL_KEYS, 2))
        for d1, d2 in all_unique_pairs:
            match = find_best_match(entity_words[d1], entity_words[d2])
            if match:
                is_dhivehi_pair = (d1 in DHIVEHI_KEYS and d2 in DHIVEHI_KEYS)
                pairwise_rows.append({
                    "ID": concept_id,
                    "Word List": word_list,
                    "Category": category,
                    "English": english,
                    "Entity_A": d1,
                    "Entity_B": d2,
                    "Word_A": match["word_a"],
                    "Word_B": match["word_b"],
                    "Raw_Distance": match["raw_dist"],
                    "Normalized_Distance": match["norm_dist"],
                    "Similarity_Pct": match["sim_pct"],
                    "Is_Dhivehi_Pair": "Yes" if is_dhivehi_pair else "No",
                })
                # Accumulate for summary matrix
                matrix_accum[(d1, d2)]["total_norm_dist"] += match["norm_dist"]
                matrix_accum[(d1, d2)]["total_sim"] += match["sim_pct"]
                matrix_accum[(d1, d2)]["count"] += 1

                matrix_accum[(d2, d1)]["total_norm_dist"] += match["norm_dist"]
                matrix_accum[(d2, d1)]["total_sim"] += match["sim_pct"]
                matrix_accum[(d2, d1)]["count"] += 1

    # Write Concept Wide CSV
    wide_csv_path = os.path.join(output_dir, "concept_edit_distances.csv")
    if concept_wide_rows:
        fieldnames = list(concept_wide_rows[0].keys())
        with open(wide_csv_path, mode="w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(concept_wide_rows)
        print(f"Generated: {wide_csv_path} ({len(concept_wide_rows)} rows)")

    # Write Pairwise Long CSV
    pairwise_csv_path = os.path.join(output_dir, "concept_pairwise_distances.csv")
    if pairwise_rows:
        fieldnames = list(pairwise_rows[0].keys())
        with open(pairwise_csv_path, mode="w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(pairwise_rows)
        print(f"Generated: {pairwise_csv_path} ({len(pairwise_rows)} rows)")

    # Write Summary Matrix CSV
    matrix_csv_path = os.path.join(output_dir, "dialect_distance_summary_matrix.csv")
    with open(matrix_csv_path, mode="w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Dialect / Language"] + ALL_KEYS)
        for d1 in ALL_KEYS:
            row_vals = [d1]
            for d2 in ALL_KEYS:
                if d1 == d2:
                    row_vals.append("0.00 (100.0%) [n=-]")
                else:
                    acc = matrix_accum.get((d1, d2))
                    if acc and acc["count"] > 0:
                        avg_norm = acc["total_norm_dist"] / acc["count"]
                        avg_sim = acc["total_sim"] / acc["count"]
                        row_vals.append(f"{avg_norm:.4f} ({avg_sim:.1f}%) [n={acc['count']}]")
                    else:
                        row_vals.append("N/A")
            writer.writerow(row_vals)
    print(f"Generated: {matrix_csv_path}")


if __name__ == "__main__":
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    input_file = os.path.join(base_dir, "dhivehi_language_comparision.csv")
    output_directory = os.path.join(base_dir, "data")
    process_dataset(input_file, output_directory)
