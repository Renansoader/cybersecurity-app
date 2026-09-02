# -*- coding: utf-8 -*-
"""Laboratorio 4.8 — cadeia de custodia como matematica, nao como formulario.

Modelo declarado: uma cadeia de custodia registrada como uma lista de
eventos (quem, quando, o que fez), onde cada evento carrega o hash do
evento anterior mais os proprios dados. Nao acessa nenhum arquivo real —
e simulacao pura, no mesmo padrao de modo_de_falha_comum.py (4.3) e
autoridade_pre_combinada.py (4.7).

A pergunta: um formulario em papel prova alguma coisa sozinho? E uma
planilha editavel?

Roda com: python cadeia_de_custodia.py
"""

import hashlib


def hash_evento(evento, hash_anterior):
    bruto = f"{hash_anterior}|{evento['quem']}|{evento['quando']}|{evento['acao']}"
    return hashlib.sha256(bruto.encode("utf-8")).hexdigest()


def construir_cadeia(eventos):
    cadeia = []
    hash_anterior = "0" * 64  # hash genesis, sem evento anterior
    for evento in eventos:
        h = hash_evento(evento, hash_anterior)
        cadeia.append({**evento, "hash": h, "hash_anterior": hash_anterior})
        hash_anterior = h
    return cadeia


def verificar_cadeia(cadeia):
    """Recalcula cada hash a partir dos dados registrados e do hash anterior
    guardado. Se algum evento foi editado depois do registro, o hash
    recalculado diverge do hash guardado — a adulteracao fica evidente sem
    precisar de nenhuma assinatura externa."""
    hash_anterior = "0" * 64
    for i, evento in enumerate(cadeia):
        h_recalculado = hash_evento(evento, hash_anterior)
        if h_recalculado != evento["hash"]:
            return False, i
        hash_anterior = evento["hash"]
    return True, None


EVENTOS = [
    {"quem": "perito A", "quando": "2026-09-02 09:00", "acao": "imagem de disco criada, sha256 registrado"},
    {"quem": "perito A", "quando": "2026-09-02 09:15", "acao": "imagem transferida para cofre digital"},
    {"quem": "perito B", "quando": "2026-09-03 14:00", "acao": "imagem analisada em ambiente isolado"},
    {"quem": "perito B", "quando": "2026-09-03 16:30", "acao": "relatorio de achados gerado"},
]


def main():
    cadeia = construir_cadeia(EVENTOS)

    print("=== cadeia de custódia, como registrada ===")
    for i, ev in enumerate(cadeia):
        print(f"  [{i}] {ev['quando']} {ev['quem']:<10} {ev['acao']}")
        print(f"      hash: {ev['hash'][:16]}...")

    ok, onde = verificar_cadeia(cadeia)
    print(f"\n=== verificação da cadeia original ===")
    print(f"  íntegra: {ok}")

    print("\n=== simulando uma adulteração: alguém reescreve o evento [2] ===")
    cadeia_adulterada = [dict(e) for e in cadeia]
    cadeia_adulterada[2]["quando"] = "2026-09-02 09:20"  # tenta encobrir um gap de 29h entre coleta e análise
    ok2, onde2 = verificar_cadeia(cadeia_adulterada)
    print(f"  íntegra: {ok2}")
    if not ok2:
        print(f"  divergência detectada a partir do evento [{onde2}]")

    print("\n=== leitura ===")
    print("  Mudar UM campo de UM evento no meio da cadeia quebra o hash dele")
    print("  e de todos os eventos seguintes — a verificação não depende de")
    print("  confiar em quem assinou o formulário, depende de recalcular. É a")
    print("  diferença entre 'cadeia de custódia' como registro cronológico de")
    print("  papel — que qualquer um pode reescrever sem deixar rastro — e como")
    print("  propriedade matemática verificável por qualquer terceiro.")


if __name__ == "__main__":
    main()
