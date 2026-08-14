import csv
import re
import urllib.request
import html
import os

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
RAW_DIR = os.path.join(PROJECT_ROOT, "data", "raw")

# Dynamic AST patching to support Aksharamukha on Python 3.14+
import ast
class DummyStr:
    pass
ast.Str = DummyStr

from indic_transliteration.sanscript import transliterate as indic_transliterate
from aksharamukha import transliterate as akshara_transliterate

# Transliteration function for Dhivehi / Thaana
def transliterate_thaana(text):
    mapping = {
        'ހ': 'h', 'ށ': 'sh', 'ނ': 'n', 'ރ': 'r', 'ބ': 'b', 'ޅ': 'lh',
        'ކ': 'k', 'އ': '', 'ވ': 'v', 'މ': 'm', 'ފ': 'f', 'ދ': 'dh',
        'ތ': 'th', 'ލ': 'l', 'ގ': 'g', 'ޏ': 'gn', 'ސ': 's', 'ޑ': 'd',
        'ޒ': 'z', 'ޓ': 't', 'ޔ': 'y', 'ޕ': 'p', 'ޖ': 'j', 'چین': 'ch', 'ޗ': 'ch',
        # Vowels (Fili)
        'ަ': 'a', 'ާ': 'aa', 'ި': 'i', 'ީ': 'ee', 'u': 'u', 'u': 'u', 'ު': 'u', 'ޫ': 'oo',
        'ެ': 'e', 'ޭ': 'ey', 'ޮ': 'o', 'ޯ': 'oa', 'ް': '',
    }
    
    text = text.replace('\u200e', '').replace('\u200f', '').strip()
    
    result = []
    i = 0
    while i < len(text):
        char = text[i]
        if char in mapping:
            mapped = mapping[char]
            if char == 'އ':
                if i + 1 < len(text) and text[i+1] in ['ަ', 'ާ', 'ި', 'ީ', 'ު', 'ޫ', 'ެ', 'ޭ', 'ޮ', 'ޯ']:
                    mapped = ''
            result.append(mapped)
        else:
            result.append(char)
        i += 1
    
    # Capitalize first letter of transliterated word
    res = "".join(result).strip()
    return res.capitalize() if res else ""

def clean_malayalam_romanized(text):
    chillus = {
        'ൻ': 'n',
        'ൽ': 'l',
        'ർ': 'r',
        'ൺ': 'ṇ',
        'ൿ': 'k'
    }
    for k, v in chillus.items():
        text = text.replace(k, v)
    return text

def transliterate_sinhala(text):
    if not text:
        return ""
    # Transliterate to IAST
    res = indic_transliterate(text, 'sinhala', 'iast')
    # Strip native Sinhala chars if any remain (range \u0D80-\u0DFF)
    res = re.sub(r'[\u0D80-\u0DFF]', '', res)
    return res.strip().capitalize()

def transliterate_malayalam(text):
    if not text:
        return ""
    # Transliterate to IAST
    res = indic_transliterate(text, 'malayalam', 'iast')
    res = clean_malayalam_romanized(res)
    # Strip native Malayalam chars if any remain (range \u0D00-\u0D7F)
    res = re.sub(r'[\u0D00-\u0D7F]', '', res)
    return res.strip().capitalize()

def transliterate_arabic(text):
    if not text:
        return ""
    # Clean up notes or comments in brackets if any e.g. <notes:masculine>
    text = re.sub(r'<[^>]+>', '', text).strip()
    # Transliterate to ISO
    res = akshara_transliterate.process('Arab', 'ISO', text)
    # Strip native Arabic chars if any remain (range \u0600-\u06FF)
    res = re.sub(r'[\u0600-\u06FF]', '', res)
    return res.strip().capitalize()

def parse_lua_file(filename):
    data = {}
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    matches = re.finditer(r'm\[(\d+)\]\s*=\s*(.+)', content)
    for m in matches:
        num = int(m.group(1))
        val_str = m.group(2).strip()
        terms = re.findall(r'term\s*=\s*"([^"]+)"', val_str)
        # Clean terms (remove anything like Thesaurus:...)
        clean_terms = []
        for t in terms:
            if not t.startswith("Thesaurus:"):
                clean_terms.append(t)
        data[num] = clean_terms
    return data

