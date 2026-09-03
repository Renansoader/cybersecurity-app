# -*- coding: utf-8 -*-
"""Laboratorio 3.6 (eixo 2) — verificacao por handler esquece porta; verificacao
central nao.

Sobe um servidor HTTP real em 127.0.0.1 com DOIS metodos na MESMA rota
/pedido: GET (protegido, exige sessao) e DELETE (o mesmo recurso, mas o
programador so lembrou de colar a checagem de sessao no metodo GET -- o
DELETE responde a qualquer requisicao, sem sessao nenhuma). O recurso e um
so; a superficie de entrada sobre ele tem duas portas, e so uma foi trancada.
Nenhum host de terceiro e tocado; o servidor derruba sozinho ao final.

Roda com: python verificacao_por_handler_nao_centralizada.py
"""

import http.server
import socketserver
import threading
import time
import urllib.request

PORTA = 8102

PEDIDOS = {77: {"cliente": "ana.silva", "status": "confirmado"}}


class HandlerInseguro(http.server.BaseHTTPRequestHandler):
    server_version = "PedidosDemo/1.0"
    sys_version = ""

    def do_GET(self):
        if not self.path.startswith("/pedido"):
            self.send_response(404)
            self.end_headers()
            return
        # GET tem a checagem -- exige sessao.
        if self.headers.get("Authorization") != "Bearer sessao-valida":
            self.send_response(401)
            self.end_headers()
            self.wfile.write(b"sem sessao")
            return
        self.send_response(200)
        self.end_headers()
        self.wfile.write(str(PEDIDOS.get(77)).encode())

    def do_DELETE(self):
        if not self.path.startswith("/pedido"):
            self.send_response(404)
            self.end_headers()
            return
        # DELETE e a MESMA rota, o MESMO recurso -- mas ninguem colou a
        # checagem de sessao aqui. O handler foi escrito depois do GET, numa
        # sprint diferente, e a checagem nao veio junto.
        PEDIDOS.pop(77, None)
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"pedido 77 cancelado")

    def log_message(self, *a):
        pass


def main():
    socketserver.TCPServer.allow_reuse_address = True
    servidor = socketserver.TCPServer(("127.0.0.1", PORTA), HandlerInseguro)
    threading.Thread(target=servidor.serve_forever, daemon=True).start()
    time.sleep(0.3)

    print(f"=== servidor real em 127.0.0.1:{PORTA}, rota /pedido (id 77) ===")

    print("\n=== GET /pedido sem sessao (checagem presente) ===")
    req = urllib.request.Request(f"http://127.0.0.1:{PORTA}/pedido?id=77", method="GET")
    try:
        urllib.request.urlopen(req)
    except urllib.error.HTTPError as erro:
        print(f"  status: {erro.code} (recusado, como esperado)")

    print(f"\n  pedidos antes do DELETE: {PEDIDOS}")
    print("\n=== DELETE /pedido, mesma rota, sem sessao nenhuma ===")
    req = urllib.request.Request(f"http://127.0.0.1:{PORTA}/pedido?id=77", method="DELETE")
    resposta = urllib.request.urlopen(req)
    print(f"  status: {resposta.status}")
    print(f"  corpo:  {resposta.read().decode()}")
    print(f"\n  pedidos depois do DELETE: {PEDIDOS}")

    print("\n=== leitura ===")
    print("  GET recusou sem sessao; DELETE, na mesma rota, sobre o mesmo")
    print("  recurso, aceitou. A checagem foi colada no metodo, nao na rota --")
    print("  cada porta nova (metodo, versao, endpoint legado) precisa que")
    print("  alguem lembre de repetir a checagem, e uma vez esquecida a porta")
    print("  fica aberta. Um ponto central -- um decorador aplicado a toda a")
    print("  rota, ou um middleware antes de qualquer handler -- nao depende")
    print("  de lembranca por porta.")

    servidor.shutdown()


if __name__ == "__main__":
    main()
