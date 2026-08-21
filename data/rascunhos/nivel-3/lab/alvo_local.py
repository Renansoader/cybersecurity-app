"""Alvo proposital em localhost: HTTP com algumas rotas e um banner TCP simples.

Roda so em 127.0.0.1. Serve de alvo para os laboratorios de varredura e
enumeracao — nenhum host de terceiro e tocado em momento algum.
"""
import http.server, socket, socketserver, threading, time

ROTAS = {
    "/": (200, "<html><title>Portal interno</title><h1>Portal interno</h1></html>"),
    "/index.html": (200, "<html><title>Portal interno</title></html>"),
    "/admin": (401, "<html><h1>401 Unauthorized</h1></html>"),
    "/backup": (403, "<html><h1>403 Forbidden</h1></html>"),
    "/api/status": (200, '{"servico":"portal","versao":"1.4.2"}'),
    "/.git/config": (200, "[core]\n\trepositoryformatversion = 0\n"),
}

class Handler(http.server.BaseHTTPRequestHandler):
    server_version = "PortalInterno/1.4.2"
    sys_version = ""

    def do_GET(self):
        codigo, corpo = ROTAS.get(self.path, (404, "<html><h1>404 Not Found</h1></html>"))
        dados = corpo.encode()
        self.send_response(codigo)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(dados)))
        self.send_header("X-Powered-By", "PortalInterno")
        self.end_headers()
        self.wfile.write(dados)

    def log_message(self, *args):
        pass

def banner_tcp(porta):
    """Servico de texto que se apresenta ao conectar, como SMTP ou FTP fazem."""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(("127.0.0.1", porta))
    s.listen(5)
    while True:
        con, _ = s.accept()
        con.sendall(b"220 mail.interno.local ESMTP PortalMTA 3.8.1 pronto\r\n")
        time.sleep(0.2)
        con.close()

if __name__ == "__main__":
    socketserver.TCPServer.allow_reuse_address = True
    web = socketserver.TCPServer(("127.0.0.1", 8080), Handler)
    threading.Thread(target=web.serve_forever, daemon=True).start()
    threading.Thread(target=banner_tcp, args=(2525,), daemon=True).start()
    print("alvo local em 127.0.0.1:8080 (HTTP) e 127.0.0.1:2525 (banner)")
    time.sleep(300)
