#!/usr/bin/env python3
"""
Celine's Game Land — combined game server (port 8765)
  /                  → hub
  /food-bowl-rush/*  → food-bowl-rush game
  /math-bond-star/*  → math-bond-star game
  /api/scores        → shared score store (food-bowl-rush/scores.json)
"""
import json, threading, webbrowser, mimetypes
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path

PORT        = 8765
PROJECTS    = Path(__file__).parent.parent       # .../projects/
HUB_DIR     = Path(__file__).parent              # .../celinegameland/
SCORES_FILE = PROJECTS / 'food-bowl-rush' / 'scores.json'

GAMES = {
    '/food-bowl-rush': PROJECTS / 'food-bowl-rush',
    '/math-bond-star':  PROJECTS / 'math-bond-star',
}

def load_scores():
    try:    return json.loads(SCORES_FILE.read_text())
    except: return {}

def save_scores(data):
    SCORES_FILE.write_text(json.dumps(data, indent=2))


class Handler(BaseHTTPRequestHandler):

    def do_OPTIONS(self):
        self.send_response(200); self._cors(); self.end_headers()

    def do_GET(self):
        path = self.path.split('?')[0]
        if path == '/api/scores':
            return self._json(200, load_scores())
        if path in ('/', '', '/index.html'):
            return self._file(HUB_DIR / 'index.html')
        for prefix, d in GAMES.items():
            if path == prefix or path.startswith(prefix + '/'):
                rel = path[len(prefix):].lstrip('/') or 'index.html'
                return self._file(d / rel)
        self.send_error(404)

    def do_POST(self):
        if self.path == '/api/scores':
            n = int(self.headers.get('Content-Length', 0))
            save_scores(json.loads(self.rfile.read(n)))
            self._json(200, {'ok': True})

    def do_DELETE(self):
        if self.path == '/api/scores':
            save_scores({})
            self._json(200, {'ok': True})

    def _file(self, p):
        p = Path(p)
        if not p.exists(): return self.send_error(404)
        mime = mimetypes.guess_type(str(p))[0] or 'application/octet-stream'
        data = p.read_bytes()
        self.send_response(200)
        self.send_header('Content-Type', mime)
        self.send_header('Content-Length', len(data))
        self._cors(); self.end_headers(); self.wfile.write(data)

    def _json(self, code, data):
        payload = json.dumps(data).encode()
        self.send_response(code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', len(payload))
        self._cors(); self.end_headers(); self.wfile.write(payload)

    def _cors(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')

    def log_message(self, *a): pass


def main():
    httpd = HTTPServer(('localhost', PORT), Handler)
    url   = f'http://localhost:{PORT}'
    print(f'\n  🎮  Celine\'s Game Land is running!')
    print(f'  🌐  {url}')
    print(f'  Press Ctrl+C to stop.\n')
    threading.Timer(0.8, lambda: webbrowser.open(url)).start()
    try:    httpd.serve_forever()
    except KeyboardInterrupt: print('\n  👋  Bye!')

if __name__ == '__main__':
    main()
