"""Serve only the generated public site on loopback. No uploads or accounts."""
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import mimetypes
from pathlib import Path
import sys
from urllib.parse import urlsplit, unquote

ROOT = Path(__file__).resolve().parent/'site'
PREFIX = '/gratis-workflows/'


class Handler(BaseHTTPRequestHandler):
    def do_GET(self): self.respond(False)
    def do_HEAD(self): self.respond(True)
    def log_message(self,*args): pass
    def respond(self,head):
        port=self.server.server_address[1]
        if self.headers.get('Host') not in {f'127.0.0.1:{port}',f'localhost:{port}'}:
            self.send_error(421);return
        route=unquote(urlsplit(self.path).path)
        if route in {'/',PREFIX.rstrip('/')}:
            self.send_response(302);self.send_header('Location',PREFIX);self.end_headers();return
        files={PREFIX+p.relative_to(ROOT).as_posix():p for p in ROOT.rglob('*') if p.is_file()}
        for key,path in list(files.items()):
            if key.endswith('/index.html'):files[key.removesuffix('index.html')]=path
        path=files.get(route)
        if path is None:self.send_error(404);return
        body=path.read_bytes()
        mime={'.js':'text/javascript','.css':'text/css','.woff2':'font/woff2'}.get(path.suffix,mimetypes.guess_type(path.name)[0] or 'application/octet-stream')
        self.send_response(200)
        for key,value in [('Content-Type',mime),('Content-Length',str(len(body))),('X-Content-Type-Options','nosniff'),('X-Robots-Tag','noindex, nofollow'),('Cache-Control','no-store'),('Referrer-Policy','strict-origin-when-cross-origin'),('Content-Security-Policy',"default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self'; font-src 'self'; connect-src 'self'; object-src 'none'; base-uri 'none'; frame-ancestors 'none'")]:self.send_header(key,value)
        self.end_headers()
        if not head:self.wfile.write(body)


if __name__=='__main__':
    port=int(sys.argv[1]) if len(sys.argv)>1 else 8772
    with ThreadingHTTPServer(('127.0.0.1',port),Handler) as server:
        print(f'http://127.0.0.1:{server.server_address[1]}{PREFIX}',flush=True)
        server.serve_forever()
