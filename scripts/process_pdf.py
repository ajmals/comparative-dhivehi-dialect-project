import csv
import urllib.request
import os

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
RAW_DIR = os.path.join(PROJECT_ROOT, "data", "raw")

def download_and_convert_list(list_id, filename):
    url = f"https://raw.githubusercontent.com/concepticon/concepticon-data/master/concepticondata/conceptlists/{list_id}.tsv"
    print(f"Downloading {list_id} from Concepticon GitHub...")
    try:
        with urllib.request.urlopen(url) as response:
            content = response.read().decode('utf-8')
            lines = content.splitlines()
            
            # Read TSV
            reader = csv.reader(lines, delimiter='\t')
            rows = list(reader)
            
            if not rows:
                print(f"No data found for {list_id}")
                return
            
            # Write CSV
            filepath = os.path.join(RAW_DIR, filename)
            with open(filepath, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerows(rows)
            
            print(f"Successfully wrote {len(rows)-1} items to {filepath}")
    except Exception as e:
        print(f"Error downloading/saving {list_id}: {e}")

if __name__ == "__main__":
    # Download and save the 100-item list
    download_and_convert_list("Swadesh-1955-100", "swadesh_1955_100.csv")
    
    # Download and save the 215-item list
    download_and_convert_list("Swadesh-1955-215", "swadesh_1955_215.csv")
