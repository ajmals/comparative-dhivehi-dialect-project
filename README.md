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
The dataset compares standard Dhivehi vocabulary across different regional dialects and relative/neighboring languages based on the standard 100-concept Swadesh list (originally proposed by Morris Swadesh in 1955).

Included Languages & Dialects:
1. **Dhivehi Dialects**:
   - **Male'** (Standard Maldivian)
   - **Addu** (Southernmost dialect, known for major phonological shifts)
   - **Huvadhu** (Southern dialect, preserving unique archaic features)
2. **Comparative Languages**:
   - **Sinhala** (Close Relative; Indo-Aryan sibling language)
   - **Malayalam** (Coast Neighbor; Dravidian language with high historical contact)
   - **Arabic** (Significant historical superstrate influence)

Each Dhivehi dialect is split into separate columns for **Latin transliteration** and the **native Thaana script** to support phonological, phonetic, and orthographic analyses. Comparison languages are provided in standardized Latin script (ISO/IAST) to maintain clarity and focus on the Maldivian variants.

---

## Column Descriptions

| Column Name | Description |
| :--- | :--- |
| **Concept ID** | Three-digit unique identifier for the Swadesh concept (001–100) |
| **English** | The reference English concept term |
| **Male' - Latin** | Standard Maldivian term in Latin transliteration |
| **Male' - Thaana** | Standard Maldivian term in native Thaana script |
| **Addu - Latin** | Addu dialect term in Latin transliteration |
| **Addu - Thaana** | Addu dialect term in native Thaana script |
| **Huvadhu - Latin** | Huvadhu dialect term in Latin transliteration |
| **Huvadhu - Thaana** | Huvadhu dialect term in native Thaana script |
| **Sinhala** | Sinhala comparative term(s) in Latin transliteration |
| **Malayalam** | Malayalam comparative term(s) in Latin transliteration |
| **Arabic** | Arabic comparative term(s) in Latin transliteration |

*Note: Where multiple words correspond to a single concept, they are separated by a slash (` / `).*

---

## Dialectal and Transliteration Notes

- **Thaana Orthography**: Native Dhivehi words are spelled according to standard Maldivian conventions in the Thaana script columns.
- **Latin Transliteration**: Consonants and vowels (Fili) are mapped phonetically.
- **Diacritics**: Comparative columns (Sinhala, Malayalam, Arabic) use standard ISO/IAST diacritic marks (such as macrons like `ā` for long vowels, and underdots like `ḍ` or `ṭ` for retroflex consonants) to preserve exact pronunciation profiles.

---

## References & Sources
- **[Swadesh 1955 Concept List (PDF)](https://s3.nexus.mpcdf.mpg.de/eva-dlce-concepticon/Swadesh1955.pdf)**: The original reference paper outlining the 100-concept list (*Towards a satisfactory calibration of glottochronology*, Morris Swadesh, 1955).
