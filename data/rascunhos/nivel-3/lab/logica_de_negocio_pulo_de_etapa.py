# -*- coding: utf-8 -*-
"""Laboratorio 3.6 (eixo 4) — pular uma etapa confiando no campo que o
proprio cliente envia.

Sobe um servidor HTTP real em 127.0.0.1 com um fluxo de checkout de duas
etapas: /pagar (marca o pedido como pago, no ESTADO DO SERVIDOR) e
/confirmar (deveria so aceitar se o servidor registrou o pagamento). O
defeito: /confirmar le um campo "pago" que vem NO CORPO DA REQUISICAO,
em vez de checar o estado que ele mesmo guarda. A requisicao e
sintaticamente perfeita -- nenhum caractere especial, nenhum parametro
malformado -- so a etapa de pagamento nunca aconteceu.

Roda com: python logica_de_negocio_pulo_de_etapa.py
"""

import http.server
import json
import socketserver
import threading
import time
import urllib.request

PORTA = 8104

PEDIDOS = {1: {"valor": 899.90, "pago_no_servidor": False, "status": "carrinho"}}


class HandlerInseguro(http.server.BaseHTTPRequestHandler):
    server_version = "CheckoutDemo/1.0"
    sys_version = ""

    def do_POST(self):
        tamanho = int(self.headers.get("Content-Length", 0))
        corpo = json.loads(self.rfile.read(tamanho) or b"{}")

        if self.path == "/pagar":
            # etapa real: so aqui o servidor registraria o pagamento --
            # neste laboratorio ela nunca e chamada pelo cliente malicioso.
            PEDIDOS[1]["pago_no_servidor"] = True
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"pagamento registrado")
            return

        if self.path == "/confirmar":
            # DEFEITO: confia no campo "pago" que o CLIENTE enviou, em vez
            # de checar PEDIDOS[1]["pago_no_servidor"], que e o unico dado
            # que o proprio servidor controla.
            if corpo.get("pago"):
                PEDIDOS[1]["status"] = "confirmado"
                self.send_response(200)
                self.end_headers()
                self.wfile.write(b"pedido confirmado")
            else:
                self.send_response(402)
                self.end_headers()
                self.wfile.write(b"pagamento pendente")
            return

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
    print(f"  pedido 1 antes: {PEDIDOS[1]}")

    print("\n=== /confirmar chamado direto, sem nunca passar por /pagar, ===")
    print("=== mandando {'pago': true} no corpo da propria requisicao    ===")
    dados = json.dumps({"pago": True}).encode()
    req = urllib.request.Request(
        f"http://127.0.0.1:{PORTA}/confirmar", data=dados, method="POST",
        headers={"Content-Type": "application/json"})
    resposta = urllib.request.urlopen(req)
    print(f"  status: {resposta.status}")
    print(f"  corpo:  {resposta.read().decode()}")

    print(f"\n  pedido 1 depois: {PEDIDOS[1]}")

    print("\n=== leitura ===")
    print("  'pago_no_servidor' continua False -- /pagar nunca foi chamado --")
    print("  e ainda assim o pedido virou 'confirmado'. Nao ha caractere")
    print("  especial nem parametro malformado nesta requisicao: ela e")
    print("  sintaticamente perfeita, so chegou fora de ordem, e o servidor")
    print("  aceitou um campo que o proprio cliente inventou como se fosse")
    print("  o registro dele mesmo. Nenhum filtro de entrada pega isso --")
    print("  o defeito e o servidor nao guardar (e checar) o proprio estado.")

    servidor.shutdown()


if __name__ == "__main__":
    main()
