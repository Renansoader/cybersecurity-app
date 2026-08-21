"""Laboratorio de varredura e enumeracao — SO CONTRA ALVO PROPRIO.

Sobe o alvo de alvo_local.py dentro do proprio processo, em 127.0.0.1, e roda
contra ele: varredura de portas por conexao, coleta de banner, leitura de
cabecalho HTTP e enumeracao de diretorio. Nenhum endereco de terceiro e tocado.
"""
import http.server, socket, socketserver, threading, time, urllib.request, urllib.error

import alvo_local

PORTAS_ALVO = [22, 80, 443, 2525, 3306, 8080, 8443, 9000]


def sobe_alvo():
    socketserver.TCPServer.allow_reuse_address = True
    web = socketserver.TCPServer(("127.0.0.1", 8080), alvo_local.Handler)
    threading.Thread(target=web.serve_forever, daemon=True).start()
    threading.Thread(target=alvo_local.banner_tcp, args=(2525,), daemon=True).start()
    time.sleep(0.5)
    return web


def varre(host, portas, espera=0.3):
    """Varredura por conexao completa: o mesmo que -sT faz, e o que o alvo registra."""
    resultado = []
    for porta in portas:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(espera)
        inicio = time.perf_counter()
        estado = "aberta" if s.connect_ex((host, porta)) == 0 else "fechada/filtrada"
        gasto = time.perf_counter() - inicio
        s.close()
        resultado.append((porta, estado, gasto))
    return resultado


def banner(host, porta, espera=1.0):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(espera)
    try:
        s.connect((host, porta))
        return s.recv(256).decode(errors="replace").strip()
    except OSError as erro:
        return f"(sem banner: {type(erro).__name__})"
    finally:
        s.close()


def cabecalhos(url):
    try:
        with urllib.request.urlopen(url, timeout=2) as r:
            return r.status, dict(r.headers)
    except urllib.error.HTTPError as e:
        return e.code, dict(e.headers)


def enumera(base, caminhos):
    achados = []
    for caminho in caminhos:
        req = urllib.request.Request(base + caminho, method="GET")
        try:
            with urllib.request.urlopen(req, timeout=2) as r:
                achados.append((caminho, r.status, len(r.read())))
        except urllib.error.HTTPError as e:
            achados.append((caminho, e.code, len(e.read())))
        except OSError as e:
            achados.append((caminho, "erro", type(e).__name__))
    return achados


if __name__ == "__main__":
    sobe_alvo()
    print("=== 1. varredura por conexao em 127.0.0.1 (alvo proprio) ===")
    for porta, estado, gasto in varre("127.0.0.1", PORTAS_ALVO):
        marca = "  <-- aberta" if estado == "aberta" else ""
        print(f"  {porta:>5}/tcp  {estado:<18} {gasto*1000:6.1f} ms{marca}")

    print()
    print("=== 2. banner do servico em 127.0.0.1:2525 ===")
    print("  " + banner("127.0.0.1", 2525))
    print("  porta 8080 (HTTP nao fala primeiro):", banner("127.0.0.1", 8080, 0.6))

    print()
    print("=== 3. cabecalho da resposta HTTP em 127.0.0.1:8080 ===")
    codigo, cab = cabecalhos("http://127.0.0.1:8080/")
    print(f"  status: {codigo}")
    for chave in ("Server", "X-Powered-By", "Content-Type", "Content-Length"):
        if chave in cab:
            print(f"  {chave}: {cab[chave]}")

    print()
    print("=== 4. enumeracao de caminhos com lista pequena ===")
    lista = ["/", "/admin", "/backup", "/api/status", "/.git/config", "/naoexiste", "/painel"]
    for caminho, codigo, tam in enumera("http://127.0.0.1:8080", lista):
        print(f"  {caminho:<14} {codigo}  {tam} bytes")
    print()
    print("  Observacao: 401 e 403 tambem revelam que o caminho existe.")
    print("  Filtrar so por 200 perde metade do mapa.")
