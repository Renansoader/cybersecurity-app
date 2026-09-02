# -*- coding: utf-8 -*-
"""Laboratorio 3.4 — o cookie de sessao volta sozinho, sem checar quem pediu.

Sobe um servidor HTTP real em 127.0.0.1. Um "login" define um cookie de
sessao. Depois, este script monta uma requisicao para uma acao sensivel
(transferir saldo) usando a biblioteca padrao de cookies do Python
(http.cookiejar) — o mesmo mecanismo de correspondencia por dominio que um
navegador usa. A requisicao nunca passa pela pagina de login de novo: o
cookie e anexado automaticamente so por bater o dominio, exatamente o
mecanismo que um formulario escondido em outro site exploraria (CSRF).
Nenhum host de terceiro e tocado; o servidor derruba sozinho ao final.

Roda com: python reenvio_automatico_de_cookie.py
"""

import http.cookiejar
import http.server
import socketserver
import threading
import time
import urllib.parse
import urllib.request

PORTA = 8093
SALDO = {"conta": 1000}


class Handler(http.server.BaseHTTPRequestHandler):
    server_version = "BancoDemo/1.0"
    sys_version = ""

    def do_GET(self):
        if self.path == "/login":
            self.send_response(200)
            self.send_header("Set-Cookie", "sessao=abc123; Path=/")
            self.end_headers()
            self.wfile.write(b"login ok")
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        cookie = self.headers.get("Cookie", "")
        tamanho = int(self.headers.get("Content-Length", 0))
        dados = urllib.parse.parse_qs(self.rfile.read(tamanho).decode())
        valor = int(dados.get("valor", ["0"])[0])
        # So confia que existe UM cookie de sessao valido — nunca confere
        # se a requisicao veio da propria pagina do banco ou de outro lugar.
        if "sessao=abc123" in cookie:
            SALDO["conta"] -= valor
            corpo = f"transferencia de {valor} aceita. saldo: {SALDO['conta']}".encode()
        else:
            corpo = b"sem sessao valida"
        self.send_response(200)
        self.end_headers()
        self.wfile.write(corpo)

    def log_message(self, *a):
        pass


def main():
    socketserver.TCPServer.allow_reuse_address = True
    servidor = socketserver.TCPServer(("127.0.0.1", PORTA), Handler)
    threading.Thread(target=servidor.serve_forever, daemon=True).start()
    time.sleep(0.3)

    jar = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(jar))

    print(f"=== servidor real em 127.0.0.1:{PORTA} ===")
    print(f"  saldo antes: {SALDO['conta']}")

    print("\n=== login uma vez, cookie de sessão guardado pelo cliente ===")
    opener.open(f"http://127.0.0.1:{PORTA}/login")
    print(f"  cookies guardados: {[str(c) for c in jar]}")

    print("\n=== requisição de transferência, montada como se viesse de OUTRA página ===")
    print("  (mesma lógica que um <form> escondido em outro site dispararia:")
    print("  o navegador anexa o cookie sozinho, só porque o domínio bate)")
    dados = urllib.parse.urlencode({"valor": "1000"}).encode()
    req = urllib.request.Request(f"http://127.0.0.1:{PORTA}/", data=dados, method="POST")
    resposta = opener.open(req)
    print(f"  status: {resposta.status}")
    print(f"  corpo:  {resposta.read().decode()}")

    print(f"\n  saldo depois: {SALDO['conta']}")

    print("\n=== leitura ===")
    print("  O jar de cookies (a mesma lógica que um navegador usa) anexou o")
    print("  cookie de sessão à requisição de transferência automaticamente —")
    print("  não porque confirmou que o pedido veio da página legítima do banco,")
    print("  só porque o domínio bateu. É exatamente esse reenvio automático,")
    print("  cego a quem pediu, que um formulário escondido em outro site")
    print("  exploraria: a vítima só precisa estar logada, em outra aba, quando")
    print("  visita a página maliciosa.")

    servidor.shutdown()


if __name__ == "__main__":
    main()
