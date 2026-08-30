# -*- coding: utf-8 -*-
"""Laboratorio 4.4 — o que sobrevive a isolar e o que sobrevive a desligar.

Nao executa nada, nao captura nada e nao toca em rede. E um modelo declarado
neste proprio arquivo, alimentado por uma contagem real desta maquina feita a
parte, em modo somente leitura e sem nome de processo, usuario ou endereco.

A pergunta: um host suspeito precisa sair do caminho. Arrancar da tomada e
isolar da rede parecem a mesma decisao e nao sao.

Roda com: python isolar_ou_desligar.py
"""

# Contagem real desta maquina, 25/08/2026, somente leitura, agregada.
# Get-Process, Get-NetTCPConnection e Get-Service. Nenhum nome coletado.
MEDIDO = {
    "processos em execucao": 309,
    "conexoes TCP estabelecidas": 101,
    "portas em escuta": 31,
    "servicos em execucao": 145,
    "modulos carregados no total": 8434,
}

# Ordem de volatilidade: do que some primeiro para o que dura mais.
# sobrevive_isolar / sobrevive_desligar sao propriedades do artefato, nao
# opiniao: memoria some quando a energia acaba, disco nao.
ARTEFATOS = [
    ("conteudo da memoria dos processos", False , True),
    ("tabela de conexoes de rede em uso", False , True),
    ("processos em execucao e seus modulos", False , True),
    ("chaves e segredos so carregados em RAM", False , True),
    ("area de troca e arquivo de hibernacao", True  , True),
    ("registros de evento ja gravados", True  , True),
    ("arquivos em disco e horarios deles", True  , True),
    ("tarefas agendadas e servicos declarados", True  , True),
]
# tupla: (nome, sobrevive_a_desligar, sobrevive_a_isolar)



def main():
    print("=== quanto estado volatil existe agora nesta maquina ===")
    for k, v in MEDIDO.items():
        print(f"  {k:<32} {v:>6}")
    print("\n  Tudo isso desaparece no instante em que a energia acaba.")

    print("\n=== o que sobrevive a cada decisao ===")
    print(f"  {'artefato':<42} {'desligar':>9} {'isolar':>10}")
    for nome, desl, isol in ARTEFATOS:
        m = lambda b: "sobrevive" if b else "perde"
        print(f"  {nome:<42} {m(desl):>9} {m(isol):>10}")

    perde_desligar = [n for n, d, i in ARTEFATOS if not d]
    perde_isolar = [n for n, d, i in ARTEFATOS if not i]
    print(f"\n  desligar destroi {len(perde_desligar)} das {len(ARTEFATOS)} categorias")
    print(f"  isolar destroi   {len(perde_isolar)} das {len(ARTEFATOS)} categorias")

    print("\n=== o que cada decisao interrompe ===")
    print("  desligar : interrompe a cifra em curso, a exfiltracao e o processo")
    print("             malicioso — e a evidencia volatil junto")
    print("  isolar   : interrompe a exfiltracao e o comando remoto, e mantem")
    print("             o processo vivo com a memoria intacta para captura")

    print("\n=== leitura ===")
    print("  As duas decisoes param a saida de dados. So uma delas preserva as")
    print("  quatro categorias volateis — e sao justamente as que respondem de")
    print("  onde o codigo veio, com quem ele falava e o que ele ja tinha aberto.")
    print("  Isolar nao e sempre a resposta: contra cifra em andamento, cada")
    print("  minuto de processo vivo e mais arquivo perdido, e ai desligar pode")
    print("  ser a escolha certa mesmo custando a memoria.")
    print("  O erro nao e escolher desligar. O erro e escolher sem saber que a")
    print("  conta inclui perder as quatro primeiras linhas da tabela.")


if __name__ == "__main__":
    main()
