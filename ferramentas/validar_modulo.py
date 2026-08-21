"""Valida um módulo de conteúdo antes de ele entrar no app.

Uso:
    python ferramentas/validar_modulo.py data/modulos/02-05-autenticacao-e-identidade.json
    python ferramentas/validar_modulo.py --esqueleto exemplo/modulo-minimo.json

Roda o esquema de `app/content.py` mais as regras de qualidade de
`tests/test_qualidade_conteudo.py`, e ainda algumas convenções que os testes não
cobrem: bloco de teoria com analogia e erro comum, tag fora do padrão, enunciado
repetido, dado pessoal em artefato, endereço de terceiro em módulo ofensivo e
payload pronto para copiar e colar.

`--esqueleto` dispensa as regras de quantidade (35 a 60 questões, 4 a 8 blocos de
teoria). Serve para conferir a forma de um arquivo de exemplo ou de um módulo
ainda pela metade.

Sai com código 1 se houver falha. Aviso não reprova.
"""

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ))

from app import content  # noqa: E402

MIN_QUESTOES, MAX_QUESTOES, MIN_TIPOS = 35, 60, 4
MIN_TEORIA, MAX_TEORIA = 4, content.MAX_BLOCOS_TEORIA

# Dado pessoal não entra em artefato: saída real de ferramenta se anonimiza antes.
# O alvo aqui é o vazamento real — caminho de usuário, SID de conta, e-mail em
# provedor de verdade. Domínio fictício (contoso, example, .local) é o que se
# espera ver em exemplo, e não dispara nada.
PESSOAL = re.compile(
    r"C:\\Users\\[A-Za-z0-9._-]+"            # caminho com nome de usuário do Windows
    r"|S-1-(?:5-21|11-96)-[\d-]{10,}"         # SID de conta real
    r"|[\w.+-]+@(?:gmail|hotmail|outlook|live|yahoo|icloud|proton(?:mail)?|"
    r"bol|uol|terra)\.[\w.]{2,}",             # e-mail em provedor real
    re.I)

# Módulo ofensivo só aponta para alvo próprio: localhost, RFC 1918, link-local ou
# faixa de documentação (RFC 5737). Endereço fora disso vira aviso para revisão.
IP = re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b")
IP_PERMITIDO = re.compile(
    r"^(127\.|10\.|192\.168\.|172\.(1[6-9]|2\d|3[01])\.|169\.254\.|"
    r"192\.0\.2\.|198\.51\.100\.|203\.0\.113\.|0\.0\.0\.0|255\.)")

# Ensina-se o mecanismo, não a munição.
PAYLOAD = re.compile(
    r"' *OR *'1' *= *'1|<script>alert|; *DROP +TABLE|UNION +SELECT +.*FROM|"
    r"nc +-e +/bin|/bin/sh +-i|powershell +-enc|msfvenom|sqlmap +-u +http", re.I)


def ids_publicados():
    pasta = RAIZ / "data" / "modulos"
    return {json.loads(p.read_text(encoding="utf-8"))["id"] for p in pasta.glob("*.json")}


