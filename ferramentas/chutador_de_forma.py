"""Chutador burro: estratégias de forma pura para responder múltipla escolha.

Nasceu pra medir se a regra 7 do validador (unicidade estrutural — dígito,
negação) media vazamento real. Não mediu: a taxa de acerto no corpus inteiro
(a única população não-circular — ver `relatorio_regra7_chutador.md`) ficou
em 27% e 17,8%, contra 25% de acaso. A regra 7 foi removida em 01/09/2026.

O que sobrou tem uso permanente: `mais_longa` e `evita_absoluto` SÃO sinal
real — 41% e 43% no corpus inteiro, quase o dobro do acaso — e correspondem
ao viés de comprimento que o PROGRESS.md já rastreia à mão desde antes desta
ferramenta existir. Este arquivo virou o portão de qualidade desse viés:
mede, por módulo, a taxa com que "escolher a alternativa mais longa, sem
ler nada" acerta a resposta certa.

Cada estratégia só recebe `alternativas` (lista de textos) — nunca o campo
`correta`, a explicação, as dicas ou as tags. Quando a heurística não se
aplica, ela se abstém (devolve None) em vez de chutar ao acaso — abstenção
não conta como acerto nem como erro.

Uso:
    python -m ferramentas.chutador_de_forma                    # todos os módulos publicados, pior pro melhor
    python -m ferramentas.chutador_de_forma data/modulos/X.json  # só os arquivos dados
"""

import json
import math
import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent

RE_DIGITO = re.compile(r"\d")
RE_NEGACAO = re.compile(r"\bnão\b|\bnunca\b|\bnenhum\w*\b", re.I)
RE_ABSOLUTO = re.compile(r"\bsempre\b|\bnunca\b|\bqualquer\b|\btodo\w*\b", re.I)

# Teto do portão de qualidade. Escolhido a partir da distribuição real dos 27
# módulos publicados (ver `python -m ferramentas.chutador_de_forma`): mediana
# 43,8%, quartis 28,1%/56,2%, acaso 25%. Não uso a mediana — reprovaria metade
# dos módulos por definição, o que não separa nada; a mediana só diz "acima da
# metade pior", não "sinal real".
#
# O corte em 40% não é a mediana nem um palpite: é o mesmo número que
# MAX_CORRETA_MAIS_LONGA já usa em `validar_modulo.py`, e os dois concordam
# nos 27 módulos por acaso não é — testei com o critério estatístico
# (intervalo de Wilson 95% da taxa de mais_longa contra os 25% de acaso;
# módulo "tem sinal" quando o limite inferior do IC passa de 25%) e ele bate
# EXATAMENTE nos mesmos 15 de 27 módulos que 40% separa, com a mesma fronteira
# entre 0.3 (41,9%) e 1.5 (35,5%). Dois critérios independentes convergindo no
# mesmo corte é evidência melhor que qualquer um dos dois sozinho.
TETO_MAIS_LONGA = 0.40

# Mesmo portão, segundo eixo: "evita_absoluto" (rejeitar a alternativa com
# sempre/nunca/qualquer/todo e escolher a mais longa entre as que sobram) é
# sinal real, não ruído — medido contra os 29 módulos publicados em
# 02/09/2026: mediana 35,5%, e o mesmo critério estatístico independente
# (limite inferior do IC95 de Wilson passa de 25% de acaso) converge
# EXATAMENTE no corte de 40%: o último módulo com sinal (4.1, 40,6%) fica
# acima, o primeiro sem sinal (4.6, 38,7%) fica abaixo — a mesma coincidência
# de dois critérios independentes que já validou o teto de mais_longa.
TETO_EVITA_ABSOLUTO = 0.40


def _unica(alternativas, padrao, quer_marca):
    marcas = [bool(padrao.search(a)) for a in alternativas]
    n = sum(marcas)
    if quer_marca and n == 1:
        return marcas.index(True)
    if not quer_marca and len(alternativas) - n == 1:
        return marcas.index(False)
    return None


def mais_longa(alternativas):
    return max(range(len(alternativas)), key=lambda i: len(alternativas[i]))


