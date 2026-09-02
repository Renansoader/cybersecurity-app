# -*- coding: utf-8 -*-
"""Laboratorio 3.4 — validacao que so existe no navegador nao e controle.

Sobe um servidor HTTP real em 127.0.0.1. A pagina tem um formulario com
JavaScript que bloqueia o envio se "quantidade" passar de 5 — mas o
endpoint que recebe o formulario aceita qualquer valor, porque confia que
"se chegou aqui, o JS ja validou". Uma requisicao POST direta, sem nunca
executar o JavaScript da pagina, prova o contrario. Nenhum host de
terceiro e tocado; o servidor derruba sozinho ao final do script.

Roda com: python validacao_so_no_cliente.py
"""

import http.server
import socketserver
import threading
import time
import urllib.parse
import urllib.request

PORTA = 8092
ESTOQUE = 5

PAGINA = """<html><body>
<form id="pedido">
  <input name="quantidade" id="quantidade">
  <button type="submit">Comprar</button>
</form>
<script>
document.getElementById('pedido').onsubmit = function(e) {
  var q = parseInt(document.getElementById('quantidade').value);
  if (q > 5) { alert('maximo 5 unidades'); e.preventDefault(); }
};
</script>
</body></html>"""


class Handler(http.server.BaseHTTPRequestHandler):
    server_version = "LojaDemo/1.0"
    sys_version = ""

    def do_GET(self):
        corpo = PAGINA.encode()
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(corpo)

    def do_POST(self):
        tamanho = int(self.headers.get("Content-Length", 0))
        dados = urllib.parse.parse_qs(self.rfile.read(tamanho).decode())
        quantidade = int(dados.get("quantidade", ["0"])[0])
        # NUNCA revalida o limite — confia que o JS da pagina ja bloqueou
        # qualquer pedido acima de 5.
        global ESTOQUE
        ESTOQUE -= quantidade
        corpo = f"pedido aceito: {quantidade} unidades. estoque restante: {ESTOQUE}".encode()
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

    print(f"=== servidor real em 127.0.0.1:{PORTA} ===")
    print(f"  estoque inicial: {ESTOQUE}")
    print("  regra do formulario (só em JavaScript, no navegador): quantidade <= 5")

    print("\n=== POST direto pedindo 9999 unidades, sem nunca executar o JavaScript da página ===")
    dados = urllib.parse.urlencode({"quantidade": "9999"}).encode()
    req = urllib.request.Request(f"http://127.0.0.1:{PORTA}/", data=dados, method="POST")
    resposta = urllib.request.urlopen(req)
    print(f"  status: {resposta.status}")
    print(f"  corpo:  {resposta.read().decode()}")

    print("\n=== leitura ===")
    print("  A regra 'quantidade <= 5' nunca existiu para o servidor — ela existia")
    print("  só no JavaScript que roda dentro do navegador de quem usa a página")
    print("  normalmente. Uma requisição que não passa pelo navegador não passa")
    print("  por essa regra nenhuma. Validação no cliente é conveniência para o")
    print("  usuário legítimo; não é, e nunca foi, um controle de segurança.")

    servidor.shutdown()


if __name__ == "__main__":
    main()
