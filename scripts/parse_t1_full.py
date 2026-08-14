import fitz
import re
import csv
import json
import os
import pandas as pd

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
PDF_PATH = os.path.join(PROJECT_ROOT, "data", "references", "Fritz_Sonja_2002_The_Dhivehi_Language_A_Descriptive_and_Historical.pdf")

DIALECT_MAP = {
    "M": "Male'",
    "A": "Addu",
    "F": "Fua Mulaku"
}

def extract_story_t1(max_pdf_page=16):
    doc = fitz.open(PDF_PATH)
    all_rows = []
    
    # Story T1 starts on PDF Page 6 (Book Page 2)
    for p_idx in range(5, max_pdf_page):
        page = doc[p_idx]
        pdf_page_num = p_idx + 1
        
        # Get blocks
        blocks = page.get_text("blocks")
        lines = []
        for b in blocks:
            text = b[4].strip()
            if text:
                lines.extend(text.split("\n"))
                
        # Derive book page from header line if present
        book_page = pdf_page_num - 4
        if lines and lines[0].isdigit():
            book_page = int(lines[0])
            
        print(f"Parsing PDF Page {pdf_page_num} (Book Page {book_page})...")
        
    doc.close()
    return True

if __name__ == "__main__":
    extract_story_t1(16)
