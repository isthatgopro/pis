from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

STATE_FILE = Path(".flaky_count")



class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path != "/flaky.json":
            self.send_response(404)
            self.end_headers()
            return

        count = int(STATE_FILE.read_text()) if STATE_FILE.exists() else 0
        count += 1
        STATE_FILE.write_text(str(count))

        if count <= 2:
            self.send_response(503)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            self.wfile.write(f"temporary failure attempt {count}\n".encode())
            return

        body = b'{"status":"ok","attempt":3}\n'
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_HEAD(self):
        if self.path != "/flaky.json":
            self.send_response(404)
            self.end_headers()
            return

        count = int(STATE_FILE.read_text()) if STATE_FILE.exists() else 0

        if count <= 2:
            self.send_response(503)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            return

        body = b'{"status":"ok","attempt":3}\n'
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()

    def log_message(self, *_args):
        pass


if __name__ == "__main__":
    if STATE_FILE.exists():
        STATE_FILE.unlink()

    HTTPServer(("127.0.0.1", 8000), Handler).serve_forever()