"""Medidor de molde de dica: maior família de questões cujas dicas começam
com as mesmas N palavras, por módulo.

Nasceu do achado da revisão adversarial do 3.5: `dicas[2]` abria com a mesma
frase ("Só uma alternativa... sem inventar...") em 28 de 28 questões de
múltipla escolha, sem exceção. É a quarta variante desta família de defeito
nesta série (frase de autorrejeição no 4.7, qualificador absolutista no 4.8,
hedge solto no 3.4, abertura de dica agora) — nenhuma pega por regra
automática, só por leitura. Seguindo a lição da regra 7 (seção 7 do
PROGRESS.md: heurística só vira código depois de medida contra o corpus
inteiro, não contra o caso que a inspirou), esta ferramenta MEDE — não
corrige e não é, por si só, um portão de qualidade.

Escolha de N = 5: uma dica progressiva típica deste corpus abre com uma
oração curta (4 a 8 palavras) antes de divergir para o conteúdo específico
da questão — "Só uma alternativa..." tem 3 palavras antes de ramificar,
"Antes de o banco processar..." tem 5. N=5 pega repetição de frase inteira
com folga estatística (5 palavras em comum ao acaso, num vocabulário técnico
de milhares de termos, é praticamente impossível) sem exigir a frase
INTEIRA idêntica, o que sub-contaria paráfrases que só mudam a cauda. N
menor (3) pega demais: conectivos comuns em português técnico ("Antes de
verificar se...", "O que diferencia...") colidem por acaso, não por molde.
N maior (8) exige quase a sentença completa e perde variantes que trocam só
o fim. N=5 é o meio que ficou, não o único defensável — outro N teria outra
sensibilidade, e é por isso que esta ferramenta reporta o número bruto, não
decide um teto sozinha.

Cada dica ocupa um papel pedagógico diferente (dicas[0] é a mais vaga, [2] a
mais específica), então a família é contada DENTRO de cada índice — misturar
os três inflaria falsos positivos (dicas[0] de questões diferentes tendem a
ser mais genéricas por design).

Uso:
    python -m ferramentas.medidor_molde_dica                    # todos os módulos publicados, pior pro melhor
    python -m ferramentas.medidor_molde_dica data/modulos/X.json  # só os arquivos dados
"""

import json
import re
import sys
from collections import Counter
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent

N_PALAVRAS = 5

RE_PALAVRA = re.compile(r"[\wÀ-ÿ]+", re.UNICODE)


def _prefixo(texto, n=N_PALAVRAS):
    palavras = RE_PALAVRA.findall(texto.lower())
    if len(palavras) < n:
        return None
    return tuple(palavras[:n])


def maior_familia(dicas_dessa_posicao):
    """`dicas_dessa_posicao` é uma lista de textos (uma dica por questão, mesmo
    índice). Devolve (tamanho_da_maior_familia, prefixo, total_com_prefixo)."""
    contagem = Counter()
    for texto in dicas_dessa_posicao:
        prefixo = _prefixo(texto)
        if prefixo is not None:
            contagem[prefixo] += 1
    if not contagem:
        return 0, None, 0
    prefixo, tamanho = contagem.most_common(1)[0]
    return tamanho, prefixo, len(dicas_dessa_posicao)


def medir_modulo(caminho):
    """Devolve lista de 3 dicts, um por índice de dica (0, 1, 2):
    {'indice', 'tamanho', 'prefixo', 'total', 'fracao'}."""
    dados = json.loads(Path(caminho).read_text(encoding="utf-8"))
    questoes = [q for q in dados.get("questoes", []) if len(q.get("dicas", [])) == 3]
    resultado = []
    for indice in range(3):
        textos = [q["dicas"][indice] for q in questoes]
        tamanho, prefixo, total = maior_familia(textos)
        fracao = tamanho / total if total else 0.0
        resultado.append({
            "indice": indice, "tamanho": tamanho, "prefixo": prefixo,
            "total": total, "fracao": fracao,
        })
    return dados.get("id", "?"), resultado


def main():
    alvos = [Path(a) for a in sys.argv[1:]] or sorted((RAIZ / "data" / "modulos").glob("*.json"))

    linhas = []
    for caminho in alvos:
        mod_id, resultado = medir_modulo(caminho)
        pior = max(resultado, key=lambda r: r["fracao"])
        linhas.append((pior["fracao"], mod_id, caminho.name, pior, resultado))

    linhas.sort(key=lambda x: -x[0])  # pior (fração mais alta) primeiro

    print(f"{'modulo':10} {'pior_indice':>11} {'familia':>9} {'fracao':>8}   prefixo (5 palavras)")
    for fracao, mod_id, nome, pior, resultado in linhas:
        prefixo_txt = " ".join(pior["prefixo"]) if pior["prefixo"] else "(sem molde de 5+ palavras)"
        print(f"{mod_id:10} {'dicas[' + str(pior['indice']) + ']':>11} "
              f"{pior['tamanho']:3}/{pior['total']:<4} {fracao:7.1%}   {prefixo_txt}")

    print()
    print("Mediana da pior fração por módulo:", end=" ")
    fracoes = sorted(l[0] for l in linhas)
    meio = len(fracoes) // 2
    mediana = fracoes[meio] if len(fracoes) % 2 else (fracoes[meio - 1] + fracoes[meio]) / 2
    print(f"{mediana:.1%}")


if __name__ == "__main__":
    main()
