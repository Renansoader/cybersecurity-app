"""Valida um módulo de conteúdo antes de ele entrar no app.

Uso:
    python ferramentas/validar_modulo.py data/modulos/02-05-autenticacao-e-identidade.json
    python ferramentas/validar_modulo.py --esqueleto exemplo/modulo-minimo.json

Roda o esquema de `app/content.py` mais as regras de qualidade de
`tests/test_qualidade_conteudo.py`, e ainda algumas convenções que os testes não
cobrem: bloco de teoria com analogia e erro comum, tag fora do padrão, enunciado
repetido, dado pessoal em artefato, endereço de terceiro em módulo ofensivo e
payload pronto para copiar e colar.

Roda também as quatro regras de gabarito entregue de graça — dica que reescreve a
alternativa correta, artefato que carrega a resposta, enunciado que afirma a
resposta e distrator que é o gabarito de outra questão. Elas saíram de defeitos
reais achados à mão na revisão do nível 3; a seção correspondente do README
explica o cálculo e os limites.

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

# Comprimento da alternativa correta. A régua que vale é de DISTRIBUIÇÃO, e não de
# caso isolado: "escolha a mais longa" é uma heurística que o aluno aplica sem ler,
# e ela não precisa de nenhum outlier para funcionar — basta a correta ser a mais
# longa com frequência. Mesma forma da trava de posição em test_pedagogy.py, que
# exige que a correta não caia mais de 40% das vezes na mesma linha.
# A régua de razão fica como aviso secundário, para o desequilíbrio isolado: 3x o
# maior distrator não acusa nada no corpus de hoje, por isso o corte está em 2,5x.
MAX_CORRETA_MAIS_LONGA = 0.40
LIMIAR_CORRETA_LONGA = 2.5
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

# --------------------------------------------------------------------------
# Gabarito entregue de graça: quatro padrões que a revisão do nível 3 pegou à
# mão, 23 vezes em três módulos. Todos comparam texto: medem quanto do
# vocabulário da alternativa correta reaparece onde não devia.
#
# LIMITE CONHECIDO: isto pega ECO LITERAL, não paráfrase. Uma dica que diz
# "o nome do meio indica mistura" para uma correta que diz "a combinação das
# duas abordagens" não compartilha palavra nenhuma e passa batido. A leitura
# humana continua sendo a rede que pega esses casos.
# --------------------------------------------------------------------------

VAZIO = frozenset()

# Palavra curta e palavra de ligação não contam como evidência de eco.
IRRELEVANTES = frozenset("""
    para pelo pela pelos pelas como quando onde porque porem entao ainda apenas
    tambem sobre entre cada todo toda todos todas outro outra outros outras
    mesmo mesma mesmos mesmas isso isto aquilo esse essa esses essas este esta
    estes estas seja sejam sendo esta estao tem tinha havia haver pode podem
    poderia deve devem precisa precisam faz fazem fazer feito feita sao nao sim
    que qual quais quanto quantos com sem por dos das dum duma numa num nos nas
    uma uns umas ele ela eles elas voce quem qualquer alguma algum alguns algumas
    nenhum nenhuma depois antes durante enquanto porem contudo assim logo entao
    caso vez vezes parte partes forma formas modo modos coisa coisas ponto pontos
    dado dados valor valores usar usa usam usado usada tipo tipos item itens
