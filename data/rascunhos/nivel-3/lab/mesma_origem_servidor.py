# -*- coding: utf-8 -*-
"""Laboratorio 3.4 — servidor de apoio para testar a regra de mesma origem
num navegador real.

Sobe DOIS servidores locais, em portas diferentes (portas diferentes ja
contam como origens diferentes, junto com esquema e host). A porta 8094
serve uma pagina com JavaScript que tenta ler dados da porta 8095 de duas
formas: sem cabecalho CORS e com cabecalho CORS liberando a origem 8094.
So 127.0.0.1 e usado; nenhum host de terceiro e tocado.

Roda com: python mesma_origem_servidor.py
(fica rodando ate Ctrl+C ou o processo ser encerrado por fora)
"""

import http.server
import socketserver
import threading

PORTA_PAGINA = 8094
PORTA_API = 8095

PAGINA = """<html><body>
<h1>Teste de mesma origem</h1>
<script>
async function testar(url, rotulo) {
  try {
    const r = await fetch(url);
    const texto = await r.text();
    console.log(rotulo + ' OK: ' + texto);
  } catch (e) {
    console.log(rotulo + ' BLOQUEADO PELO NAVEGADOR: ' + e.message);
  }
}
</script>
</body></html>"""


class HandlerPagina(http.server.BaseHTTPRequestHandler):
    server_version = "PaginaDemo/1.0"
    sys_version = ""

    def do_GET(self):
        corpo = PAGINA.encode()
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(corpo)

    def log_message(self, *a):
        pass


class HandlerAPI(http.server.BaseHTTPRequestHandler):
    server_version = "APIDemo/1.0"
    sys_version = ""

    def do_GET(self):
        corpo = b'{"dado":"segredo da API"}'
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        if self.path == "/com-cors":
            self.send_header("Access-Control-Allow-Origin", f"http://127.0.0.1:{PORTA_PAGINA}")
        # /sem-cors nao manda cabecalho nenhum de CORS de proposito
        self.end_headers()
        self.wfile.write(corpo)

    def log_message(self, *a):
        pass


def main():
    socketserver.TCPServer.allow_reuse_address = True
    pagina = socketserver.TCPServer(("127.0.0.1", PORTA_PAGINA), HandlerPagina)
    api = socketserver.TCPServer(("127.0.0.1", PORTA_API), HandlerAPI)
    threading.Thread(target=pagina.serve_forever, daemon=True).start()
    threading.Thread(target=api.serve_forever, daemon=True).start()
    print(f"pagina em http://127.0.0.1:{PORTA_PAGINA}/  (origem A)")
    print(f"api    em http://127.0.0.1:{PORTA_API}/     (origem B)")
    print("rodando — Ctrl+C para parar")
    import time
    while True:
        time.sleep(3600)


if __name__ == "__main__":
    main()
