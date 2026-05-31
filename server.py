#!/usr/bin/env python3
"""Simple proxy server for Norney Farm dashboard."""

import http.server
import urllib.request
import urllib.error
import base64
import json
import os

# Load .env file if present
_env = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.env')
if os.path.exists(_env):
    for _line in open(_env):
        _line = _line.strip()
        if _line and not _line.startswith('#') and '=' in _line:
            _k, _v = _line.split('=', 1)
            os.environ.setdefault(_k.strip(), _v.strip())

VICTRON_KEY  = os.environ.get("VICTRON_KEY", "")
OCTOPUS_KEY  = os.environ.get("OCTOPUS_KEY", "")
VRM_BASE     = "https://vrmapi.victronenergy.com/v2"
OCTOPUS_BASE = "https://api.octopus.energy/v1"
PORT         = 3456
STATIC_DIR   = os.path.dirname(os.path.abspath(__file__))

_octopus_auth = base64.b64encode(f"{OCTOPUS_KEY}:".encode()).decode()


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=STATIC_DIR, **kwargs)

    def do_GET(self):
        if self.path.startswith("/api/"):
            self._proxy_victron(self.path[5:])
        elif self.path.startswith("/octopus/"):
            self._proxy_octopus(self.path[9:])
        else:
            super().do_GET()

    def _proxy_victron(self, path):
        self._proxy(f"{VRM_BASE}/{path}", {
            "x-authorization": f"Token {VICTRON_KEY}",
            "Content-Type": "application/json",
        })

    def _proxy_octopus(self, path):
        self._proxy(f"{OCTOPUS_BASE}/{path}", {
            "Authorization": f"Basic {_octopus_auth}",
            "Content-Type": "application/json",
        })

    def _proxy(self, url, headers):
        req = urllib.request.Request(url, headers=headers)
        try:
            with urllib.request.urlopen(req, timeout=15) as resp:
                body = resp.read()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(body)
        except urllib.error.HTTPError as e:
            body = e.read()
            self.send_response(e.code)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(body)
        except Exception as e:
            self.send_response(502)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode())

    def log_message(self, fmt, *args):
        pass


if __name__ == "__main__":
    with http.server.ThreadingHTTPServer(("", PORT), Handler) as httpd:
        print(f"Norney Farm server running at http://localhost:{PORT}")
        httpd.serve_forever()
