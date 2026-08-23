"""Linha de base e desvio: o mecanismo central do hardening, em 40 linhas.

Somente leitura. Compara as portas em escuta desta maquina com uma linha de base
declarada e classifica cada diferenca. E o que uma ferramenta de conformidade faz
em escala: nao existe "seguro", existe "igual ao que foi declarado".
"""
import socket
import subprocess

# Linha de base fictícia, no formato que uma organizacao declararia:
# porta -> (servico esperado, justificativa registrada)
LINHA_BASE = {
    135: ("RPC endpoint mapper", "exigido pelo sistema"),
    445: ("SMB", "compartilhamento de arquivos interno"),
    3389: ("RDP", "acesso remoto autorizado, restrito por firewall"),
}


def em_escuta():
    """Portas TCP em escuta, lidas do proprio sistema."""
    saida = subprocess.run(["netstat", "-an"], capture_output=True, text=True).stdout
    portas = set()
    for linha in saida.splitlines():
        if "LISTENING" not in linha.upper():
            continue
        campos = linha.split()
        if len(campos) < 2:
            continue
        endereco = campos[1]
        if ":" in endereco:
            porta = endereco.rsplit(":", 1)[1]
            if porta.isdigit():
                portas.add(int(porta))
    return portas


def classificar(portas):
    desvios, conformes, ausentes = [], [], []
    for porta in sorted(portas):
        if porta in LINHA_BASE:
            conformes.append((porta, LINHA_BASE[porta][0]))
        elif porta >= 49152:
            continue  # faixa efemera: nao e servico publicado
        else:
            desvios.append(porta)
    for porta, (servico, _) in sorted(LINHA_BASE.items()):
        if porta not in portas:
            ausentes.append((porta, servico))
    return conformes, desvios, ausentes


if __name__ == "__main__":
    portas = em_escuta()
    conformes, desvios, ausentes = classificar(portas)

    print("=== conforme a linha de base ===")
    for porta, servico in conformes:
        print(f"  {porta:>5}  {servico}  — declarado, com justificativa registrada")

    print()
    print("=== desvio: em escuta e fora da linha de base ===")
    for porta in desvios:
        print(f"  {porta:>5}  sem justificativa registrada — investigar ou fechar")

    print()
    print("=== declarado e ausente ===")
    for porta, servico in ausentes:
        print(f"  {porta:>5}  {servico} — nao esta em escuta; a linha de base envelheceu")

    print()
    print(f"resumo: {len(conformes)} conformes, {len(desvios)} desvios, {len(ausentes)} ausentes")
    print("A linha de base nao mede seguranca: mede distancia entre o declarado e o real.")
