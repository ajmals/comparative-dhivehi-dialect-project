# Regional Atoll & Island Dialect Documentation
### ދިވެހިރާއްޖޭގެ މީހުން ދިރިއުޅޭ ރަށްރަށުގެ ބަހުރުވަތައް

Welcome to the **Island-Level Dialect Directory** of the Comparative Dhivehi Dialect Project. 

While the master dataset ([`dhivehi_language_comparision.csv`](../../dhivehi_language_comparision.csv)) captures high-level regional benchmarks (Male', Addu, Huvadhu, Fuvahmulah, Maliku), this directory is dedicated to **micro-dialectology**—documenting and preserving the distinct lexical items, phonetic shifts, and grammatical quirks across all **188 inhabited islands** of the Maldives.

---

## 1. Directory of Administrative Atolls (20 Files)

All files follow the official North-to-South administrative order of the Maldives and are linked to official Local Government Authority (LGA) council records and coordinates from [`ajmals/maldives-islands-dataset`](https://github.com/ajmals/maldives-islands-dataset):

| # | Code | Atoll Name | File | Inhabited Islands | Administrative Capital | Baseline Status |
| :---: | :---: | :--- | :--- | :---: | :--- | :--- |
| **01** | `HA` | Haa Alifu | [`01_HA_haa_alifu.csv`](01_HA_haa_alifu.csv) | 14 | Dhidhdhoo | Standard Male' baseline |
| **02** | `HDh` | Haa Dhaalu | [`02_HDh_haa_dhaalu.csv`](02_HDh_haa_dhaalu.csv) | 12 | Kulhudhuffushi | Standard Male' baseline |
| **03** | `Sh` | Shaviyani | [`03_Sh_shaviyani.csv`](03_Sh_shaviyani.csv) | 14 | Funadhoo | Standard Male' baseline |
| **04** | `N` | Noonu | [`04_N_noonu.csv`](04_N_noonu.csv) | 13 | Manadhoo | Standard Male' baseline |
| **05** | `R` | Raa | [`05_R_raa.csv`](05_R_raa.csv) | 15 | Ungoofaaru | Standard Male' baseline |
| **06** | `B` | Baa | [`06_B_baa.csv`](06_B_baa.csv) | 13 | Eydhafushi | Standard Male' baseline |
| **07** | `Lh` | Lhaviyani | [`07_Lh_lhaviyani.csv`](07_Lh_lhaviyani.csv) | 4 | Naifaru | Standard Male' baseline |
| **08** | `K` | Kaafu | [`08_K_kaafu.csv`](08_K_kaafu.csv) | 12 | Male' / Thulusdhoo | Male' City populated |
| **09** | `AA` | Alifu Alifu | [`09_AA_alifu_alifu.csv`](09_AA_alifu_alifu.csv) | 8 | Rasdhoo | Standard Male' baseline |
| **10** | `ADh` | Alifu Dhaalu | [`10_ADh_alifu_dhaalu.csv`](10_ADh_alifu_dhaalu.csv) | 10 | Mahibadhoo | Standard Male' baseline |
| **11** | `V` | Vaavu | [`11_V_vaavu.csv`](11_V_vaavu.csv) | 5 | Felidhoo | Standard Male' baseline |
| **12** | `M` | Meemu | [`12_M_meemu.csv`](12_M_meemu.csv) | 8 | Muli | Standard Male' baseline |
| **13** | `F` | Faafu | [`13_F_faafu.csv`](13_F_faafu.csv) | 5 | Nilandhoo | Standard Male' baseline |
| **14** | `Dh` | Dhaalu | [`14_Dh_dhaalu.csv`](14_Dh_dhaalu.csv) | 6 | Kudahuvadhoo | Standard Male' baseline |
| **15** | `Th` | Thaa | [`15_Th_thaa.csv`](15_Th_thaa.csv) | 13 | Veymandoo | Standard Male' baseline |
| **16** | `L` | Laamu | [`16_L_laamu.csv`](16_L_laamu.csv) | 11 | Fonadhoo | Standard Male' baseline |
| **17** | `GA` | Gaafu Alifu | [`17_GA_gaafu_alifu.csv`](17_GA_gaafu_alifu.csv) | 9 | Vilingili | Huvadhu baseline (Vilingili populated) |
| **18** | `GDh` | Gaafu Dhaalu | [`18_GDh_gaafu_dhaalu.csv`](18_GDh_gaafu_dhaalu.csv) | 9 | Thinadhoo | Huvadhu baseline (Thinadhoo populated) |
| **19** | `GN` | Gnaviyani | [`19_GN_gnaviyani.csv`](19_GN_gnaviyani.csv) | 1 | Fuvahmulah | Fuvahmulah populated |
| **20** | `S` | Seenu (Addu) | [`20_S_seenu_addu.csv`](20_S_seenu_addu.csv) | 6 | Hithadhoo | Addu baseline (Hithadhoo populated) |

---

## 2. File Column Schema

Each atoll file contains a uniform structure designed for easy reading and editing in spreadsheets:

| Column Header | Purpose | Example |
| :--- | :--- | :--- |
| `ID` | Standardized Concept Identifier | `SW100-001` |
| `Category` | Semantic Domain / Lexical Category | `Quantitatives`, `Body Parts` |
| `English` | Reference Concept / Gloss | `all`, `belly` |
| `Standard Male' - Latin` | National reference standard in Latin | `Hurihaa` |
| `Standard Male' - Thaana` | National reference standard in Thaana | `ހުރިހާ` |
| `Benchmark - Latin` | Common regional atoll baseline in Latin | `Hushihei` *(Addu)* |
| `Benchmark - Thaana` | Common regional atoll baseline in Thaana | `ހުށިހެއި` *(Addu)* |
| `<Island_Name> - Latin` | Island-specific variant (Latin) | `Hushihai` *(Meedhoo)* |
| `<Island_Name> - Thaana` | Island-specific variant (Thaana) | `ހުށިހައި` *(Meedhoo)* |
| `Notes` | Phonetic, grammatical, or contextual usage notes | `Pronounced with retroflex ށ` |

> [!NOTE]
> Capital islands (e.g., *Hithadhoo*, *Thinadhoo*, *Vilingili*) appear as the first island columns immediately after the Benchmark.

---

## 3. How the Benchmark & Blank Cell Rule Work

Documenting 188 islands across 100+ concepts requires tracking tens of thousands of data points. Within most atolls, neighboring islands agree on 85–95% of basic vocabulary.

To prevent contributors from having to repeatedly type identical words:

### The Rule:
1. **If your island says the word the same way as the Benchmark**:
   - **Leave the cell BLANK.**
2. **If your island has a distinct word, vowel shift, or pronunciation difference**:
   - **Type your island's word into both the Latin and Thaana columns for your island.**

```text
┌─────────────────────────────────┐
│        Atoll Benchmark          │ ◄── Common regional form (e.g., "Bonda")
└────────────────┬────────────────┘
                 │
                 ├─── [Island Column is BLANK] ───► Inherits "Bonda" automatically
                 │
                 └─── [Island Column has WORD]  ───► Records distinct local variant
```

### Real Example: Addu Atoll ([`20_S_seenu_addu.csv`](20_S_seenu_addu.csv))

| English | Standard Male' | Benchmark | Hithadhoo | Feydhoo | Hulhudhoo | Meedhoo |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **all** | Hurihaa | **Hushihei** | Hushihei | *(blank)* | *(blank)* | **Hushihai** |
| **big** | Bodu | **Bonda** | Bonda | *(blank)* | *(blank)* | *(blank)* |

* **Row 1 (`all`)**: Feydhoo and Hulhudhoo leave their cells blank because they pronounce it *Hushihei* (identical to the benchmark). Meedhoo contributors fill in *Hushihai* to capture their distinct diphthong shift.
* **Row 2 (`big`)**: All islands leave their cells blank, confirming *Bonda* is the universal term across the entire atoll.

---

## 4. Contributor Guidelines: Orthography & Conventions

To maintain high data quality across different contributors:

1. **Native Thaana Script**:
   - Use standard Dhivehi orthography with correct Sukun and Fili.
   - For sounds unique to southern dialects (such as subtle retroflexes or glottal stops), use standard Thaana letters (`އ`, `ށް`, `ޓ`, `ޅ`, `ށ`).
2. **Latin Transliteration**:
   - Standard Maldivian Latin conventions should be followed consistently:
     - Long vowels: double letters (`aa`, `ee`, `oo`).
     - Consonants: `th` for ތ, `dh` for ދ, `lh` for ޅ, `sh` for ށ, `gn` for ޏ.
3. **Multiple Variants / Synonyms**:
   - If an island uses more than one term for the same concept, separate them with a slash surrounded by spaces: `WordA / WordB`.
4. **Context & Nuance in `Notes`**:
   - Use the `Notes` column if a term is only used by elderly speakers, in poetic/archaic contexts, or in specific domains (e.g. fishing or seafaring terminology).

---

## 5. Automated GIS Compilation Pipeline

All 20 CSV files in this folder are compiled into a unified, machine-readable dataset via the build pipeline:

```bash
# From the repository root:
python scripts/compile_islands.py
```

### What the compiler produces:
- **Output File**: [`data/compiled/dhivehi_islands_unified.csv`](../compiled/dhivehi_islands_unified.csv)
- **Record Count**: **18,800 geocoded rows** (100 concepts × 188 islands).
- **Metadata Enriched**: Automatically merges every island with:
  - Official MLSA Land Feature Code (`FCODE`, e.g., `LD0568`)
  - Decimal Degree GPS coordinates (`Lat_DD`, `Lon_DD`)
  - Island Council Name & Type
  - Variation Flag (`Is_Distinct_Variation = Y / N`)
- **Use Cases**: Ready for GIS spatial mapping, isogloss boundary identification, Leaflet.js interactive maps, and computational dialectometry (e.g., Mantel correlation tests between marine travel distance and lexical distance).

---

## 6. How to Contribute

We welcome contributions from native speakers, researchers, and island councils:

1. **Via GitHub**:
   - Fork this repository.
   - Open your atoll's CSV file (e.g., `data/atolls/05_R_raa.csv`).
   - Find your island's columns and enter any distinct terms.
   - Submit a Pull Request.
2. **Via Google Sheets**:
   - You can also suggest edits and add comments directly on our shared **[Google Sheets Comparative Table](https://docs.google.com/spreadsheets/d/1eNV8vGmLK5fiN4gR276K0aZQsV8hcCFjA3XVrmLahTQ/edit)**.