# Load Swadesh 100 list
sw100 = []
sw100_path = os.path.join(RAW_DIR, "swadesh_1955_100.csv")
with open(sw100_path, "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        # Normalize name
        name = row["ENGLISH"].lower().replace("*", "").strip()
        # Clean parenthesis content for easier dictionary lookup
        lookup_name = re.sub(r'\(.*?\)', '', name).strip()
        sw100.append({
            "number": row["NUMBER"],
            "english": row["ENGLISH"].replace("*", "").strip(),
            "lookup_name": lookup_name
        })

# Map 100 concepts to 207 indices
swadesh_100_to_207 = {
    "all": 17,
    "ashes": 168,
    "bark": 58,
    "belly": 85,
    "big": 27,
    "bird": 46,
    "bite": 94,
    "black": 176,
    "blood": 64,
    "bone": 65,
    "breast": 89,
    "burn": 169,
    "claw": 79,
    "cloud": 160,
    "cold": 181,
    "come": 122,
    "die": 109,
    "dog": 47,
    "drink": 92,
    "dry": 195,
    "ear": 73,
    "earth": 159,
    "eat": 93,
    "egg": 67,
    "eye": 74,
    "fat": 66,
    "feather": 70,
    "fire": 167,
    "fish": 45,
    "fly": 120,
    "foot": 80,
    "full": 182,
    "give": 128,
    "good": 185,
    "green": 173,
    "hair": 71,
    "hand": 83,
    "head": 72,
    "hear": 102,
    "heart": 90,
    "horn": 68,
    "hot": 180,
    "i": 1,
    "kill": 110,
    "knee": 82,
    "know": 103,
    "leaf": 56,
    "lie": 123,
    "liver": 91,
    "long": 28,
    "louse": 48,
    "man": 37,
    "many": 18,
    "meat": 63,
    "moon": 148,
    "mountain": 171,
    "mouth": 76,
    "name": 207,
    "neck": 87,
    "new": 183,
    "night": 177,
    "nose": 75,
    "not": 16,
    "one": 22,
    "person": 38,
    "rain": 151,
    "red": 172,
    "road": 170,
    "root": 57,
    "round": 190,
    "sand": 157,
    "say": 140,
    "see": 101,
    "seed": 55,
    "sit": 124,
    "skin": 62,
    "sleep": 107,
    "small": 32,
    "smoke": 166,
    "stand": 125,
    "star": 149,
    "stone": 156,
    "sun": 147,
    "swim": 119,
    "tail": 69,
    "that": 8,
    "this": 7,
    "thou": 2,
    "three": 24,
    "tongue": 78,
    "tooth": 77,
    "tree": 51,
    "two": 23,
    "warm": 180,
    "water": 150,
    "we": 4,
    "what": 12,
    "white": 175,
    "who": 11,
    "yellow": 174,
}

# High-quality corrections for Sinhala (fixing Wiktionary module errors)
si_corrections = {
    168: ["අළු"],          # ashes (mārga was incorrect)
    94: ["හපනවා"],        # bite
    160: ["වලාකුළ"],       # cloud
    181: ["සීතල"],         # cold
    159: ["පොළොව"],       # earth (soil/ground)
    102: ["ඇහෙනවා"],       # hear
    103: ["දන්නවා"],       # know
    140: ["කියනවා"],       # say
    101: ["දකිනවා"],       # see
    124: ["ඉඳගන්නවා"],     # sit
    107: ["නිදාගන්නවා"],    # sleep
    125: ["හිටගන්නවා"],     # stand
    119: ["පීනනවා"],       # swim
    121: ["ඇවිදිනවා"],       # walk
    180: ["උණුසුම්"],       # warm/hot
}

# High-quality corrections for Malayalam where there are missing entries
ml_corrections = {
    109: ["മരിക്കുക"],     # die
    159: ["ഭൂമി"],         # earth
}

def fetch_and_clean_module(lang_code, output_lua):
    url = f"https://en.wiktionary.org/wiki/Module:Swadesh/data/{lang_code}"
    print(f"Fetching {lang_code} Swadesh list...")
    try:
        req = urllib.request.Request(
            url, 
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        )
        with urllib.request.urlopen(req) as response:
            text = response.read().decode('utf-8')
            match = re.search(r'<pre[^>]*>(.*?)</pre>', text, re.DOTALL)
            if match:
                code_html = match.group(1)
                code_text = re.sub(r'<[^>]+>', '', code_html)
                code_text = html.unescape(code_text)
                with open(output_lua, "w", encoding="utf-8") as out:
                    out.write(code_text)
    except Exception as e:
        print(f"Error fetching {lang_code}: {e}")

lua_dv = os.path.join(RAW_DIR, "swadesh_dv.lua")
lua_si = os.path.join(RAW_DIR, "swadesh_si.lua")
lua_ml = os.path.join(RAW_DIR, "swadesh_ml.lua")
lua_ar = os.path.join(RAW_DIR, "swadesh_ar.lua")

if not os.path.exists(lua_dv):
    fetch_and_clean_module("dv", lua_dv)
if not os.path.exists(lua_si):
    fetch_and_clean_module("si", lua_si)
if not os.path.exists(lua_ml):
    fetch_and_clean_module("ml", lua_ml)
if not os.path.exists(lua_ar):
    fetch_and_clean_module("ar", lua_ar)

# Load parsed languages
dv = parse_lua_file(lua_dv)
si = parse_lua_file(lua_si)
ml = parse_lua_file(lua_ml)
ar = parse_lua_file(lua_ar)

# Apply corrections
for k, v in si_corrections.items():
    si[k] = v
for k, v in ml_corrections.items():
    ml[k] = v

# Dialectal adjustment helpers for single terms
def get_single_addu_split(lookup_name, male_thaana, male_latin):
    if lookup_name == "water":
        return "Fen", "ފެން"
    if lookup_name == "road":
        return "Magu", "މަގު"
    if lookup_name == "eye":
        return "Loa", "ލޯ"
    if lookup_name == "i":
        return "Maa", "މާ"
    if lookup_name == "thou":
        return "Thiba", "ތިބާ"
    
    if male_latin.endswith('u') and not male_latin.endswith('ou'):
        addu_latin = male_latin[:-1] + 'o'
        addu_thaana = male_thaana
        if addu_thaana.endswith('ު'):
            addu_thaana = addu_thaana[:-1] + 'ޮ'
        return addu_latin, addu_thaana
    
    return male_latin, male_thaana

def get_single_huvadhu_split(lookup_name, male_thaana, male_latin):
    if lookup_name == "water":
        return "Feng", "ފެންގް"
    if lookup_name == "road":
        return "Magu", "މަގު"
    if lookup_name == "eye":
        return "Medha", "މެދަ"
    if lookup_name == "big":
        return "Boda", "ބޮޑަ"
    
    if male_latin.endswith('u'):
        huvadhu_latin = male_latin[:-1] + 'a'
        huvadhu_thaana = male_thaana
        if huvadhu_thaana.endswith('ު'):
            huvadhu_thaana = huvadhu_thaana[:-1] + 'ަ'
        return huvadhu_latin, huvadhu_thaana
    
    return male_latin, male_thaana

# Dialectal adjustment helpers for lists of terms (uniqued)
def get_addu_split(lookup_name, dv_terms):
    addu_latins = []
    addu_thaanas = []
    for term_thaana in dv_terms:
        term_latin = transliterate_thaana(term_thaana)
        lat, th = get_single_addu_split(lookup_name, term_thaana, term_latin)
        addu_latins.append(lat)
        addu_thaanas.append(th)
    
    # Unique values while preserving order
    addu_latins = list(dict.fromkeys(addu_latins))
    addu_thaanas = list(dict.fromkeys(addu_thaanas))
    return " / ".join(addu_latins), " / ".join(addu_thaanas)

def get_huvadhu_split(lookup_name, dv_terms):
    huvadhu_latins = []
    huvadhu_thaanas = []
    for term_thaana in dv_terms:
        term_latin = transliterate_thaana(term_thaana)
        lat, th = get_single_huvadhu_split(lookup_name, term_thaana, term_latin)
        huvadhu_latins.append(lat)
        huvadhu_thaanas.append(th)
        
    huvadhu_latins = list(dict.fromkeys(huvadhu_latins))
    huvadhu_thaanas = list(dict.fromkeys(huvadhu_thaanas))
    return " / ".join(huvadhu_latins), " / ".join(huvadhu_thaanas)

SWADESH_100_CATEGORIES = {
    "all": "Quantitatives",
    "ashes": "Natural Objects & Phenomena",
    "bark": "Plants & Plant Parts",
    "belly": "Body Parts & Substances",
    "big": "Size",
    "bird": "Animals",
    "bite": "Body Sensations & Activities",
    "black": "Colors",
    "blood": "Body Parts & Substances",
    "bone": "Body Parts & Substances",
    "breast": "Body Parts & Substances",
    "burn": "Miscellaneous",
    "claw": "Body Parts & Substances",
    "cloud": "Natural Objects & Phenomena",
    "cold": "Descriptives",
    "come": "Position & Movement",
    "die": "Body Sensations & Activities",
    "dog": "Animals",
    "drink": "Body Sensations & Activities",
    "dry": "Descriptives",
    "ear": "Body Parts & Substances",
    "earth": "Natural Objects & Phenomena",
    "eat": "Body Sensations & Activities",
    "egg": "Body Parts & Substances",
    "eye": "Body Parts & Substances",
    "fat (grease)": "Body Parts & Substances",
    "feather": "Body Parts & Substances",
    "fire": "Natural Objects & Phenomena",
    "fish": "Animals",
    "fly": "Position & Movement",
    "foot": "Body Parts & Substances",
    "full": "Quantitatives",
    "give": "Position & Movement",
    "good": "Descriptives",
    "green": "Colors",
    "hair": "Body Parts & Substances",
    "hand": "Body Parts & Substances",
    "head": "Body Parts & Substances",
    "hear": "Body Sensations & Activities",
    "heart": "Body Parts & Substances",
    "horn": "Body Parts & Substances",
    "i": "Personal Pronouns",
    "kill": "Miscellaneous",
    "knee": "Body Parts & Substances",
    "know": "Body Sensations & Activities",
    "leaf": "Plants & Plant Parts",
    "lie": "Position & Movement",
    "liver": "Body Parts & Substances",
    "long": "Size",
    "louse": "Animals",
    "man": "Persons",
    "many": "Quantitatives",
    "meat (flesh)": "Body Parts & Substances",
    "moon": "Natural Objects & Phenomena",
    "mountain": "Natural Objects & Phenomena",
    "mouth": "Body Parts & Substances",
    "name": "Miscellaneous",
    "neck": "Body Parts & Substances",
    "new": "Descriptives",
    "night": "Time Periods",
    "nose": "Body Parts & Substances",
    "not": "Miscellaneous",
    "one": "Numerals",
    "person (human being)": "Persons",
    "rain": "Natural Objects & Phenomena",
    "red": "Colors",
    "road (path)": "Miscellaneous",
    "root": "Plants & Plant Parts",
    "round": "Descriptives",
    "sand": "Natural Objects & Phenomena",
    "say": "Oral Activities",
    "see": "Body Sensations & Activities",
    "seed": "Plants & Plant Parts",
    "sit": "Position & Movement",
    "skin": "Body Parts & Substances",
    "sleep": "Body Sensations & Activities",
    "small": "Size",
    "smoke": "Natural Objects & Phenomena",
    "stand": "Position & Movement",
    "star": "Natural Objects & Phenomena",
    "stone": "Natural Objects & Phenomena",
    "sun": "Natural Objects & Phenomena",
    "swim": "Position & Movement",
    "tail": "Body Parts & Substances",
    "that": "Location & Deixis",
    "this": "Location & Deixis",
    "thou": "Personal Pronouns",
    "tongue": "Body Parts & Substances",
    "tooth": "Body Parts & Substances",
    "tree": "Plants & Plant Parts",
    "two": "Numerals",
    "walk": "Position & Movement",
    "warm (hot)": "Descriptives",
    "water": "Natural Objects & Phenomena",
    "we": "Personal Pronouns",
    "what": "Interrogatives",
    "white": "Colors",
    "who": "Interrogatives",
    "woman": "Persons",
    "yellow": "Colors"
}

# Compile final dataset with split columns
final_rows = []
for word_info in sw100:
    lookup_name = word_info["lookup_name"]
    idx = swadesh_100_to_207.get(lookup_name)
    
    # Dhivehi (Malé)
    dv_terms = dv.get(idx, [])
    # Unique dv_terms to avoid duplicates
    dv_terms = list(dict.fromkeys(dv_terms))
    male_term_latin_list = [transliterate_thaana(t) for t in dv_terms]
    male_term_latin_list = list(dict.fromkeys(male_term_latin_list))
    
    male_term_latin = " / ".join(male_term_latin_list)
    male_term_thaana = " / ".join(dv_terms)
    
    # Addu Dialect
    addu_latin, addu_thaana = get_addu_split(lookup_name, dv_terms) if dv_terms else ("", "")
    
    # Huvadhu Dialect
    huvadhu_latin, huvadhu_thaana = get_huvadhu_split(lookup_name, dv_terms) if dv_terms else ("", "")
    
    # Sinhala (Close Relative) - Transliterated to Latin
    si_terms = si.get(idx, [])
    si_latin_terms = [transliterate_sinhala(t) for t in si_terms]
    si_latin_terms = list(dict.fromkeys(si_latin_terms))
    si_display = " / ".join(si_latin_terms) if si_latin_terms else ""
    
    # Malayalam (Coast Neighbor) - Transliterated to Latin
    ml_terms = ml.get(idx, [])
    ml_latin_terms = [transliterate_malayalam(t) for t in ml_terms]
    ml_latin_terms = list(dict.fromkeys(ml_latin_terms))
    ml_display = " / ".join(ml_latin_terms) if ml_latin_terms else ""
    
    # Arabic - Transliterated to Latin
    ar_terms = ar.get(idx, [])
    ar_latin_terms = [transliterate_arabic(t) for t in ar_terms]
    ar_latin_terms = list(dict.fromkeys(ar_latin_terms))
    ar_display = " / ".join(ar_latin_terms) if ar_latin_terms else ""
    
    # Unique ID prefixed with list identifier (e.g., SW100-001)
    item_id = f"SW100-{int(word_info['number']):03d}"
    word_list = "Swadesh 100"
    category = SWADESH_100_CATEGORIES.get(lookup_name, SWADESH_100_CATEGORIES.get(word_info["english"].lower(), "General"))
    notes = ""
    
    final_rows.append([
        item_id,
        word_list,
        category,
        word_info["english"],
        male_term_latin,
        male_term_thaana,
        addu_latin,
        addu_thaana,
        huvadhu_latin,
        huvadhu_thaana,
        "",  # Fuvahmulah - Latin
        "",  # Fuvahmulah - Thaana
        si_display,
        ml_display,
        ar_display,
        notes
    ])

# Write to CSV
headers = [
    "ID",
    "Word List",
    "Category",
    "English",
    "Male' - Latin",
    "Male' - Thaana",
    "Addu - Latin",
    "Addu - Thaana",
    "Huvadhu - Latin",
    "Huvadhu - Thaana",
    "Fuvahmulah - Latin",
    "Fuvahmulah - Thaana",
    "Sinhala",
    "Malayalam",
    "Arabic",
    "Notes"
]

output_file = os.path.join(PROJECT_ROOT, "dhivehi_language_comparision.csv")
with open(output_file, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(headers)
    writer.writerows(final_rows)

print(f"Dataset successfully compiled and saved to {output_file}")