def mais_curta(alternativas):
    """Espelho de mais_longa. Cortar demais a correta não elimina o viés de
    comprimento — inverte ele: se a correta virar a mais curta com frequência
    acima do acaso, "escolher a mais curta" passa a ser o mesmo atalho por
    outro lado. O alvo do portão é a correta ficar no meio da distribuição
    dos distratores, não em nenhum dos dois extremos."""
    return min(range(len(alternativas)), key=lambda i: len(alternativas[i]))


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
    "mais_curta": mais_curta,
    "unica_com_negacao": unica_com_negacao,
    "unica_sem_negacao": unica_sem_negacao,
    "unica_com_digito": unica_com_digito,
    "unica_sem_digito": unica_sem_digito,
    "evita_absoluto": evita_absoluto,
}


def wilson(acertos, aplicacoes, z=1.96):
    """Intervalo de confiança de Wilson para uma proporção — melhor que a
    aproximação normal quando a amostra é pequena."""
    if aplicacoes == 0:
        return None
    p = acertos / aplicacoes
    denom = 1 + z * z / aplicacoes
    centro = p + z * z / (2 * aplicacoes)
    margem = z * math.sqrt(p * (1 - p) / aplicacoes + z * z / (4 * aplicacoes * aplicacoes))
    return ((centro - margem) / denom, (centro + margem) / denom)


def medir(estrategia, questoes):
    """`questoes` é uma lista de dicts de questão (precisam de 'alternativas' e 'correta')."""
    acertos = aplicacoes = abstencoes = 0
    for q in questoes:
        palpite = estrategia(q["alternativas"])
        if palpite is None:
            abstencoes += 1
        else:
            aplicacoes += 1
            if palpite == q["correta"]:
                acertos += 1
    return {"acertos": acertos, "aplicacoes": aplicacoes, "abstencoes": abstencoes, "total": len(questoes)}


def _questoes_mc(dados):
    return [q for q in dados.get("questoes", []) if "alternativas" in q]


def checar_modulo(caminho):
    """Portão de qualidade de forma: taxa de mais_longa (viés de comprimento),
    mais_curta (o mesmo viés no extremo oposto) e evita_absoluto (rejeitar a
    alternativa com sempre/nunca/qualquer/todo) de um módulo. Devolve
    (dados, resultado_mais_longa, resultado_mais_curta, resultado_evita_absoluto)."""
    dados = json.loads(Path(caminho).read_text(encoding="utf-8"))
    questoes = _questoes_mc(dados)
    return (dados, medir(mais_longa, questoes), medir(mais_curta, questoes),
            medir(evita_absoluto, questoes))


def main():
    alvos = [Path(a) for a in sys.argv[1:]] or sorted((RAIZ / "data" / "modulos").glob("*.json"))

    linhas = []
    for caminho in alvos:
        dados, r_longa, r_curta, r_absoluto = checar_modulo(caminho)
        taxa = r_longa["acertos"] / r_longa["aplicacoes"] if r_longa["aplicacoes"] else 0.0
        linhas.append((taxa, dados.get("id", "?"), caminho.name, r_longa, r_curta, r_absoluto))

    linhas.sort(key=lambda x: -x[0])  # pior (taxa mais alta) primeiro

    print(f"{'modulo':10} {'mais_longa':>12} {'mais_curta':>12} {'evita_absoluto':>16}   {'teto':>6}  status")
    reprovados = 0
    for taxa, mod_id, nome, r_longa, r_curta, r_absoluto in linhas:
        taxa_curta = r_curta["acertos"] / r_curta["aplicacoes"] if r_curta["aplicacoes"] else 0.0
        taxa_absoluto = r_absoluto["acertos"] / r_absoluto["aplicacoes"] if r_absoluto["aplicacoes"] else 0.0
        acima = taxa > TETO_MAIS_LONGA or taxa_absoluto > TETO_EVITA_ABSOLUTO
        reprovados += acima
        status = "ACIMA DO TETO" if acima else "ok"
        print(f"{mod_id:10} {taxa:11.1%} ({r_longa['acertos']:2}/{r_longa['aplicacoes']:2})"
              f"  {taxa_curta:10.1%} ({r_curta['acertos']:2}/{r_curta['aplicacoes']:2})"
              f"  {taxa_absoluto:14.1%} ({r_absoluto['acertos']:2}/{r_absoluto['aplicacoes']:2})"
              f"  {TETO_MAIS_LONGA:5.0%}  {status}")

    print(f"\n{reprovados}/{len(linhas)} módulo(s) acima do teto de {TETO_MAIS_LONGA:.0%} "
          f"(mais_longa ou evita_absoluto)")


if __name__ == "__main__":
    main()
