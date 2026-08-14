import fitz
import re
import csv
import json
import os
import pandas as pd

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
PDF_PATH = os.path.join(PROJECT_ROOT, "data", "references", "Fritz_Sonja_2002_The_Dhivehi_Language_A_Descriptive_and_Historical.pdf")

DIALECT_MAP = {
    "M": "Male",
    "A": "Addu",
    "F": "Fua Mulaku"
}

def parse_pdf_pages(start_pdf_page, end_pdf_page):
    """
    Parses PDF pages from start_pdf_page to end_pdf_page (1-indexed).
    Extracts structured word mappings for Dhivehi short story T1.
    """
    doc = fitz.open(PDF_PATH)
    all_words = []
    
    for page_num in range(start_pdf_page - 1, end_pdf_page):
        page = doc[page_num]
        pdf_page_str = page_num + 1
        
        # Get raw layout blocks
        dict_page = page.get_text("dict")
        blocks = dict_page["blocks"]
        
        # Extract text lines with positions
        lines_pos = []
        for b in blocks:
            if "lines" in b:
                for l in b["lines"]:
                    text = "".join([s["text"] for s in l["spans"]]).strip()
                    if text:
                        bbox = l["bbox"]
                        lines_pos.append({
                            "text": text,
                            "x0": bbox[0],
                            "y0": bbox[1],
                            "x1": bbox[2],
                            "y1": bbox[3],
                            "spans": l["spans"]
                        })
        
        # Sort lines vertically by y0, then x0
        lines_pos.sort(key=lambda item: (item["y0"], item["x0"]))
        
        # Determine book page number from header
        book_page = None
        for l in lines_pos[:5]:
            m = re.match(r"^(\d+)\b", l["text"])
            if m:
                book_page = int(m.group(1))
                break
        if not book_page:
            book_page = pdf_page_str - 4  # Fallback approximation
            
    doc.close()
    return lines_pos

print("Script framework ready.")
