# -*- coding: utf-8 -*-
"""Laboratorio 3.6 (eixo 3) — a MESMA checagem incompleta produz escalada
horizontal e vertical.

Sobe um servidor HTTP real em 127.0.0.1. Uma unica funcao de autorizacao,
`autorizado()`, so confere se existe uma sessao valida -- nunca confere DE
QUEM e o recurso (isso abre escalada horizontal: usuario le a mensagem de
outro usuario) nem QUAL papel a acao exige (isso abre escalada vertical:
usuario comum aciona uma acao de administrador). E a mesma linha de codigo
faltando nos dois casos, nao dois defeitos diferentes.

Roda com: python escalada_horizontal_e_vertical.py
"""

import http.server
import socketserver
import threading
import time
import urllib.request

PORTA = 8103

SESSOES = {"tok-bruno": {"usuario": "bruno", "papel": "usuario"}}
MENSAGENS = {9001: {"dono": "carla", "texto": "combinar reajuste com RH"}}
SISTEMA = {"modo_manutencao": False}


def autorizado(self):
    """So confere se existe sessao -- nunca de quem e o recurso, nunca que
    papel a acao exige. Essa unica lacuna e a raiz dos dois casos abaixo."""
    token = self.headers.get("Authorization", "").replace("Bearer ", "")
    return SESSOES.get(token)


class HandlerInseguro(http.server.BaseHTTPRequestHandler):
    server_version = "PainelDemo/1.0"
    sys_version = ""

    def do_GET(self):
        sessao = autorizado(self)
        if not sessao:
            self.send_response(401)
            self.end_headers()
            return
        if self.path.startswith("/mensagem"):
            # ESCALADA HORIZONTAL: nao compara sessao["usuario"] com
            # mensagem["dono"] -- so exige "alguma sessao existe".
            msg_id = int(self.path.split("=")[1])
            self.send_response(200)
            self.end_headers()
            self.wfile.write(str(MENSAGENS.get(msg_id)).encode())
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        sessao = autorizado(self)
        if not sessao:
            self.send_response(401)
            self.end_headers()
            return
        if self.path.startswith("/manutencao"):
            # ESCALADA VERTICAL: nao compara sessao["papel"] com o papel que
            # a acao exige (deveria ser "admin") -- so exige "alguma sessao".
            SISTEMA["modo_manutencao"] = True
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"modo manutencao ativado")
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
    print("  sessao: bruno, papel=usuario (comum, nao admin)")

    print("\n=== HORIZONTAL: bruno le a mensagem 9001, que e da carla ===")
    req = urllib.request.Request(
        f"http://127.0.0.1:{PORTA}/mensagem?id=9001",
        headers={"Authorization": "Bearer tok-bruno"})
    resposta = urllib.request.urlopen(req)
    print(f"  status: {resposta.status}")
    print(f"  corpo:  {resposta.read().decode()}")

    print(f"\n  sistema antes: {SISTEMA}")
    print("\n=== VERTICAL: bruno (usuario comum) ativa modo manutencao ===")
    req = urllib.request.Request(
        f"http://127.0.0.1:{PORTA}/manutencao", method="POST",
        headers={"Authorization": "Bearer tok-bruno"})
    resposta = urllib.request.urlopen(req)
    print(f"  status: {resposta.status}")
    print(f"  corpo:  {resposta.read().decode()}")
    print(f"  sistema depois: {SISTEMA}")

    print("\n=== leitura ===")
    print("  As duas requisicoes passaram pela MESMA funcao autorizado(), que")
    print("  so confere 'existe sessao?'. No primeiro caso faltou comparar o")
    print("  dono do recurso (horizontal: outra CONTA do mesmo nivel). No")
    print("  segundo faltou comparar o papel exigido (vertical: um NIVEL")
    print("  acima). Sao a mesma lacuna -- 'autenticado' tratado como sinonimo")
    print("  de 'autorizado' -- vista por dois angulos diferentes.")

    servidor.shutdown()


if __name__ == "__main__":
    main()
