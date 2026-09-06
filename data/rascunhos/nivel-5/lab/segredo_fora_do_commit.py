# -*- coding: utf-8 -*-
"""Laboratorio 5.1 -- segredo vaza sem nunca passar por um commit.

Nenhum segredo real: a chave abaixo e inventada só para este script. Nao
usa Git, nao commita nada -- demonstra outro lugar do ciclo de vida onde um
segredo escapa: uma excecao nao tratada que imprime as variaveis locais
(inclusive a chave) direto num arquivo de log, sem que ninguem tenha feito
nada com controle de versao.

Roda com: python segredo_fora_do_commit.py
"""

import logging
import traceback


CHAVE_DE_API = "sk-exemplo-inventado-000111222"  # nunca commitada, so' existe em memoria


def chamar_servico_externo(payload):
    # simula uma falha de rede que interrompe a chamada no meio
    raise ConnectionError(f"timeout ao chamar servico externo com payload={payload!r}")


def processar_pedido(pedido_id):
    cabecalho_autenticacao = {"Authorization": f"Bearer {CHAVE_DE_API}"}
    return chamar_servico_externo({"pedido": pedido_id, "auth": cabecalho_autenticacao})


def main():
    logging.basicConfig(filename="pedido_saida.log", level=logging.ERROR,
                         format="%(asctime)s %(levelname)s %(message)s")

    try:
        processar_pedido(4471)
    except Exception:
        # erro comum: logar a excecao "completa" para facilitar debug
        logging.error("falha ao processar pedido:\n%s", traceback.format_exc())

    print("=== conteudo do log gerado ===")
    with open("pedido_saida.log", encoding="utf-8") as f:
        conteudo = f.read()
    print(conteudo)

    vazou = CHAVE_DE_API in conteudo
    print(f"a chave de API aparece no arquivo de log? {vazou}")

    print("\n=== leitura ===")
    print("  nenhum 'git add', nenhum commit -- a chave nunca chegou perto")
    print("  de controle de versao. ela vazou porque o codigo, ao tratar")
    print("  o erro, imprimiu a propria estrutura de dados que a carregava.")
    print("  a resposta de 1.7 para segredo no historico do git (rotacionar,")
    print("  nao apagar) continua certa aqui, mas o vazamento em si aconteceu")
    print("  num lugar que revisao de commit nunca alcanca: log de execucao,")
    print("  em producao, gerado por um caminho de codigo que ninguem pensou")
    print("  em testar com uma chave de verdade.")


if __name__ == "__main__":
    main()
