#!/usr/bin/env python3
"""
Downloads high-quality public domain / Creative Commons images from Wikimedia / Wikipedia
for the Dhivehi dialect comparison prompt words.
Saves them locally with the English word as the filename.
"""

import csv
import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request

DEST_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "assets", "images", "prompts"))
os.makedirs(DEST_DIR, exist_ok=True)

CSV_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "dhivehi_language_comparision.csv"))

# Disambiguation / clean subject mappings for Wikipedia PageImages API
MAPPINGS = {
    'all': 'Whole',
    'ashes': 'Ash',
    'bark': 'Bark (botany)',
    'belly': 'Abdomen',
    'big': 'Elephant',  # Elephant is standard visual icon for "big" in child/linguistic surveys
    'bird': 'Bird',
    'bite': 'Animal bite',
    'black': 'Black',
    'blood': 'Blood',
    'bone': 'Bone',
    'burn': 'Combustion',
    'claw': 'Claw',
    'cloud': 'Cumulus cloud',
    'cold': 'Frost',
    'come': 'Walking',
    'die': 'Skull and crossbones',
    'dog': 'Dog',
    'drink': 'Drinking',
    'dry': 'Desertification',
    'ear': 'Ear',
    'earth': 'Earth',
    'eat': 'Eating',
    'egg': 'Egg as food',
    'eye': 'Human eye',
    'fat (grease)': 'Adipose tissue',
    'feather': 'Feather',
    'fire': 'Campfire',
    'fish': 'Fish',
    'fly': 'Bird flight',
    'foot': 'Foot',
    'full': 'Glass of water',
    'give': 'Gift',
    'good': 'Thumb signal',
    'green': 'Green',
    'hair': 'Human hair',
    'hand': 'Hand',
    'head': 'Human head',
    'hear': 'Hearing',
    'heart': 'Heart',
    'horn': 'Horn (anatomy)',
    'I': 'Pointing',
    'kill': 'Predation',
    'knee': 'Knee',
    'know': 'Thought',
    'leaf': 'Leaf',
    'lie': 'Lying (position)',
    'liver': 'Liver',
    'long': 'Ruler',
    'louse': 'Head louse',
    'man': 'Man',
    'many': 'Crowd',
    'meat (flesh)': 'Meat',
    'moon': 'Full moon',
    'mountain': 'Mountain',
    'mouth': 'Mouth',
    'name': 'Name tag',
    'neck': 'Neck',
    'new': 'Gift',
    'night': 'Night',
    'nose': 'Human nose',
    'not': 'No symbol',
    'one': '1',
    'person': 'Human',
    'rain': 'Rain',
    'red': 'Red',
    'road': 'Road',
    'root': 'Root',
    'round': 'Sphere',
    'sand': 'Sand',
    'say': 'Speech balloon',
    'see': 'Visual perception',
    'seed': 'Seed',
    'sit': 'Sitting',
    'skin': 'Human skin',
    'sleep': 'Sleep',
    'small': 'Ladybug',  # clean recognizable small visual icon
    'smoke': 'Smoke',
    'stand': 'Standing',
    'star': 'Star',
    'stone': 'Rock (geology)',
    'sun': 'Sun',
    'swim': 'Swimming',
    'tail': 'Tail',
    'that': 'Index finger',
    'this': 'Pointing',
    'thou': 'Pointing',
    'tongue': 'Tongue',
    'tooth': 'Tooth',
    'tree': 'Tree',
    'two': '2',
    'walk': 'Walking',
    'warm (hot)': 'Campfire',
    'water': 'Glass of water',
    'we': 'Teamwork',
    'what': 'Question mark',
    'white': 'White',
    'who': 'Question mark',
    'woman': 'Woman',
    'yellow': 'Yellow'
}

HEADERS = {
    'User-Agent': 'DhivehiDialectVisualElicitation/1.0 (academic-research@dhivehi-dialect.org)'
}

def clean_filename(name):
    # sanitize english word for filesystem: "fat (grease)" -> "fat_grease"
    name = name.strip().lower()
    name = re.sub(r'[^\w\s-]', '', name)
    name = re.sub(r'[\s]+', '_', name)
    return name

def fetch_wiki_image(title):
    url = f"https://en.wikipedia.org/w/api.php?action=query&titles={urllib.parse.quote(title)}&prop=pageimages&format=json&pithumbsize=600"
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=8) as resp:
            data = json.loads(resp.read().decode())
            pages = data.get('query', {}).get('pages', {})
            for p in pages.values():
                if 'thumbnail' in p and 'source' in p['thumbnail']:
                    return p['thumbnail']['source']
    except Exception as e:
        pass
    return None

def fetch_commons_search(query):
    url = f"https://commons.wikimedia.org/w/api.php?action=query&generator=search&gsrsearch={urllib.parse.quote(query)}&gsrnamespace=6&gsrlimit=1&prop=imageinfo&iiprop=url&iiurlwidth=600&format=json"
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=8) as resp:
            data = json.loads(resp.read().decode())
            pages = data.get('query', {}).get('pages', {})
            for p in pages.values():
                if 'imageinfo' in p and len(p['imageinfo']) > 0:
                    info = p['imageinfo'][0]
                    return info.get('thumburl') or info.get('url')
    except Exception as e:
        pass
    return None

