# -*- coding: utf-8 -*-
"""Laboratorio 3.4 — a decisao de autorizacao precisa acontecer no servidor,
nao na tela que o esconde.

Sobe um servidor HTTP real em 127.0.0.1, so para esta execucao. A pagina
esconde o botao "excluir usuario" via CSS quando o papel nao e admin — mas
o endpoint /excluir continua respondendo a qualquer requisicao HTTP direta,
porque o servidor nunca checa o papel de quem pediu. Nenhum host de
terceiro e tocado; o servidor derruba sozinho ao final do script.

Roda com: python decisao_no_servidor.py
"""

import http.server
import socketserver
import threading
import time
import urllib.request

PORTA = 8091

PAGINA = """<html><body>
<h1>Painel</h1>
<button style="display:none">Excluir usuario 42</button>
<p>(o botao so aparece via JS se papel==admin — mas isso e so CSS)</p>
</body></html>"""

USUARIOS = {42: "ana.silva"}


class HandlerInseguro(http.server.BaseHTTPRequestHandler):
    server_version = "PainelDemo/1.0"
    sys_version = ""

    def do_GET(self):
        if self.path == "/":
            corpo = PAGINA.encode()
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(corpo)
        elif self.path.startswith("/excluir"):
            # NUNCA verifica quem esta pedindo — so confia que, se o botao
            # estava escondido na tela, ninguem chegaria aqui.
            USUARIOS.pop(42, None)
            corpo = b"usuario 42 excluido"
            self.send_response(200)
            self.end_headers()
            self.wfile.write(corpo)
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, *a):
        pass


def main():
    socketserver.TCPServer.allow_reuse_address = True
    servidor = socketserver.TCPServer(("127.0.0.1", PORTA), HandlerInseguro)
    threading.Thread(target=servidor.serve_forever, daemon=True).start()
    time.sleep(0.3)

    print(f"=== servidor real em 127.0.0.1:{PORTA} ===")
    print(f"  usuarios antes: {USUARIOS}")

    print("\n=== requisicao HTTP direta para /excluir, sem nunca ter carregado a pagina ===")
    resposta = urllib.request.urlopen(f"http://127.0.0.1:{PORTA}/excluir?id=42")
    print(f"  status: {resposta.status}")
    print(f"  corpo:  {resposta.read().decode()}")

    print(f"\n  usuarios depois: {USUARIOS}")

    print("\n=== leitura ===")
    print("  O botao nunca apareceu na tela — e nao precisou aparecer. A requisicao")
    print("  HTTP direta, sem passar pela pagina nem pelo JS que esconde o botao,")
    print("  teve exatamente o mesmo efeito. Esconder um controle na interface e")
    print("  UX, nao autorizacao: o servidor e quem decide se aceita a requisicao,")
    print("  e neste exemplo ele decidiu aceitar qualquer uma.")

    servidor.shutdown()


if __name__ == "__main__":
    main()
