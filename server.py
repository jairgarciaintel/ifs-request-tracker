"""
IFS Request Tracker — Local Server
===================================
Sirve la landing page y permite guardar tracking.json desde el browser.

Uso:
    python server.py

    Abre http://localhost:8080 en el browser.
    Jenn y tú pueden acceder si están en la misma red o si lo pones en el servidor.

Para que ambos (Jenn y tú) compartan el mismo tracking.json,
corran este server en la máquina compartida (el data server).
"""

import http.server
import json
import os
from pathlib import Path

PORT = 8080
DIRECTORY = Path(__file__).parent


class TrackerHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(DIRECTORY), **kwargs)
    
    def do_PUT(self):
        """Handle PUT requests to save tracking.json and tracking.xlsx"""
        if self.path in ('/data/tracking.json', '/data/tracking.xlsx'):
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length)
            
            target = DIRECTORY / self.path.lstrip('/')
            target.parent.mkdir(parents=True, exist_ok=True)
            
            if self.path.endswith('.json'):
                # Validate JSON
                try:
                    data = json.loads(body)
                    target.write_text(json.dumps(data, indent=2))
                except json.JSONDecodeError:
                    self.send_response(400)
                    self.end_headers()
                    self.wfile.write(b'Invalid JSON')
                    return
            else:
                # Binary (xlsx)
                target.write_bytes(body)
            
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(b'{"saved": true}')
            ext = 'JSON' if self.path.endswith('.json') else 'Excel'
            print(f"  saved {ext} -> {target.name}")
        else:
            self.send_response(404)
            self.end_headers()
    
    def end_headers(self):
        # CORS headers for local development
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, PUT, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()


def main():
    print("=" * 50)
    print("IFS Request Tracker — Local Server")
    print("=" * 50)
    print(f"\n  🌐 http://localhost:{PORT}")
    print(f"  📁 Serving: {DIRECTORY}")
    print(f"\n  Tracking saves to: data/tracking.json")
    print(f"  Both Jenn and Jair see the same data.\n")
    print("  Press Ctrl+C to stop.\n")
    
    server = http.server.HTTPServer(('0.0.0.0', PORT), TrackerHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n\n  Server stopped.")
        server.shutdown()


if __name__ == '__main__':
    main()
