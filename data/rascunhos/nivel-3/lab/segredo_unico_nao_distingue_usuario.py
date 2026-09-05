# -*- coding: utf-8 -*-
"""Laboratorio 3.9 -- um segredo compartilhado por todos nao autentica
ninguem, so a rede.

Nenhuma captura, nenhum ataque contra rede de terceiro, nenhum handshake:
so a matematica de verificacao de senha, comparando dois desenhos —
segredo unico (modo domestico/pessoal) contra segredo por pessoa (modo
corporativo) — com senhas e identidades inventadas para este script.

Roda com: python segredo_unico_nao_distingue_usuario.py
"""

import hmac
import hashlib


def verifica_modo_pessoal(senha_tentada, senha_da_rede):
    """Um unico segredo vale para a rede inteira. A funcao so pode
    responder 'sim, alguem que sabe a senha' -- nunca 'sim, e a Alice'."""
    return hmac.compare_digest(senha_tentada.encode(), senha_da_rede.encode())


def verifica_modo_corporativo(usuario, senha_tentada, tabela_de_credenciais):
    """Cada pessoa tem o proprio par usuario/senha, guardado a parte
    (o papel do servidor de autenticacao citado em 4.2.t6). A funcao
    responde 'sim, e esta pessoa especifica' -- ou nega so essa pessoa."""
    esperado = tabela_de_credenciais.get(usuario)
    if esperado is None:
        return False
    return hmac.compare_digest(senha_tentada.encode(), esperado.encode())


def main():
    senha_da_rede = "cafe-com-leite-2026"  # inventada, senha unica do modo pessoal

    print("=== modo pessoal: um segredo para a rede inteira ===")
    for nome, senha_usada in [
        ("Ana (dona da rede)", senha_da_rede),
        ("Bruno (visitante autorizado)", senha_da_rede),
        ("Desconhecido (achou a senha anotada num post-it)", senha_da_rede),
    ]:
        ok = verifica_modo_pessoal(senha_usada, senha_da_rede)
        print(f"  {nome}: {'aceito' if ok else 'recusado'}")

    print("\n  a rede aceitou os tres com a MESMA resposta -- ela nao tem")
    print("  como saber que o terceiro nao deveria estar ali. So resta uma")
    print("  acao possivel para tirar so ele: trocar a senha da rede")
    print("  inteira, o que derruba Ana e Bruno tambem.")

    print("\n=== modo corporativo: um segredo por pessoa ===")
    tabela = {
        "ana": "senha-da-ana-2026",
        "bruno": "senha-do-bruno-2026",
    }
    tentativas = [
        ("ana", "senha-da-ana-2026"),
        ("bruno", "senha-do-bruno-2026"),
        ("bruno", "senha-da-ana-2026"),  # bruno tentando a senha da ana
    ]
    for usuario, senha_tentada in tentativas:
        ok = verifica_modo_corporativo(usuario, senha_tentada, tabela)
        print(f"  usuario '{usuario}' com a senha tentada: "
              f"{'aceito' if ok else 'recusado'}")

    print("\n  revogar so o bruno, sem tocar na credencial da ana:")
    del tabela["bruno"]
    ok = verifica_modo_corporativo("bruno", "senha-do-bruno-2026", tabela)
    ok_ana = verifica_modo_corporativo("ana", "senha-da-ana-2026", tabela)
    print(f"  bruno depois de revogado: {'aceito' if ok else 'recusado'}")
    print(f"  ana, sem ter sido tocada:  {'aceito' if ok_ana else 'recusado'}")

    print("\n=== leitura ===")
    print("  a funcao de verificacao do modo pessoal so pode responder")
    print("  'alguem que sabe a senha' -- ela nunca recebeu identidade")
    print("  nenhuma para comparar. O modo corporativo verifica um par")
    print("  usuario+segredo, o que torna possivel negar UMA identidade")
    print("  sem afetar as outras -- a diferenca nao e a forca da senha,")
    print("  e o que a funcao de verificacao consegue enxergar.")


if __name__ == "__main__":
    main()