def validar(caminho, ids_conhecidos, esqueleto=False):
    falhas, avisos = [], []
    dados = json.loads(Path(caminho).read_text(encoding="utf-8"))

    try:
        content.validar_modulo(dados, Path(caminho).name)
    except content.ErroDeConteudo as erro:
        return dados, [f"ESQUEMA: {erro}"], avisos

    questoes, teoria = dados["questoes"], dados["teoria"]

    if not esqueleto:
        if not MIN_QUESTOES <= len(questoes) <= MAX_QUESTOES:
            falhas.append(f"{len(questoes)} questões; o esperado é de {MIN_QUESTOES} a {MAX_QUESTOES}")
        if not MIN_TEORIA <= len(teoria) <= MAX_TEORIA:
            falhas.append(f"{len(teoria)} blocos de teoria; o esperado é de {MIN_TEORIA} a {MAX_TEORIA}")
        tipos = {q["tipo"] for q in questoes}
        if len(tipos) < MIN_TIPOS:
            falhas.append(f"só {len(tipos)} tipos de questão: {sorted(tipos)}")

    for bloco in teoria:
        for campo in ("analogia", "erro_comum"):
            if not bloco.get(campo, "").strip():
                falhas.append(f"{bloco['id']}: bloco de teoria sem '{campo}' (convenção do projeto)")
        if not bloco["id"].startswith(dados["id"] + "."):
            falhas.append(f"{bloco['id']}: id não começa com o id do módulo")

    for pre in dados["pre_requisitos"]:
        if pre not in ids_conhecidos:
            falhas.append(f"pré-requisito '{pre}' não existe em data/modulos/")

    repetidos = Counter(q["enunciado"].strip().lower() for q in questoes)
    for texto, n in repetidos.items():
        if n > 1:
            falhas.append(f"enunciado repetido {n}x: {texto[:60]}")

    for q in questoes:
        ctx = q["id"]
        if not ctx.startswith(dados["id"] + "."):
            falhas.append(f"{ctx}: id não começa com o id do módulo")
        if len(q["dicas"]) < 2:
            falhas.append(f"{ctx}: menos de 2 dicas")
        elif len(q["dicas"]) != 3:
            avisos.append(f"{ctx}: {len(q['dicas'])} dicas; a convenção do projeto é 3")
        for campo in ("pergunta_socratica", "explicacao", "fonte"):
            if not q[campo].strip():
                falhas.append(f"{ctx}: campo '{campo}' vazio")
        if not q["pergunta_socratica"].startswith("Antes de conferir"):
            avisos.append(f"{ctx}: pergunta socrática fora do padrão 'Antes de conferir:'")

        alternativas = q.get("alternativas")
        if alternativas:
            if len(alternativas) != 4:
                avisos.append(f"{ctx}: {len(alternativas)} alternativas; a convenção do projeto é 4")
            if len({a for a in alternativas if alternativas.count(a) > 1}):
                falhas.append(f"{ctx}: alternativas repetidas")
            certa = alternativas[q["correta"]]
            outras = [a for i, a in enumerate(alternativas) if i != q["correta"]]
            if outras and len(certa) > 1.6 * max(len(a) for a in outras):
                avisos.append(f"{ctx}: alternativa correta muito mais longa que as outras")

        if q["tipo"] == "pareamento":
            direita = [par[1] for par in q["pares"]]
            if len(set(direita)) != len(direita):
                falhas.append(f"{ctx}: dois pares com o mesmo lado direito — pareamento ambíguo")
        if q["tipo"] == "ordenacao" and len(q["itens"]) < 4:
            avisos.append(f"{ctx}: ordenação com menos de 4 itens")

        for tag in q["tags"]:
            if tag != tag.lower() or " " in tag:
                falhas.append(f"{ctx}: tag fora do padrão minúsculo-com-hífen: {tag}")

    bruto = json.dumps(dados, ensure_ascii=False)
    achado = PESSOAL.search(bruto)
    if achado:
        falhas.append(f"dado pessoal no conteúdo: {achado.group(0)!r} — anonimize o artefato")
    achado = PAYLOAD.search(bruto)
    if achado:
        falhas.append(f"payload pronto para copiar e colar: {achado.group(0)!r}")
    for endereco in sorted(set(IP.findall(bruto))):
        if not any(len(octeto) == 3 for octeto in endereco.split(".")):
            continue  # "Sec. 3.4.4.3" tem forma de endereço e é número de seção
        if not IP_PERMITIDO.match(endereco):
            avisos.append(f"endereço fora de localhost, RFC 1918 e RFC 5737: {endereco}")

    return dados, falhas, avisos


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("arquivos", nargs="+", help="um ou mais módulos .json")
    parser.add_argument("--esqueleto", action="store_true",
                        help="não cobra as regras de quantidade")
    args = parser.parse_args()

    alvos = [Path(a) for a in args.arquivos]
    ids = ids_publicados() | {json.loads(a.read_text(encoding="utf-8"))["id"] for a in alvos}

    total = 0
    for alvo in alvos:
        dados, falhas, avisos = validar(alvo, ids, args.esqueleto)
        questoes = dados.get("questoes", [])
        print(f"--- {alvo.name} (id {dados.get('id')})")
        print(f"    questões={len(questoes)} teoria={len(dados.get('teoria', []))} "
              f"objetivos={len(dados.get('objetivos', []))}")
        print(f"    tipos={dict(Counter(q['tipo'] for q in questoes))}")
        for aviso in avisos:
            print(f"    aviso: {aviso}")
        for falha in falhas:
            print(f"    FALHA: {falha}")
        print("    RESULTADO:", "OK" if not falhas else f"{len(falhas)} falha(s)")
        total += len(falhas)

    sys.exit(1 if total else 0)


if __name__ == "__main__":
    main()
