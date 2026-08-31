"""Chutador burro: estratégias de forma pura para responder múltipla escolha.

Terceira tentativa de medir se a regra 7 do validador (unicidade estrutural —
ver `validar_modulo.py`) mede vazamento real. As duas primeiras tentativas
falharam: amostra manual classificada por quem já sabia o gabarito (não
generaliza) e agente cego instruído a ignorar o mérito técnico (não
generaliza — o modelo por trás do agente já sabe cibersegurança, nenhuma
instrução apaga pré-treino). Esta tira o modelo do circuito: as estratégias
abaixo são regras determinísticas de Python, sem entendimento nenhum do
assunto, então não têm como "trapacear" respondendo pelo conteúdo.

Cada estratégia só recebe `alternativas` (lista de 4 textos) — nunca o campo
`correta`, a explicação, as dicas ou as tags. Quando a heurística não se
aplica (ex.: nenhuma alternativa é estruturalmente única), a estratégia se
abstém (devolve None) em vez de chutar ao acaso — abstenção não conta como
acerto nem como erro no relatório.

Uso:
    python ferramentas/chutador_de_forma.py
"""

import json
import math
import random
import re
from collections import Counter
from pathlib import Path

from ferramentas.validar_modulo import (
    RAIZ,
    RE_DIGITO,
    RE_NEGACAO,
    _unicidade_estrutural,
    ids_publicados,
    validar,
)

RE_ABSOLUTO = re.compile(r"\bsempre\b|\bnunca\b|\bqualquer\b|\btodo\w*\b", re.I)


def _unica(alternativas, padrao, quer_marca):
    """Índice da única alternativa cuja presença/ausência da marca destoa das
    outras três. `quer_marca=True` procura a única COM a marca; False, a
    única SEM. Abstém (None) se não houver exatamente uma nessa condição."""
    marcas = [bool(padrao.search(a)) for a in alternativas]
    n = sum(marcas)
    if quer_marca and n == 1:
        return marcas.index(True)
    if not quer_marca and len(alternativas) - n == 1:
        return marcas.index(False)
    return None


def mais_longa(alternativas):
    return max(range(len(alternativas)), key=lambda i: len(alternativas[i]))


def unica_com_negacao(alternativas):
    return _unica(alternativas, RE_NEGACAO, True)


def unica_sem_negacao(alternativas):
    return _unica(alternativas, RE_NEGACAO, False)


def unica_com_digito(alternativas):
    return _unica(alternativas, RE_DIGITO, True)


def unica_sem_digito(alternativas):
    return _unica(alternativas, RE_DIGITO, False)


def evita_absoluto(alternativas):
    restantes = [i for i, a in enumerate(alternativas) if not RE_ABSOLUTO.search(a)]
    if not restantes:
        return None
    return max(restantes, key=lambda i: len(alternativas[i]))


ESTRATEGIAS = {
    "mais_longa": mais_longa,
    "unica_com_negacao": unica_com_negacao,
    "unica_sem_negacao": unica_sem_negacao,
    "unica_com_digito": unica_com_digito,
    "unica_sem_digito": unica_sem_digito,
    "evita_absoluto": evita_absoluto,
}


# --------------------------------------------------------------------------
# Montagem das populações e medição — não faz parte do "chutador" em si, é
# infraestrutura de medição que PODE ler `correta` (só pra conferir acerto).
# --------------------------------------------------------------------------

SEED_GRUPO_B = 20260831  # data da medição original da regra 7, documentada no PROGRESS.md


def _carregar_modulos():
    return {p: json.loads(p.read_text(encoding="utf-8")) for p in sorted((RAIZ / "data" / "modulos").glob("*.json"))}


def _questoes_mc(dados):
    return [q for q in dados.get("questoes", []) if "alternativas" in q]


def montar_populacoes():
    arquivos = _carregar_modulos()
    ids = ids_publicados()

    grupo_a = []  # (modulo, questao) que disparam a regra 7 hoje
    for caminho, dados in arquivos.items():
        _, _, avisos = validar(caminho, ids)
        disparadas = {a.split(":")[0] for a in avisos if "entre as quatro" in a}
        for q in _questoes_mc(dados):
            if q["id"] in disparadas:
                grupo_a.append((dados["id"], q))

    limpos_por_modulo = {}
    for dados in arquivos.values():
        limpos_por_modulo[dados["id"]] = [
            q for q in _questoes_mc(dados) if not _unicidade_estrutural(q["alternativas"], q["correta"])
        ]

    contagem_a = Counter(m for m, _ in grupo_a)
    random.seed(SEED_GRUPO_B)
    grupo_b = []
    for modulo, n in contagem_a.items():
        pool = limpos_por_modulo[modulo]
        grupo_b.extend((modulo, q) for q in random.sample(pool, min(n, len(pool))))

    grupo_c = [(dados["id"], q) for dados in arquivos.values() for q in _questoes_mc(dados)]

    return {"A": grupo_a, "B": grupo_b, "C": grupo_c}


def wilson(acertos, aplicacoes, z=1.96):
    """Intervalo de confiança de Wilson para uma proporção — melhor que a
    aproximação normal quando a amostra é pequena (eixo dígito, n=10)."""
    if aplicacoes == 0:
        return None
    p = acertos / aplicacoes
    denom = 1 + z * z / aplicacoes
    centro = p + z * z / (2 * aplicacoes)
    margem = z * math.sqrt(p * (1 - p) / aplicacoes + z * z / (4 * aplicacoes * aplicacoes))
    return ((centro - margem) / denom, (centro + margem) / denom)


def medir(estrategia, questoes):
    acertos = aplicacoes = abstencoes = 0
    for _, q in questoes:
        palpite = estrategia(q["alternativas"])
        if palpite is None:
            abstencoes += 1
        else:
            aplicacoes += 1
            if palpite == q["correta"]:
                acertos += 1
    return {"acertos": acertos, "aplicacoes": aplicacoes, "abstencoes": abstencoes, "total": len(questoes)}


def relatorio():
    populacoes = montar_populacoes()
    linhas = [f"populacao A: {len(populacoes['A'])} questoes (regra 7 dispara)",
              f"populacao B: {len(populacoes['B'])} questoes (controle, sem marca)",
              f"populacao C: {len(populacoes['C'])} questoes (todas as MC do corpus)",
              ""]
    resultados = {}
    for nome_estrat, fn in ESTRATEGIAS.items():
        for pop, questoes in populacoes.items():
            r = medir(fn, questoes)
            resultados[(nome_estrat, pop)] = r
            taxa = r["acertos"] / r["aplicacoes"] if r["aplicacoes"] else None
            ic = wilson(r["acertos"], r["aplicacoes"])
            taxa_str = f"{100*taxa:5.1f}%" if taxa is not None else "  n/a "
            ic_str = f"[{100*ic[0]:.1f}%, {100*ic[1]:.1f}%]" if ic else "sem aplicação"
            linhas.append(
                f"{nome_estrat:22} pop={pop}  acertos={r['acertos']:3}/{r['aplicacoes']:3}"
                f"  abstencoes={r['abstencoes']:3}/{r['total']:3}  taxa={taxa_str}  IC95%={ic_str}"
            )
        linhas.append("")
    return "\n".join(linhas), resultados


if __name__ == "__main__":
    texto, _ = relatorio()
    print(texto)
