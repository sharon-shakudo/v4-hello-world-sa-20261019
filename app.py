#!/usr/bin/env python3
"""Minimal zero-dependency Hello World HTTP server for the Shakudo V4
Git Repository -> Microservice integration test."""
import json
import os
import socket
import subprocess
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

PORT = int(os.environ.get("PORT", "8787"))
HOST = os.environ.get("HOST", "0.0.0.0")
APP_VERSION = "1.0.0"
BUILD_MARKER = os.environ.get("BUILD_MARKER", "v4-integration-test")
HEADING = os.environ.get("HEADING", "Hello World")


def revision():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], stderr=subprocess.DEVNULL
        ).decode().strip()
    except Exception:
        return os.environ.get("GIT_REVISION", "unknown")


PAGE = """<!doctype html>
<html lang="en">
<head><meta charset="utf-8"><title>Shakudo V4 Hello World</title></head>
<body>
  <h1 id="hello-heading">{heading}</h1>
  <p>Served by a Shakudo V4 microservice.</p>
</body>
</html>
""".format(heading=HEADING)


class Handler(BaseHTTPRequestHandler):
    def _send(self, code, ctype, body):
        data = body.encode()
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        if self.path in ("/", "/index.html"):
            self._send(200, "text/html; charset=utf-8", PAGE)
        elif self.path == "/healthz":
            self._send(200, "application/json", json.dumps({"status": "ok"}))
        elif self.path == "/version":
            self._send(200, "application/json", json.dumps({
                "app_version": APP_VERSION,
                "build_marker": BUILD_MARKER,
                "revision": revision(),
                "host": socket.gethostname(),
            }))
        else:
            self._send(404, "text/plain; charset=utf-8", "not found")

    def log_message(self, fmt, *args):
        print("%s - %s" % (self.address_string(), fmt % args), flush=True)


if __name__ == "__main__":
    print("starting on %s:%d" % (HOST, PORT), flush=True)
    ThreadingHTTPServer((HOST, PORT), Handler).serve_forever()
