#!/usr/bin/env python3
"""
Lightweight local curation server for Dhivehi dialect visual prompt images.
Serves the curator web app and handles:
- Instant image replacement from Wikimedia Commons URLs directly to disk
- Local file upload replacement
- State persistence (curation_state.json)
"""

import http.server
import json
import os
import re
import socketserver
import sys
import urllib.parse
import urllib.request

PORT = 8085
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
PROMPTS_DIR = os.path.join(BASE_DIR, "assets", "images", "prompts")
STATE_FILE = os.path.join(PROMPTS_DIR, "curation_state.json")

HEADERS = {
    'User-Agent': 'DhivehiDialectCurator/1.0 (dialect-research@dhivehi-project.org)'
}

class CuratorHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=BASE_DIR, **kwargs)

    def end_headers(self):
        # Enable CORS and disable aggressive caching for live image editing
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    def do_HEAD(self):
        self.do_GET()

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path == '/' or parsed.path == '/curator':
            self.send_response(302)
            self.send_header('Location', '/assets/images/prompts/index.html')
            self.end_headers()
            return
        elif parsed.path == '/api/get-state':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            if os.path.exists(STATE_FILE):
                with open(STATE_FILE, 'r', encoding='utf-8') as f:
                    self.wfile.write(f.read().encode('utf-8'))
            else:
                self.wfile.write(json.dumps({}).encode('utf-8'))
            return
        super().do_GET()

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(length) if length > 0 else b'{}'

        if parsed.path == '/api/save-state':
            try:
                data = json.loads(body.decode('utf-8'))
                with open(STATE_FILE, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"success": True}).encode('utf-8'))
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode('utf-8'))
            return

        elif parsed.path == '/api/replace-image':
            try:
                data = json.loads(body.decode('utf-8'))
                filename = data.get('filename')
                image_url = data.get('imageUrl')

                if not filename or not image_url:
                    raise ValueError("Missing filename or imageUrl")

                # Sanitize target path
                filename = os.path.basename(filename)
                target_path = os.path.join(PROMPTS_DIR, filename)

                req = urllib.request.Request(image_url, headers=HEADERS)
                with urllib.request.urlopen(req, timeout=15) as resp:
                    img_bytes = resp.read()

                with open(target_path, 'wb') as f:
                    f.write(img_bytes)

                file_size = len(img_bytes)

                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({
                    "success": True,
                    "filename": filename,
                    "fileSize": file_size,
                    "message": f"Successfully replaced {filename} ({file_size/1024:.1f} KB)"
                }).encode('utf-8'))
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode('utf-8'))
            return

        elif parsed.path == '/api/upload-image':
            try:
                data = json.loads(body.decode('utf-8'))
                filename = os.path.basename(data.get('filename', ''))
                base64_data = data.get('base64Data', '')

                if not filename or not base64_data:
                    raise ValueError("Missing filename or base64Data")

                import base64
                if ',' in base64_data:
                    base64_data = base64_data.split(',', 1)[1]

                img_bytes = base64.b64decode(base64_data)
                target_path = os.path.join(PROMPTS_DIR, filename)

                with open(target_path, 'wb') as f:
                    f.write(img_bytes)

                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({
                    "success": True,
                    "filename": filename,
                    "fileSize": len(img_bytes)
                }).encode('utf-8'))
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode('utf-8'))
            return

        self.send_response(404)
        self.end_headers()

def run():
    port = PORT
    # Try preferred port, or increment if busy
    for p in range(PORT, PORT + 20):
        try:
            with socketserver.TCPServer(("", p), CuratorHandler) as httpd:
                print(f"🚀 Curator server active on: http://localhost:{p}")
                print(f"📂 Prompts directory: {PROMPTS_DIR}")
                print("Press Ctrl+C to stop.")
                httpd.serve_forever()
                break
        except OSError:
            continue

if __name__ == '__main__':
    run()
