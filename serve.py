#!/usr/bin/env python3
"""Simple dev server for the site + contact form endpoint.

Static files: served from ./public
Endpoint: POST /contact  (JSON body) -> returns { ok:true, simulated:true }

If you later add SMTP credentials, you can extend send_mail().
"""
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from email.message import EmailMessage
import os, sys, json, datetime, ssl, smtplib
from urllib.parse import urlparse, unquote

ROOT = os.path.abspath(os.path.dirname(__file__))
PUBLIC = os.path.join(ROOT, 'public')

REQUIRED_FIELDS = ['name','email','message']

def try_send_email(payload: dict) -> bool:
    """Attempt real email if ENV vars set, else simulate.
    Returns True if real email sent, False if simulated."""
    host = os.getenv('SMTP_HOST'); user = os.getenv('SMTP_USER'); pwd = os.getenv('SMTP_PASS')
    to_addr = os.getenv('MAIL_TO','jolaupo@gmail.com')
    body_lines = []
    for k in ['name','email','phone','companyType','companyTypeOther','urgency','preference','reason','reasonOther','message']:
        if payload.get(k):
            body_lines.append(f"{k}: {payload[k]}")
    body = '\n'.join(body_lines)
    if not (host and user and pwd):
        # Simulation mode: log to file
        log_path = os.path.join(ROOT, 'contact_submissions.log')
        with open(log_path,'a',encoding='utf-8') as f:
            f.write(f"\n--- {datetime.datetime.utcnow().isoformat()}Z (SIMULATED) ---\n{body}\n")
        return False
    msg = EmailMessage()
    msg['Subject'] = f"Nouveau message site – {payload.get('name','(inconnu)')}"
    msg['From'] = user
    msg['To'] = to_addr
    msg.set_content(body)
    with smtplib.SMTP(host, int(os.getenv('SMTP_PORT','587'))) as s:
        s.starttls(context=ssl.create_default_context())
        s.login(user, pwd)
        s.send_message(msg)
    return True

class Handler(SimpleHTTPRequestHandler):
    server_version = "JLPStatic/1.0"

    def translate_path(self, path):
        # Serve everything from PUBLIC; fallback to index.html
        # Decode %20 etc. so files with spaces work
        path = unquote(path)
        rel = path.lstrip('/') or 'index.html'
        target = os.path.join(PUBLIC, rel)
        if os.path.isdir(target):
            # serve directory index if exists else index.html inside
            index = os.path.join(target,'index.html')
            return index if os.path.exists(index) else target
        if os.path.exists(target):
            return target
        # fallback SPA style to index
        return os.path.join(PUBLIC, 'index.html')

    def log_message(self, fmt, *args):
        ts = datetime.datetime.now().strftime('%H:%M:%S')
        sys.stderr.write(f"[{ts}] {self.client_address[0]} {self.command} {self.path} -> " + fmt%args + "\n")

    def do_OPTIONS(self):
        if self.path == '/contact':
            self.send_response(204)
            self.send_header('Access-Control-Allow-Origin','*')
            self.send_header('Access-Control-Allow-Headers','Content-Type')
            self.send_header('Access-Control-Allow-Methods','POST, OPTIONS')
            self.end_headers()
        else:
            super().do_OPTIONS()

    def do_GET(self):
        if self.path == '/contact':
            self.send_response(405, 'Method Not Allowed')
            self.send_header('Content-Type','application/json; charset=utf-8')
            self.send_header('Allow','POST, OPTIONS')
            self.end_headers()
            self.wfile.write(b'{"error":"method_not_allowed","allow":"POST"}')
            return
        return super().do_GET()

    def do_POST(self):
        parsed = urlparse(self.path)
        if parsed.path != '/contact':
            self.send_error(404, 'Not Found')
            return
        try:
            length = int(self.headers.get('Content-Length','0'))
            raw = self.rfile.read(length)
            data = json.loads(raw or b'{}')
        except Exception:
            return self._json({'ok':False,'error':'invalid_json'}, 400)
        missing = [f for f in REQUIRED_FIELDS if not data.get(f)]
        if missing:
            return self._json({'ok':False,'error':'missing_fields','fields':missing}, 422)
        try:
            real = try_send_email(data)
        except Exception as e:
            return self._json({'ok':False,'error':'send_failed','detail':str(e)}, 500)
        return self._json({'ok':True,'simulated': (not real)})

    def _json(self, obj, status=200):
        enc = json.dumps(obj).encode('utf-8')
        self.send_response(status)
        self.send_header('Content-Type','application/json; charset=utf-8')
        self.send_header('Content-Length', str(len(enc)))
        self.send_header('Access-Control-Allow-Origin','*')
        self.end_headers()
        self.wfile.write(enc)

def run():
    port = int(os.getenv('PORT','8000'))
    # CLI override: python3 serve.py 8070
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            pass
    server = ThreadingHTTPServer(('0.0.0.0', port), Handler)
    print(f"Serving site on http://localhost:{port}  (CTRL+C to quit)")
    print("Ouvrez cette URL exacte dans le navigateur pour que fetch('/contact') fonctionne.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print('\nShutdown requested.')

if __name__ == '__main__':
    run()
