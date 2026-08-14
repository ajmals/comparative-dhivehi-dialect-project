import csv
import json
import os
import pandas as pd

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
EXTRACTIONS_DIR = os.path.join(PROJECT_ROOT, "data", "extractions")

# Unique word mappings extracted from the story interlinear analysis
# 4 columns: English, Male, Addu, Fuvahmulah
word_mappings = [
    {"English": "fiñdanā bird", "Male": "fiñdanfuḷu", "Addu": "fiñdanā", "Fuvahmulah": "fiñdanu"},
    {"English": "boñdanā bird", "Male": "boḍanfuḷu", "Addu": "boñdanā", "Fuvahmulah": "boñdanu"},
    {"English": "house", "Male": "ge", "Addu": "gē", "Fuvahmulah": "gē"},
    {"English": "lives / live", "Male": "uḷē", "Addu": "ebege", "Fuvahmulah": "ebege"},
    {"English": "to build / built", "Male": "aḷafi", "Addu": "eḍafie", "Fuvahmulah": "eḍī"},
    {"English": "having built", "Male": "aḷaigen", "Addu": "eḍi", "Fuvahmulah": "eḍāgen"},
    {"English": "wood / timber", "Male": "vakaru", "Addu": "vakara", "Fuvahmulah": "vakaro"},
    {"English": "teak wood", "Male": "hai", "Addu": "hai", "Fuvahmulah": "hai"},
    {"English": "rotten", "Male": "fī", "Addu": "fī", "Fuvahmulah": "fī"},
    {"English": "brushwood", "Male": "lieśi", "Addu": "lieśi", "Fuvahmulah": "lieśi"},
    {"English": "having gone / going", "Male": "gos", "Addu": "gosfei", "Fuvahmulah": "gohofē"},
    {"English": "to cut / cut", "Male": "kaṇḍan", "Addu": "kaṇḍāś", "Fuvahmulah": "keṇḍī"},
    {"English": "two", "Male": "de", "Addu": "de", "Fuvahmulah": "de"},
    {"English": "people", "Male": "mīhun", "Addu": "verie", "Fuvahmulah": "mīhun"},
    {"English": "night / at night", "Male": "reaku", "Addu": "reaki", "Fuvahmulah": "rē"},
    {"English": "rain / heavy rain", "Male": "vilāgaḍu", "Addu": "vissāra", "Fuvahmulah": "vissāra"},
    {"English": "strong", "Male": "gada", "Addu": "gada", "Fuvahmulah": "gada"},
    {"English": "collapsed / fell", "Male": "veṭṭijje", "Addu": "uduhige", "Fuvahmulah": "veṭṭīge"},
    {"English": "head", "Male": "bō", "Addu": "bō", "Fuvahmulah": "bola"},
    {"English": "wave", "Male": "raḷu", "Addu": "raḷu", "Fuvahmulah": "raḷo"},
    {"English": "hitting / striking", "Male": "jehē", "Addu": "jahā", "Fuvahmulah": "jahā"},
    {"English": "to sleep / sleeping", "Male": "nidālāne", "Addu": "nidāṇe", "Fuvahmulah": "nidanna"},
    {"English": "place", "Male": "tan", "Addu": "tān", "Fuvahmulah": "tan"},
    {"English": "giving / to give", "Male": "dī", "Addu": "dēś", "Fuvahmulah": "denna"},
    {"English": "elder brother", "Male": "bēbē", "Addu": "bēbē", "Fuvahmulah": "bēbē"},
    {"English": "table", "Male": "āśi", "Addu": "āśe", "Fuvahmulah": "aśi"},
    {"English": "big", "Male": "boḍu", "Addu": "boḍa", "Fuvahmulah": "boṇḍo"},
    {"English": "to lie down / lying", "Male": "onnāś", "Addu": "veśionnaś", "Fuvahmulah": "veśīonnaha"},
    {"English": "cried / said", "Male": "govāli", "Addu": "beṇafi", "Fuvahmulah": "beṇi"},
    {"English": "they say (quotation particle)", "Male": "eve", "Addu": "ē", "Fuvahmulah": "ai"}
]

# Convert to DataFrame
df = pd.DataFrame(word_mappings)

# Remove any duplicates just in case
df = df.drop_duplicates(subset=["English", "Male", "Addu", "Fuvahmulah"])

# Save 4-column CSV
csv_path = os.path.join(EXTRACTIONS_DIR, "dhivehi_dialect_vocabulary_mapping.csv")
df.to_csv(csv_path, index=False, encoding="utf-8-sig")

# Save 4-column Markdown table
md_path = os.path.join(EXTRACTIONS_DIR, "dhivehi_dialect_vocabulary_mapping.md")
with open(md_path, "w", encoding="utf-8") as f:
    f.write("# Dhivehi Dialects Vocabulary Mapping (4-Column Comparative Table)\n\n")
    f.write("Comparative 4-column alignment of English terms with Male', Addu, and Fuvahmulah dialect equivalents extracted from Sonja Fritz (2002).\n\n")
    f.write(df.to_markdown(index=False))
    f.write("\n")

print(f"Successfully generated 4-column word mapping files:\n - {csv_path}\n - {md_path}")
