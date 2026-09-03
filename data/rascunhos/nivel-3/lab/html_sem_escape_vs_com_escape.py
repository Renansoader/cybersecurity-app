# -*- coding: utf-8 -*-
"""Laboratorio 3.5 — dado que vira instrucao: marcacao renderizada no navegador.

Sobe um servidor HTTP real em 127.0.0.1, so para esta execucao, com duas
rotas: uma que devolve a entrada do usuario direto dentro do HTML, outra
que escapa a entrada antes de devolver. Usa uma tag inofensiva (<b>, deixa
o texto em negrito) para provar o mecanismo — o mesmo raciocinio vale para
qualquer tag, o ponto nao e a tag especifica, e sim se o navegador
interpreta o dado como marcacao ou como texto. Nenhum host de terceiro e
tocado; o servidor derruba sozinho ao final.

Roda com: python html_sem_escape_vs_com_escape.py
"""

import html
import http.server
import socketserver
import threading
import time
import urllib.parse
import urllib.request

PORTA = 8096


class Handler(http.server.BaseHTTPRequestHandler):
    server_version = "ComentariosDemo/1.0"
    sys_version = ""

    def do_GET(self):
        partes = urllib.parse.urlparse(self.path)
        params = urllib.parse.parse_qs(partes.query)
        comentario = params.get("comentario", [""])[0]

        if partes.path == "/sem-escape":
            corpo = f"<html><body><p>Comentário: {comentario}</p></body></html>".encode()
        elif partes.path == "/com-escape":
            seguro = html.escape(comentario)
            corpo = f"<html><body><p>Comentário: {seguro}</p></body></html>".encode()
        else:
            self.send_response(404)
            self.end_headers()
            return

        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(corpo)

    def log_message(self, *a):
        pass


def main():
    socketserver.TCPServer.allow_reuse_address = True
    servidor = socketserver.TCPServer(("127.0.0.1", PORTA), Handler)
    threading.Thread(target=servidor.serve_forever, daemon=True).start()
    time.sleep(0.3)

    comentario_usuario = "<b>ótimo produto</b>"  # tag inofensiva, só para provar o mecanismo

    print(f"=== servidor real em 127.0.0.1:{PORTA} ===")
    print(f"  comentário enviado pelo usuário: {comentario_usuario!r}")

    print("\n=== rota /sem-escape (entrada colada direto no HTML) ===")
    url = f"http://127.0.0.1:{PORTA}/sem-escape?" + urllib.parse.urlencode({"comentario": comentario_usuario})
    resposta = urllib.request.urlopen(url).read().decode()
    print(f"  HTML devolvido: {resposta}")

    print("\n=== rota /com-escape (entrada escapada antes de entrar no HTML) ===")
    url = f"http://127.0.0.1:{PORTA}/com-escape?" + urllib.parse.urlencode({"comentario": comentario_usuario})
    resposta = urllib.request.urlopen(url).read().decode()
    print(f"  HTML devolvido: {resposta}")

    print("\n=== leitura ===")
    print("  Na rota sem escape, as tags <b> chegam intactas no HTML — o navegador")
    print("  de quem lê o comentário vai renderizar como negrito de verdade, porque")
    print("  não existe diferença, para o navegador, entre 'marcação da página' e")
    print("  'texto que um usuário digitou'. Na rota com escape, os mesmos caracteres")
    print("  < e > viram &lt; e &gt; — o navegador exibe a tag como TEXTO literal,")
    print("  porque ela deixou de ter forma de instrução. A tag usada aqui só deixa")
    print("  texto em negrito; a mesma lacuna aceita qualquer tag, inclusive as que")
    print("  executam código.")

    servidor.shutdown()


if __name__ == "__main__":
    main()
