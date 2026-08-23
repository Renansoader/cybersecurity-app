"""Filtro sem estado x filtro com estado, em 40 linhas e sem tocar na rede.

Simula as duas politicas contra a mesma sequencia de pacotes de uma conexao HTTPS
de saida. O ponto do modulo: o filtro sem estado precisa de uma regra de entrada
permanente e larga para o trafego de volta; o filtro com estado nao precisa,
porque ele lembra da conexao que ele mesmo deixou sair.
"""

# (direcao, origem, porta_origem, destino, porta_destino, flag)
SEQUENCIA = [
    ("saida",   "192.168.100.6", 51520, "203.0.113.10", 443, "SYN"),
    ("entrada", "203.0.113.10",  443,   "192.168.100.6", 51520, "SYN-ACK"),
    ("saida",   "192.168.100.6", 51520, "203.0.113.10", 443, "ACK"),
    ("entrada", "203.0.113.10",  443,   "192.168.100.6", 51520, "dados"),
    # pacote nao solicitado: ninguem pediu, chega do mesmo par origem/porta
    ("entrada", "198.51.100.77", 443,   "192.168.100.6", 51521, "SYN-ACK"),
]

# Filtro sem estado: so olha o pacote isolado. Para o retorno funcionar, alguem
# precisa liberar "qualquer coisa vinda da porta 443" — e e isso que abre o flanco.
REGRAS_SEM_ESTADO = [
    ("saida", "qualquer", "qualquer", "permite"),
    ("entrada", 443, "qualquer", "permite"),   # regra larga, exigida pelo retorno
]


def sem_estado(pacote):
    direcao, _, porta_origem, _, _, _ = pacote
    for regra_dir, porta, _, acao in REGRAS_SEM_ESTADO:
        if regra_dir != direcao:
            continue
        if porta == "qualquer" or porta == porta_origem:
            return acao
    return "descarta"


def com_estado(pacote, tabela):
    direcao, origem, porta_origem, destino, porta_destino, _ = pacote
    if direcao == "saida":
        tabela.add((destino, porta_destino, origem, porta_origem))
        return "permite"
    if (origem, porta_origem, destino, porta_destino) in tabela:
        return "permite"
    return "descarta"


if __name__ == "__main__":
    tabela = set()
    print(f"{'pacote':<52} {'sem estado':<12} com estado")
    print("-" * 78)
    for pacote in SEQUENCIA:
        direcao, origem, po, destino, pd, flag = pacote
        rotulo = f"{direcao:<8} {origem}:{po} -> {destino}:{pd} [{flag}]"
        print(f"{rotulo:<52} {sem_estado(pacote):<12} {com_estado(pacote, tabela)}")
    print()
    print(f"conexoes na tabela de estado ao final: {len(tabela)}")