def main():
    with open(CSV_FILE, 'r', encoding='utf-8') as f:
        rows = list(csv.DictReader(f))

    print(f"Total concepts to process: {len(rows)}")
    results = []
    success_count = 0

    for idx, row in enumerate(rows, 1):
        eng = row['English'].strip()
        fname_base = clean_filename(eng)
        wiki_title = MAPPINGS.get(eng, eng)

        # 1. Try Wikipedia page lead image
        img_url = fetch_wiki_image(wiki_title)

        # 2. Fallback to Commons search if needed
        if not img_url:
            img_url = fetch_commons_search(f"{eng} photo")

        if not img_url:
            img_url = fetch_commons_search(eng)

        ext = "jpg"
        if img_url:
            parsed = urllib.parse.urlparse(img_url)
            path_part = parsed.path.lower()
            if path_part.endswith(".png"):
                ext = "png"
            elif path_part.endswith(".svg.png") or path_part.endswith(".svg"):
                ext = "png"
            elif path_part.endswith(".webp"):
                ext = "webp"

        filename = f"{fname_base}.{ext}"
        filepath = os.path.join(DEST_DIR, filename)

        status = "FAIL"
        file_size = 0

        if img_url:
            try:
                img_req = urllib.request.Request(img_url, headers=HEADERS)
                with urllib.request.urlopen(img_req, timeout=12) as img_resp:
                    content = img_resp.read()
                    with open(filepath, 'wb') as out_f:
                        out_f.write(content)
                    file_size = len(content)
                    status = "OK"
                    success_count += 1
            except Exception as e:
                status = f"ERR: {e}"

        results.append({
            'id': row['ID'],
            'english': eng,
            'category': row['Category'],
            'male_thaana': row['Male\' - Thaana'],
            'male_latin': row['Male\' - Latin'],
            'filename': filename,
            'filepath': filepath,
            'file_size': file_size,
            'img_url': img_url,
            'status': status
        })

        print(f"[{idx:02d}/{len(rows)}] {eng:<15} -> {filename} ({file_size/1024:.1f} KB) [{status}]")
        time.sleep(0.15)  # Respectful rate limiting for Wikimedia servers

    print(f"\nCompleted: {success_count}/{len(rows)} successfully downloaded.")

    # Write HTML Gallery for Visual Inspection
    gallery_html_path = os.path.join(DEST_DIR, "index.html")
    with open(gallery_html_path, 'w', encoding='utf-8') as gf:
        gf.write("""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Visual Prompt Gallery - 100 Dialect Concepts</title>
<style>
  :root {
    --bg: #0b0f19;
    --card: #151d2f;
    --border: #23314d;
    --text: #f0f4fc;
    --sub: #94a3b8;
    --accent: #38bdf8;
    --thaana: #34d399;
  }
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    background: var(--bg);
    color: var(--text);
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    padding: 30px 20px;
  }
  header {
    max-width: 1400px;
    margin: 0 auto 30px auto;
    text-align: center;
  }
  h1 { font-size: 2rem; margin-bottom: 8px; color: #fff; }
  p.desc { color: var(--sub); font-size: 1rem; max-width: 700px; margin: 0 auto 20px; }
  .stats-bar {
    display: inline-flex;
    gap: 20px;
    background: var(--card);
    padding: 10px 24px;
    border-radius: 999px;
    border: 1px solid var(--border);
    font-size: 0.9rem;
  }
  .stats-bar span { color: var(--accent); font-weight: 600; }
  .grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
    gap: 20px;
    max-width: 1400px;
    margin: 0 auto;
  }
  .card {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 14px;
    overflow: hidden;
    display: flex;
    flex-direction: column;
    transition: transform 0.2s, border-color 0.2s;
  }
  .card:hover {
    transform: translateY(-4px);
    border-color: var(--accent);
  }
  .img-wrap {
    width: 100%;
    aspect-ratio: 1 / 1;
    background: #060911;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;
  }
  .img-wrap img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    display: block;
  }
  .card-body {
    padding: 14px;
    display: flex;
    flex-direction: column;
    gap: 4px;
  }
  .cat {
    font-size: 0.72rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: var(--accent);
  }
  .eng-title {
    font-size: 1.1rem;
    font-weight: 700;
    color: #fff;
    text-transform: capitalize;
  }
  .dhivehi {
    font-size: 1.25rem;
    color: var(--thaana);
    font-family: 'MV Fohiru', 'Faruma', 'Kaff', sans-serif;
    direction: rtl;
    text-align: right;
    margin-top: 2px;
  }
  .meta {
    font-size: 0.78rem;
    color: var(--sub);
    margin-top: 6px;
    border-top: 1px solid var(--border);
    padding-top: 6px;
    display: flex;
    justify-content: space-between;
  }
</style>
</head>
<body>
<header>
  <h1>📸 Dialect Visual Prompt Gallery</h1>
  <p class="desc">100 Public Domain / Creative Commons image references fetched for the Dhivehi dialect comparison dataset. Review image clarity, relevance, and visual quality below.</p>
  <div class="stats-bar">
    <div>Total Concepts: <span>""" + str(len(rows)) + """</span></div>
    <div>Successfully Downloaded: <span>""" + str(success_count) + """</span></div>
    <div>License: <span>Public Domain & CC</span></div>
  </div>
</header>

<main class="grid">
""")
        for item in results:
            size_kb = f"{item['file_size']/1024:.0f} KB" if item['file_size'] > 0 else "0 KB"
            gf.write(f"""  <div class="card">
    <div class="img-wrap">
      <img src="{item['filename']}" alt="{item['english']}" loading="lazy" onerror="this.parentElement.innerHTML='<div style=\\'padding:20px;color:#ef4444;text-align:center\\'>Image Not Found</div>'">
    </div>
    <div class="card-body">
      <div class="cat">{item['category']}</div>
      <div class="eng-title">{item['english']}</div>
      <div class="dhivehi">{item['male_thaana']}</div>
      <div class="meta">
        <span>{item['filename']}</span>
        <span>{size_kb}</span>
      </div>
    </div>
  </div>\n""")

        gf.write("""</main>
</body>
</html>
""")
    print(f"Gallery created at: {gallery_html_path}")

if __name__ == '__main__':
    main()
