# -*- coding: utf-8 -*-
"""Laboratorio 3.6 (eixo 1) — checar o papel nao e checar o objeto.

Sobe um servidor HTTP real em 127.0.0.1. O endpoint /aprovar EXIGE papel
"gerente" e confere isso a cada requisicao (a licao do 3.4 esta aplicada:
decisao no servidor, nunca so na tela). Mesmo assim, uma gerente de um
departamento aprova uma despesa de outro departamento, porque o servidor
nunca comparou o dono da despesa com quem está pedindo — ele checou QUEM
decide (papel), nunca SOBRE QUE OBJETO. Autenticado e autorizado por papel
nao e o mesmo que autorizado para este recurso especifico.

Roda com: python autorizacao_por_papel_sem_objeto.py
"""

import http.server
import json
import socketserver
import threading
import time
import urllib.request

PORTA = 8101

DESPESAS = {
    501: {"departamento": "engenharia", "valor": 4200, "status": "pendente"},
    502: {"departamento": "marketing", "valor": 900, "status": "pendente"},
}

SESSOES = {
    "tok-carla": {"usuario": "carla", "papel": "gerente", "departamento": "marketing"},
}


class HandlerInseguro(http.server.BaseHTTPRequestHandler):
    server_version = "AprovacaoDemo/1.0"
    sys_version = ""

    def do_POST(self):
        if not self.path.startswith("/aprovar"):
            self.send_response(404)
            self.end_headers()
            return

        token = self.headers.get("Authorization", "").replace("Bearer ", "")
        sessao = SESSOES.get(token)

        # A verificacao roda a cada requisicao, no servidor -- a licao do 3.4
        # esta aplicada. O defeito e o QUE ela checa: so o papel.
        if not sessao or sessao["papel"] != "gerente":
            self.send_response(403)
            self.end_headers()
            self.wfile.write(b"papel insuficiente")
            return

        despesa_id = int(self.path.split("=")[1])
        despesa = DESPESAS.get(despesa_id)
        if despesa is None:
            self.send_response(404)
            self.end_headers()
            return

        # NUNCA compara despesa["departamento"] com sessao["departamento"].
        despesa["status"] = "aprovada"
        self.send_response(200)
        self.end_headers()
        self.wfile.write(json.dumps(despesa).encode())

    def log_message(self, *a):
        pass


def main():
    socketserver.TCPServer.allow_reuse_address = True
    servidor = socketserver.TCPServer(("127.0.0.1", PORTA), HandlerInseguro)
    threading.Thread(target=servidor.serve_forever, daemon=True).start()
    time.sleep(0.3)

    print(f"=== servidor real em 127.0.0.1:{PORTA} ===")
    print(f"  sessao: carla, papel=gerente, departamento=marketing")
    print(f"  despesa 501 antes: {DESPESAS[501]}")

    print("\n=== carla (gerente de marketing) aprova a despesa 501, da engenharia ===")
    req = urllib.request.Request(
        f"http://127.0.0.1:{PORTA}/aprovar?id=501", method="POST",
        headers={"Authorization": "Bearer tok-carla"})
    resposta = urllib.request.urlopen(req)
    print(f"  status: {resposta.status}")
    print(f"  corpo:  {resposta.read().decode()}")

    print(f"\n  despesa 501 depois: {DESPESAS[501]}")

    print("\n=== leitura ===")
    print("  O servidor checou o papel a cada requisicao -- nao confiou na tela,")
    print("  a licao do 3.4 esta presente. E mesmo assim aprovou uma despesa de")
    print("  outro departamento: a condicao avaliada foi 'e gerente?', nunca")
    print("  'e gerente DESTE departamento, sobre ESTA despesa?'. Autenticacao e")
    print("  papel respondem quem decide; autorizacao por objeto responde sobre")
    print("  que recurso especifico a decisao vale -- e sao perguntas diferentes.")

    servidor.shutdown()


if __name__ == "__main__":
    main()