""".split())


def _tokens(texto):
    """Palavras significativas de um texto: sem acento, com 4 letras ou mais."""
    if not texto:
        return VAZIO
    texto = texto.lower()
    for de, para in (("á", "a"), ("à", "a"), ("â", "a"), ("ã", "a"), ("é", "e"),
                     ("ê", "e"), ("í", "i"), ("ó", "o"), ("ô", "o"), ("õ", "o"),
                     ("ú", "u"), ("ç", "c")):
        texto = texto.replace(de, para)
    palavras = re.findall(r"[a-z0-9][a-z0-9-]{3,}", texto)
    return frozenset(p for p in palavras if p not in IRRELEVANTES)


def _cobertura(fonte, alvo):
    """Fração do vocabulário de `alvo` que reaparece em `fonte`."""
    alvo = _tokens(alvo)
    if not alvo:
        return 0.0
    return len(_tokens(fonte) & alvo) / len(alvo)


def _distintivos(questao, descontar_enunciado=True):
    """As palavras que SÓ a alternativa correta tem.

    É aqui que mora o gabarito. Palavra que também aparece num distrator é
    vocabulário do assunto e não distingue nada. Para dica e artefato descontamos
    também o enunciado, porque palavra que já está na pergunta não foi entregue
    por ninguém; para avaliar o próprio enunciado, não.
    """
    alternativas = questao.get("alternativas")
    if not alternativas:
        return VAZIO
    correta = _tokens(alternativas[questao["correta"]])
    for i, alternativa in enumerate(alternativas):
        if i != questao["correta"]:
            correta = correta - _tokens(alternativa)
    if descontar_enunciado:
        correta = correta - _tokens(questao["enunciado"])
    return correta


def _eco(fonte, questao, minimo, palavras_minimas, descontar_enunciado=True):
    """Mede quanto do vocabulário EXCLUSIVO da alternativa correta está em `fonte`.

    Devolve (fração, palavras) quando passa dos dois limites, senão None. A
    fração sozinha dispara com uma coincidência em alternativa curta, e a
    contagem sozinha dispara em alternativa longa — por isso os dois.
    """
    distintivos = _distintivos(questao, descontar_enunciado)
    if not distintivos:
        return None
    achadas = _tokens(fonte) & distintivos
    fracao = len(achadas) / len(distintivos)
    if fracao >= minimo and len(achadas) >= palavras_minimas:
        return fracao, sorted(achadas)
    return None


# Calibrados contra os três módulos do nível 3 antes da revisão, onde os casos
# que a leitura humana pegou estão marcados, e depois conferidos à mão nos 21
# módulos publicados: dos disparos amostrados ali, a maioria era vazamento real
# que nunca tinha sido auditado. Abaixar mais inunda de coincidência; subir mais
# deixa passar eco óbvio.
LIMIAR_DICA, PALAVRAS_DICA = 0.30, 2
LIMIAR_ENUNCIADO, PALAVRAS_ENUNCIADO = 0.35, 3
LIMIAR_ARTEFATO, PALAVRAS_ARTEFATO = 0.35, 3
LIMIAR_TRECHO = 0.70  # caça ao erro: o gabarito cita o trecho por construção
LIMIAR_DISTRATOR = 0.72
LIMIAR_ENUNCIADO_IGUAL = 0.40  # só acusa quando as duas questões perguntam o mesmo
LIMIAR_GABARITO_IGUAL = 0.55   # duas questões ensinando a mesma coisa, aqui ou em outro módulo

# Regra 6: a fôrma "Pergunte ⟨a pergunta cuja única resposta é o gabarito⟩".
# É regra de forma, não de conteúdo: não mede eco nenhum e não sabe se aquela
# dica específica entrega o gabarito. Existe porque o molde reincidiu módulo
# após módulo mesmo com a proibição escrita no encargo do autor, e porque a
# paráfrase que ele produz é justamente a que as regras 1 a 5 não alcançam.
# Proibir a fôrma é o que sobrou de acionável: dica boa aponta onde olhar.
# Pega o molde no começo da dica e no começo de qualquer frase dentro dela.
MOLDE_PERGUNTE = re.compile(
    r"(?:^|(?<=[.!?;]))\s*(?:se\s+)?pergunt[ae](?:-se)?\b"
    r"|(?:^|(?<=[.!?;]))\s*(?:questione|indague)\b", re.I)


ACEITOS = json.loads((RAIZ / "ferramentas" / "avisos_aceitos.json").read_text(encoding="utf-8"))


def _aceito(qid, rotulo):
    """Caso já analisado e aceito como legítimo, com justificativa no arquivo."""
    return rotulo in ACEITOS.get(qid, {})


def achar_gabarito_entregue(dados, avisos):
    """As quatro regras de gabarito entregue. Só produz aviso, nunca falha.

    Caso listado em ferramentas/avisos_aceitos.json não vira aviso: ele já foi
    lido, decidido e justificado ali.
    """
    questoes = dados["questoes"]

    # 6. dica no molde "Pergunte ⟨…⟩". Vale para todo tipo de questão, e não só
    # para as que têm alternativas: pareamento e ordenação também têm dicas.
    for questao in questoes:
        for n, dica in enumerate(questao["dicas"], start=1):
            achado = MOLDE_PERGUNTE.search(dica)
            if achado and not _aceito(questao["id"], f"molde da dica {n}"):
                avisos.append(
                    f"{questao['id']}: a dica {n} usa o molde {achado.group(0).strip()!r} — formular "
                    f"a pergunta cuja única resposta é o gabarito não é estreitar o raciocínio; "
                    f"aponte onde olhar")

    for questao in questoes:
        ctx = questao["id"]
        alternativas = questao.get("alternativas")
        if not alternativas:
            continue
        correta = alternativas[questao["correta"]]

        # 1. dica que reescreve a alternativa correta
        for n, dica in enumerate(questao["dicas"], start=1):
            medida = _eco(dica, questao, LIMIAR_DICA, PALAVRAS_DICA)
            if medida and not _aceito(ctx, f"dica {n}"):
                avisos.append(
                    f"{ctx}: a dica {n} traz {medida[0]:.0%} das palavras que só a alternativa "
                    f"correta tem ({', '.join(medida[1])}) — a dica deve estreitar o "
                    f"raciocínio, não reescrever o gabarito")

        # 2. artefato ou trecho que carrega a resposta.
        # Em caça ao erro o gabarito aponta para um item do próprio trecho, então
        # alguma sobreposição é da natureza do tipo: ali a régua sobe.
        for campo in ("artefato", "trecho"):
            texto = questao.get(campo)
            if not texto:
                continue
            limiar = LIMIAR_TRECHO if questao["tipo"] == "caca_erro" else LIMIAR_ARTEFATO
            medida = _eco(texto, questao, limiar, PALAVRAS_ARTEFATO)
            if medida and not _aceito(ctx, campo):
                avisos.append(
                    f"{ctx}: o campo '{campo}' traz {medida[0]:.0%} das palavras que só a "
                    f"alternativa correta tem ({', '.join(medida[1])}) — o aluno lê a "
                    f"resposta antes de responder")

        # 3. enunciado que afirma a própria resposta
        medida = _eco(questao["enunciado"], questao, LIMIAR_ENUNCIADO,
                      PALAVRAS_ENUNCIADO, descontar_enunciado=False)
        if medida and not _aceito(ctx, "enunciado"):
            avisos.append(
                f"{ctx}: o enunciado traz {medida[0]:.0%} das palavras que só a alternativa "
                f"correta tem ({', '.join(medida[1])}) — confira se ele não afirma a "
                f"resposta antes de perguntar")

    # 5. duas questões com a mesma resposta certa, aqui ou em outro módulo.
    # Foi a duplicação que a revisão do nível 3 mais encontrou à mão, e a regra 4
    # não a alcança: ela nasce de paráfrase, não de cópia.
    publicadas = []
    pasta = RAIZ / "data" / "modulos"
    for caminho in sorted(pasta.glob("*.json")):
        outro = json.loads(caminho.read_text(encoding="utf-8"))
        if outro["id"] == dados["id"]:
            continue
        for x in outro["questoes"]:
            if x.get("alternativas"):
                publicadas.append((x["id"], x["alternativas"][x["correta"]]))
    for questao in questoes:
        if not questao.get("alternativas"):
            continue
        certa = questao["alternativas"][questao["correta"]]
        vizinhas = publicadas + [(x["id"], x["alternativas"][x["correta"]])
                                 for x in questoes
                                 if x.get("alternativas") and x["id"] < questao["id"]]
        for outro_id, outra_certa in vizinhas:
            mutua = min(_cobertura(certa, outra_certa), _cobertura(outra_certa, certa))
            if (mutua >= LIMIAR_GABARITO_IGUAL and questao["id"] < outro_id
                    and not _aceito(questao["id"], f"gabarito de {outro_id}")):
                avisos.append(
                    f"{questao['id']}: a resposta certa divide {mutua:.0%} do vocabulário com a de "
                    f"{outro_id} — duas questões ensinando a mesma coisa")

    # 5b. lado direito de pareamento que é a resposta certa de outra questão.
    # A regra 5 lia só `alternativas`, e foi por essa fresta que os dois
    # pareamentos do módulo 4.2 passaram com oito gabaritos de outras questões.
    for questao in questoes:
        if questao["tipo"] != "pareamento":
            continue
        for i, par in enumerate(questao["pares"], start=1):
            for outro_id, outra_certa in [(x["id"], x["alternativas"][x["correta"]])
                                          for x in questoes if x.get("alternativas")]:
                mutua = min(_cobertura(par[1], outra_certa), _cobertura(outra_certa, par[1]))
                if mutua >= LIMIAR_GABARITO_IGUAL and not _aceito(questao["id"], f"par {i}"):
                    avisos.append(
                        f"{questao['id']}: o par {i} divide {mutua:.0%} do vocabulário com a resposta "
                        f"certa de {outro_id} — o pareamento entrega o gabarito de outra questão")

    # 4. distrator que é o gabarito de outra questão
    corretas = {q["id"]: q for q in questoes if q.get("alternativas")}
    for questao in questoes:
        alternativas = questao.get("alternativas")
        if not alternativas:
            continue
        for i, distrator in enumerate(alternativas):
            if i == questao["correta"]:
                continue
            for outro_id, proximo in corretas.items():
                if outro_id == questao["id"]:
                    continue
                outra_correta = proximo["alternativas"][proximo["correta"]]
                mutua = min(_cobertura(distrator, outra_correta),
                            _cobertura(outra_correta, distrator))
                if mutua >= LIMIAR_DISTRATOR and not _aceito(questao["id"], f"alternativa {i + 1}"):
                    # questões que definem termos vizinhos usam as definições umas
                    # das outras como distrator de propósito; o sinal só interessa
                    # quando as duas perguntam a mesma coisa
                    if _cobertura(questao["enunciado"], proximo["enunciado"]) < LIMIAR_ENUNCIADO_IGUAL:
                        continue
                    avisos.append(
                        f"{questao['id']}: a alternativa {i + 1} divide {mutua:.0%} do "
                        f"vocabulário com a resposta certa de {outro_id} — distrator não "
                        f"pode ser o gabarito de outra questão")


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

    # A correta não pode ser a mais longa com frequência: é o mesmo defeito da
    # posição fixa, por outro canal. Vale só para o módulo inteiro, por isso fica
    # fora do laço por questão — e fora do modo esqueleto, que tem poucas questões.
    if not esqueleto:
        com_alt = [q for q in questoes if q.get("alternativas")]
        mais_longa = [q for q in com_alt
                      if len(q["alternativas"][q["correta"]]) > max(
                          len(a) for i, a in enumerate(q["alternativas"]) if i != q["correta"])]
        if com_alt:
            fracao = len(mais_longa) / len(com_alt)
            if fracao > MAX_CORRETA_MAIS_LONGA:
                avisos.append(
                    f"a correta é a alternativa mais longa em {len(mais_longa)} de "
                    f"{len(com_alt)} questões de múltipla escolha ({fracao:.0%}); o teto é "
                    f"{MAX_CORRETA_MAIS_LONGA:.0%} e o acaso seria 25% — quem escolhe a mais "
                    f"longa sem ler acerta {fracao:.0%} das vezes neste módulo")

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
            if outras and len(certa) > LIMIAR_CORRETA_LONGA * max(len(a) for a in outras):
                media = sum(len(a) for a in outras) / len(outras)
                avisos.append(
                    f"{ctx}: a alternativa correta tem {len(certa)/max(len(a) for a in outras):.1f}x "
                    f"o tamanho do maior distrator e {len(certa)/media:.1f}x a média deles — "
                    f"desequilíbrio isolado, some ou reescreva os distratores")

        if q["tipo"] == "pareamento":
            direita = [par[1] for par in q["pares"]]
            if len(set(direita)) != len(direita):
                falhas.append(f"{ctx}: dois pares com o mesmo lado direito — pareamento ambíguo")
        if q["tipo"] == "ordenacao" and len(q["itens"]) < 4:
            avisos.append(f"{ctx}: ordenação com menos de 4 itens")

        for tag in q["tags"]:
            if tag != tag.lower() or " " in tag:
                falhas.append(f"{ctx}: tag fora do padrão minúsculo-com-hífen: {tag}")

    achar_gabarito_entregue(dados, avisos)

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
