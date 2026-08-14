# Comparative Dhivehi Dialect Project

Welcome to the **Comparative Dhivehi Dialect Project**! This is an open-source, community-driven initiative aiming to map, preserve, and analyze the regional dialects of the Dhivehi (Maldivian) language alongside its close relative and neighboring languages.

All data in this repository is completely free, open, and unrestricted for anyone to use, share, and build upon—whether for academic linguistic research, language learning tools, or computational NLP applications.

---

## Dataset File & Collaboration
The primary dataset is compiled as a clean CSV file:
* **[dhivehi_language_comparision.csv](dhivehi_language_comparision.csv)**

### Open Collaboration
Language changes, dialects are diverse, and corrections are always welcome! If you spot a mistake, want to suggest a better term, or wish to contribute new words, you can collaborate directly with us:
* **[Google Sheets Comparative Table](https://docs.google.com/spreadsheets/d/1eNV8vGmLK5fiN4gR276K0aZQsV8hcCFjA3XVrmLahTQ/edit)**

Anyone is free to comment and suggest edits on the Google Sheet. These suggestions are reviewed periodically and manually merged back into the master CSV file in this repository.

---

## Overview
The dataset provides a standardized comparative vocabulary across regional Dhivehi dialects and relative/neighboring languages. The schema supports multiple comparative lists—including the classic Swadesh lists (Swadesh 100 / 215), linguistic text extracts (such as Sonja Fritz 2002 dialect stories), thematic domain lists, and custom vocabulary.

Included Languages & Dialects:
1. **Dhivehi Dialects**:
   - **Male'** (Standard Maldivian)
   - **Addu** (Southernmost dialect, known for major phonological shifts)
   - **Huvadhu** (Southern dialect, preserving unique archaic features)
   - **Fuvahmulah** (Distinct dialect spoken on the isolated island of Fuvahmulah)
2. **Comparative Languages**:
   - **Sinhala** (Close Relative; Indo-Aryan sibling language)
   - **Malayalam** (Coast Neighbor; Dravidian language with high historical contact)
   - **Arabic** (Significant historical superstrate influence)

Each Dhivehi dialect is split into separate columns for **Latin transliteration** and the **native Thaana script** to support phonological, phonetic, and orthographic analyses. Comparison languages are provided in standardized Latin script (ISO/IAST) to maintain clarity and focus on the Maldivian variants.

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

The repository is organized to prioritize linguistic data and comparative tables while keeping technical automation and extraction scripts in a dedicated folder:

```
├── dhivehi_language_comparision.csv   # Primary master comparative dataset
├── data/
│   ├── extractions/                   # Dialect text extractions & vocabulary tables (Fritz 2002)
│   ├── raw/                           # Raw source wordlists (Swadesh 100/215, Wiktionary modules)
│   └── references/                    # Reference literature PDFs and scanned materials
└── scripts/                           # Technical automation, data compilation & ETL scripts
    ├── requirements.txt               # Script dependencies
    ├── build_dataset.py               # Master dataset compilation pipeline
    ├── build_full_t1_dataset.py       # Dialect Story T1 extraction builder
    ├── create_4col_mapping.py         # 4-column vocabulary mapping generator
    ├── export_p2_p3.py                # Story T1 baseline word alignment
    ├── parse_t1_full.py               # Text parsing helper
    ├── process_pdf.py                 # Concepticon wordlist fetcher
    └── process_story_words.py         # PDF layout processing tool
```

---

## References & Sources
- **[Swadesh 1955 Concept List (PDF)](https://s3.nexus.mpcdf.mpg.de/eva-dlce-concepticon/Swadesh1955.pdf)**: The original reference paper outlining the 100-concept list (*Towards a satisfactory calibration of glottochronology*, Morris Swadesh, 1955).
- **Fritz, Sonja (2002)**: *The Dhivehi Language: A Descriptive and Historical Grammar of Maldivian and Its Dialects*, Vol II: Materials.

