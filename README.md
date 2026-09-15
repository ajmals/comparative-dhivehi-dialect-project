# Comparative Dhivehi Dialect Project

Welcome to the **Comparative Dhivehi Dialect Project**! This is an open-source, community-driven initiative dedicated to mapping, preserving, and comparing all regional dialects of the **Dhivehi (Maldivian)** language with each other, using **Male' (Standard Dhivehi)** as the primary anchor.

All data in this repository is completely free, open, and unrestricted for anyone to use, share, and build upon—whether for academic linguistic research, language learning tools, or computational NLP applications.

---

## Interactive Web Explorer & Collaboration
* 🌐 **[Live Web App (GitHub Pages)](https://ajmals.github.io/comparative-dhivehi-dialect-project/)** — Interactive explorer with instant search, script toggles (Thaana / Latin), dialect comparison cards, and filters.
* 📊 **[dhivehi_language_comparision.csv](dhivehi_language_comparision.csv)** — Master dataset file.

### Open Collaboration
Language changes, dialects are diverse, and corrections are always welcome! If you spot a mistake, want to suggest a better term, or wish to contribute new words or dialect variants, you can collaborate directly with us:
* **[Google Sheets Comparative Table](https://docs.google.com/spreadsheets/d/1eNV8vGmLK5fiN4gR276K0aZQsV8hcCFjA3XVrmLahTQ/edit)**

Anyone is free to comment and suggest edits on the Google Sheet. These suggestions are reviewed periodically and manually merged back into the master CSV file in this repository.

---

## Project Goals & Objectives

The primary aims of this project are:

1. **Compare Dialects with Foreign Neighboring Languages**: Systematically evaluate lexical and phonetic relationships among regional Dhivehi dialects and neighboring foreign languages (Sinhala, Malayalam, and Arabic).
2. **Understand the Origin and Evolution of Maldivian Words**: Trace etymology, sound shifts, and historical roots to gain deeper insights into how the Maldivian language developed across different atolls over time.
3. **Preserve and Document Regional Dialects**: Document under-represented or endangered dialect variants (e.g., Addu, Huvadhu, Fuvahmulah, Maliku/Mahl) in standard orthographies before unique lexical variations are lost.
4. **Quantitative Dialectometry & Distance Analysis**: Apply computational methods (such as Levenshtein edit distance and normalized similarity scoring) to quantify lexical proximity and linguistic divergence between dialects.
5. **Open Linguistic Infrastructure**: Provide accessible, machine-readable datasets in both Latin transliteration and native Thaana script for linguists, NLP researchers, and language learners.

---

## Overview
The core mission of this project is the **comprehensive comparison of all Maldivian dialects with each other**. **Male' dialect** serves as the primary baseline and reference standard (being the most widely spoken and standardized national dialect), against which regional dialect variations across the archipelago and Minicoy are mapped.

In addition to intra-Dhivehi dialectal comparisons, external languages (Sinhala, Malayalam, Arabic) are included as supplementary reference points for cognate tracking, etymology, and historical contact analysis.

### Dialects & Languages Covered:
1. **Maldivian (Dhivehi) Dialects (Primary Focus)**:
   - **Male'** (Standard Dhivehi — primary reference dialect)
   - **Addu** (Southernmost atoll dialect, characterized by distinct phonetic shifts)
   - **Huvadhu** (Southern dialect, preserving unique archaic morphology and phonology)
   - **Fuvahmulah** (Distinctive dialect of the isolated central-southern single-island atoll)
   - **Maliku / Minicoy (Mahl)** (Spoken on Minicoy Island in Lakshadweep; the northernmost Dhivehi variety with unique phonology and contact influences)
   - *(Designed to be extensible to other regional and island dialect varieties)*

2. **Supplementary Comparative Languages (Reference)**:
   - **Sinhala** (Close Indo-Aryan sibling language for cognate tracking)
   - **Malayalam** (Neighboring Dravidian language with historical maritime and regional contact)
   - **Arabic** (Historical religious and cultural superstrate influence)

Each Dhivehi dialect is split into separate columns for **Latin transliteration** and the **native Thaana script** to support phonological, phonetic, and orthographic analyses. Comparison languages are provided in standardized Latin script (ISO/IAST) to maintain clarity and focus on the Maldivian variants.

---

## Edit Distance & Dialect Similarity Analysis

To provide quantitative insights into dialectal divergence, the project includes an automated pipeline to compute **Levenshtein edit distance** and **normalized similarity scores** across all language pairs using Latin transliterations.

### Calculation Methodology:
- **Levenshtein Distance**: Measures the minimum number of single-character edits (insertions, deletions, substitutions) required to transform one word into another.
- **Normalized Distance**: Computed as $\text{Normalized Distance} = \frac{\text{Raw Distance}}{\max(\text{len}(w_1), \text{len}(w_2))}$.
- **Similarity Percentage**: Calculated as $(1 - \text{Normalized Distance}) \times 100\%$.
- **Synonym & Variant Handling**: Where multiple synonyms or variants are listed (separated by `/`), the algorithm computes all cross-pair distances and identifies the best-matching cognate pair.

### Generated Analysis Datasets:
Running the edit distance pipeline produces three structured datasets in the `data/` directory:
1. **`data/concept_edit_distances.csv`** (Concept-by-concept wide table):
   - Contains raw distance, normalized distance, and similarity percentage for each dialect/language comparison against Male'.
   - Includes full intra-Dhivehi dialect pair comparisons.
   - Highlights the closest Dhivehi dialect, closest foreign language, and overall closest dialect pair per concept.
2. **`data/concept_pairwise_distances.csv`** (Tidy long-format table):
   - Standardized pairwise rows for each concept comparison (e.g., `Entity A`, `Entity B`, `Word A`, `Word B`, `Raw Distance`, `Normalized Distance`, `Similarity %`).
   - Ideal for statistical modeling, R / pandas dataframes, and visualization.
3. **`data/dialect_distance_summary_matrix.csv`** (Aggregate distance matrix):
   - Corpus-wide average normalized edit distance and similarity percentages across all entity pairs.

### How to Run the Edit Distance Calculation:
```bash
python scripts/calculate_edit_distance.py
```

### Aggregate Dialect Similarity Matrix (Sample Summary):
*Format: Average Normalized Distance (Average Similarity %) [Sample Count]*

| Dialect / Language | Male' | Addu | Huvadhu | Sinhala | Malayalam | Arabic |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Male'** | 0.00 (100.0%) | 0.1915 (80.8%) | 0.3995 (60.0%) | 0.7006 (29.9%) | 0.8489 (15.1%) | 0.8696 (13.0%) |
| **Addu** | 0.1915 (80.8%) | 0.00 (100.0%) | 0.3718 (62.8%) | 0.7417 (25.8%) | 0.8211 (17.9%) | 0.8422 (15.8%) |
| **Huvadhu** | 0.3995 (60.0%) | 0.3718 (62.8%) | 0.00 (100.0%) | 0.6820 (31.8%) | 0.8454 (15.5%) | 0.7987 (20.1%) |
| **Sinhala** | 0.7006 (29.9%) | 0.7417 (25.8%) | 0.6820 (31.8%) | 0.00 (100.0%) | — | — |
| **Malayalam** | 0.8489 (15.1%) | 0.8211 (17.9%) | 0.8454 (15.5%) | — | 0.00 (100.0%) | — |
| **Arabic** | 0.8696 (13.0%) | 0.8422 (15.8%) | 0.7987 (20.1%) | — | — | 0.00 (100.0%) |

---

## Column Descriptions

| Column Name | Description | Example |
| :--- | :--- | :--- |
| **ID** | Unique identifier with list-specific prefix | `SW100-001`, `SW215-011`, `FRZ-001` |
| **Word List** | Source or reference wordlist | `Swadesh 100`, `Swadesh 215`, `Fritz 2002 Texts` |
| **Category** | Semantic domain / lexical category | `Body Parts & Substances`, `Animals`, `Plants & Plant Parts` |
| **English** | The reference English concept or gloss term | `all`, `bark`, `house` |
| **Male' - Latin** | Standard Maldivian term in Latin transliteration | `Hurihaa` |
| **Male' - Thaana** | Standard Maldivian term in native Thaana script | `ހުރިހާ` |
| **Addu - Latin** | Addu dialect term in Latin transliteration | `Hurihaa` |
| **Addu - Thaana** | Addu dialect term in native Thaana script | `ހުރިހާ` |
| **Huvadhu - Latin** | Huvadhu dialect term in Latin transliteration | `Hurihaa` |
| **Huvadhu - Thaana** | Huvadhu dialect term in native Thaana script | `ހުރިހާ` |
| **Fuvahmulah - Latin** | Fuvahmulah dialect term in Latin transliteration | `fiñdanu` |
| **Fuvahmulah - Thaana** | Fuvahmulah dialect term in native Thaana script | `ފިނދަނު` |
| **Maliku - Latin** | Maliku / Minicoy (Mahl) term in Latin transliteration | `Hurihaa` |
| **Maliku - Thaana** | Maliku / Minicoy (Mahl) term in native Thaana script | `ހުރިހާ` |
| **Sinhala** | Sinhala comparative term(s) in Latin transliteration | `Hama / Òkkòma` |
| **Malayalam** | Malayalam comparative term(s) in Latin transliteration | `Èllāṃ / Sarvva` |
| **Arabic** | Arabic comparative term(s) in Latin transliteration | `Kulla` |
| **Notes** | Optional contextual, grammatical, or source notes | `Fritz (2002) p.2` |

*Note: Where multiple words correspond to a single concept, they are separated by a slash (` / `).*

---

## Dialectal and Transliteration Notes

- **Thaana Orthography**: Native Dhivehi words are spelled according to standard Maldivian conventions in the Thaana script columns.
- **Latin Transliteration**: Consonants and vowels (Fili) are mapped phonetically.
- **Diacritics**: Comparative columns (Sinhala, Malayalam, Arabic) use standard ISO/IAST diacritic marks (such as macrons like `ā` for long vowels, and underdots like `ḍ` or `ṭ` for retroflex consonants) to preserve exact pronunciation profiles.

---

## Repository Structure

The repository is organized to prioritize linguistic data and comparative tables while keeping technical automation, distance calculation, and extraction scripts in a dedicated folder:

```
├── dhivehi_language_comparision.csv       # Primary master comparative dataset
├── data/
│   ├── concept_edit_distances.csv         # Per-concept edit distance & similarity breakdown
│   ├── concept_pairwise_distances.csv     # Tidy long-format pairwise distance table
│   ├── dialect_distance_summary_matrix.csv# Aggregate dialect distance & similarity matrix
│   ├── extractions/                       # Dialect text extractions & vocabulary tables (Fritz 2002)
│   ├── raw/                               # Raw source wordlists (Swadesh 100/215, Wiktionary modules)
│   └── references/                        # Reference literature PDFs and scanned materials
└── scripts/                               # Technical automation, data compilation & analysis scripts
    ├── requirements.txt                   # Script dependencies
    ├── calculate_edit_distance.py         # Levenshtein distance & similarity calculation pipeline
    ├── sync_from_sheets.py                # Automated Google Sheets synchronization script
    ├── build_dataset.py                   # Master dataset compilation pipeline
    ├── build_full_t1_dataset.py           # Dialect Story T1 extraction builder
    ├── create_4col_mapping.py             # 4-column vocabulary mapping generator
    ├── export_p2_p3.py                    # Story T1 baseline word alignment
    ├── parse_t1_full.py                   # Text parsing helper
    ├── process_pdf.py                     # Concepticon wordlist fetcher
    └── process_story_words.py             # PDF layout processing tool
```

---

## References & Sources
- **[Swadesh 1955 Concept List (PDF)](https://s3.nexus.mpcdf.mpg.de/eva-dlce-concepticon/Swadesh1955.pdf)**: The original reference paper outlining the 100-concept list (*Towards a satisfactory calibration of glottochronology*, Morris Swadesh, 1955).
- **Fritz, Sonja (2002)**: *The Dhivehi Language: A Descriptive and Historical Grammar of Maldivian and Its Dialects*, Vol II: Materials.


