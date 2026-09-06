# -*- coding: utf-8 -*-
"""Laboratorio 5.1 -- uma dependencia direta e a ponta de uma arvore inteira.

Nenhum pacote real, nenhum CVE real, nenhum nome de biblioteca de verdade:
o grafo abaixo e inventado para este script, só para medir a forma do
problema -- quantos pacotes um projeto passa a confiar ao declarar uma
unica dependencia direta, e o que acontece quando a falha esta numa folha
that ninguem escolheu de proposito.

Roda com: python arvore_de_dependencia_transitiva.py
"""


# grafo de dependencia inventado: cada pacote aponta para o que ele mesmo
# depende (dependencia transitiva = dependencia da sua dependencia)
GRAFO = {
    "kit-web-rapido": ["motor-de-template", "cliente-http-simples"],
    "motor-de-template": ["analisador-de-texto"],
    "cliente-http-simples": ["biblioteca-de-conexao", "leitor-de-certificado"],
    "analisador-de-texto": ["normalizador-de-unicode"],
    "biblioteca-de-conexao": ["fila-de-eventos"],
    "leitor-de-certificado": [],
    "normalizador-de-unicode": [],
    "fila-de-eventos": ["relogio-monotonico"],
    "relogio-monotonico": [],
}

DIRETA = "kit-web-rapido"  # o unico pacote que o desenvolvedor de fato escolheu e digitou


def arvore_completa(pacote, grafo, visto=None):
    if visto is None:
        visto = set()
    if pacote in visto:
        return visto
    visto.add(pacote)
    for dep in grafo.get(pacote, []):
        arvore_completa(dep, grafo, visto)
    return visto


def profundidade_ate(pacote_alvo, grafo, raiz, caminho=None):
    if caminho is None:
        caminho = [raiz]
    if raiz == pacote_alvo:
        return caminho
    for dep in grafo.get(raiz, []):
        resultado = profundidade_ate(pacote_alvo, grafo, dep, caminho + [dep])
        if resultado:
            return resultado
    return None


def main():
    completa = arvore_completa(DIRETA, GRAFO)
    transitivas = completa - {DIRETA}

    print(f"=== o que '{DIRETA}' realmente traz para o projeto ===")
    print(f"  dependencia escolhida diretamente: 1 ({DIRETA})")
    print(f"  dependencias transitivas trazidas junto: {len(transitivas)}")
    print(f"  total de codigo de terceiro agora rodando no projeto: {len(completa)}")
    print(f"  lista completa: {sorted(completa)}")

    alvo = "relogio-monotonico"
    caminho = profundidade_ate(alvo, GRAFO, DIRETA)
    print(f"\n=== uma falha em '{alvo}', a folha mais distante ===")
    print(f"  caminho ate ela a partir da dependencia direta: {' -> '.join(caminho)}")
    print(f"  profundidade: {len(caminho) - 1} elos de distancia da escolha original")
    print("  ninguem no projeto escreveu 'import relogio-monotonico' --")
    print("  ele entrou porque outra coisa, que entrou por causa de outra")
    print("  coisa, precisava dele.")

    print("\n=== leitura ===")
    print(f"  uma linha (\"instale {DIRETA}\") trouxe {len(transitivas)} pacotes")
    print("  que ninguem no projeto escolheu, leu ou revisou individualmente.")
    print("  uma vulnerabilidade em qualquer um deles e uma vulnerabilidade")
    print("  no projeto -- o codigo roda de qualquer jeito, apareca ele numa")
    print("  linha de import escrita a mao ou no fundo de uma arvore de")
    print("  cinco elos de profundidade. 'nao escrevi essa parte' descreve")
    print("  autoria; nao muda quem executa o codigo quando ele falha.")


if __name__ == "__main__":
    main()
