"""Carga e validação dos JSONs de conteúdo.

Todo texto de teoria e de questão mora em data/. Nada de conteúdo de estudo
dentro de .py.

A validação roda em tempo de carga e é dura de propósito: um módulo malformado
não pode chegar à tela. O erro sempre diz qual arquivo e qual campo estão
errados, e `carregar_modulos()` devolve os erros em vez de derrubar o app.
"""

import json
from pathlib import Path

PASTA_DADOS = Path(__file__).resolve().parent.parent / "data"

# Os nove tipos da especificação, com os campos que cada um exige além
# dos comuns. Tipo fora desta lista é erro de conteúdo.
CAMPOS_POR_TIPO = {
    "conceitual": ("alternativas", "correta"),
    "cenario": ("alternativas", "correta"),
    "comando": ("alternativas", "correta"),
    "artefato": ("artefato", "alternativas", "correta"),
    "pareamento": ("pares",),
    "ordenacao": ("itens", "ordem_correta"),
    "ataque_defesa": ("alternativas", "correta"),
    "caca_erro": ("trecho", "alternativas", "correta"),
    "desafio": ("desafio_id",),
}

# Tipos em que o usuário escolhe uma alternativa: exigem justificar cada
# distrator, senão o distrator provavelmente está ruim.
TIPOS_COM_ALTERNATIVAS = {t for t, campos in CAMPOS_POR_TIPO.items()
                          if "alternativas" in campos}

CAMPOS_MODULO = ("id", "nivel", "titulo", "objetivos", "pre_requisitos",
                 "teoria", "questoes")
CAMPOS_TEORIA = ("id", "titulo", "texto", "fonte")
CAMPOS_QUESTAO = ("id", "tipo", "dificuldade", "enunciado", "dicas",
                  "pergunta_socratica", "explicacao", "fonte", "tags")

MAX_BLOCOS_TEORIA = 8  # módulo maior que isso cansa; dividir em dois


class ErroDeConteudo(Exception):
    """Erro de esquema em um arquivo de conteúdo, com arquivo e campo."""

    def __init__(self, arquivo, campo, detalhe):
        self.arquivo = arquivo
        self.campo = campo
        self.detalhe = detalhe
        super().__init__(f"{arquivo}: campo '{campo}' — {detalhe}")


def _exigir(dados, campos, arquivo, contexto):
    for campo in campos:
        if campo not in dados:
            raise ErroDeConteudo(arquivo, f"{contexto}.{campo}", "campo obrigatório ausente")


def _exigir_lista(dados, campo, arquivo, contexto, minimo=1):
    valor = dados[campo]
    if not isinstance(valor, list) or len(valor) < minimo:
        raise ErroDeConteudo(arquivo, f"{contexto}.{campo}",
                             f"esperava uma lista com pelo menos {minimo} item(ns)")
    return valor


def validar_questao(questao, arquivo, indice):
    contexto = f"questoes[{indice}]"
    _exigir(questao, CAMPOS_QUESTAO, arquivo, contexto)

    contexto = f"questoes[{questao['id']}]"
    tipo = questao["tipo"]
    if tipo not in CAMPOS_POR_TIPO:
        raise ErroDeConteudo(arquivo, f"{contexto}.tipo",
                             f"tipo desconhecido '{tipo}'; os válidos são "
                             + ", ".join(sorted(CAMPOS_POR_TIPO)))

    _exigir(questao, CAMPOS_POR_TIPO[tipo], arquivo, contexto)
    _exigir_lista(questao, "dicas", arquivo, contexto)
    _exigir_lista(questao, "tags", arquivo, contexto)

    if not isinstance(questao["dificuldade"], int) or not 1 <= questao["dificuldade"] <= 3:
        raise ErroDeConteudo(arquivo, f"{contexto}.dificuldade",
                             "esperava um inteiro de 1 a 3")

    if tipo in TIPOS_COM_ALTERNATIVAS:
        _validar_alternativas(questao, arquivo, contexto)
    elif tipo == "ordenacao":
        _validar_ordenacao(questao, arquivo, contexto)
    elif tipo == "pareamento":
        _validar_pareamento(questao, arquivo, contexto)


def _validar_alternativas(questao, arquivo, contexto):
    alternativas = _exigir_lista(questao, "alternativas", arquivo, contexto, minimo=2)
    correta = questao["correta"]
    if not isinstance(correta, int) or not 0 <= correta < len(alternativas):
        raise ErroDeConteudo(arquivo, f"{contexto}.correta",
                             f"índice {correta!r} não existe em uma lista de "
                             f"{len(alternativas)} alternativas")

    if "por_que_erradas" not in questao:
        raise ErroDeConteudo(arquivo, f"{contexto}.por_que_erradas",
                             "campo obrigatório ausente")

    esperadas = {str(i) for i in range(len(alternativas)) if i != correta}
    recebidas = set(questao["por_que_erradas"])
    if recebidas != esperadas:
        faltando = sorted(esperadas - recebidas)
        sobrando = sorted(recebidas - esperadas)
        raise ErroDeConteudo(
            arquivo, f"{contexto}.por_que_erradas",
            f"precisa justificar exatamente os distratores {sorted(esperadas)}"
            + (f"; faltando {faltando}" if faltando else "")
            + (f"; sobrando {sobrando}" if sobrando else ""))


def _validar_ordenacao(questao, arquivo, contexto):
    itens = _exigir_lista(questao, "itens", arquivo, contexto, minimo=2)
    ordem = questao["ordem_correta"]
    if sorted(ordem) != list(range(len(itens))):
        raise ErroDeConteudo(arquivo, f"{contexto}.ordem_correta",
                             f"esperava uma permutação de 0 a {len(itens) - 1}")


def _validar_pareamento(questao, arquivo, contexto):
    pares = _exigir_lista(questao, "pares", arquivo, contexto, minimo=2)
    for i, par in enumerate(pares):
        if not isinstance(par, list) or len(par) != 2:
            raise ErroDeConteudo(arquivo, f"{contexto}.pares[{i}]",
                                 "esperava um par [esquerda, direita]")


def validar_modulo(modulo, arquivo):
    """Valida a estrutura de um módulo. Levanta ErroDeConteudo no primeiro problema.

    As regras de quantidade (mínimo de 35 questões, pelo menos 4 tipos
    diferentes) são de qualidade de conteúdo e entram na Fase 4, junto com os
    módulos de verdade.
    """
    _exigir(modulo, CAMPOS_MODULO, arquivo, "modulo")

    if not isinstance(modulo["nivel"], int) or not 0 <= modulo["nivel"] <= 5:
        raise ErroDeConteudo(arquivo, "nivel", "esperava um inteiro de 0 a 5")

    _exigir_lista(modulo, "objetivos", arquivo, "modulo")
    if not isinstance(modulo["pre_requisitos"], list):
        raise ErroDeConteudo(arquivo, "pre_requisitos", "esperava uma lista (pode ser vazia)")

    teoria = _exigir_lista(modulo, "teoria", arquivo, "modulo")
    if len(teoria) > MAX_BLOCOS_TEORIA:
        raise ErroDeConteudo(arquivo, "teoria",
                             f"{len(teoria)} blocos; o máximo é {MAX_BLOCOS_TEORIA}")
    for i, bloco in enumerate(teoria):
        _exigir(bloco, CAMPOS_TEORIA, arquivo, f"teoria[{i}]")

    questoes = _exigir_lista(modulo, "questoes", arquivo, "modulo")
    for i, questao in enumerate(questoes):
        validar_questao(questao, arquivo, i)

    _exigir_ids_unicos([b["id"] for b in teoria], arquivo, "teoria")
    _exigir_ids_unicos([q["id"] for q in questoes], arquivo, "questoes")
    return modulo


def _exigir_ids_unicos(ids, arquivo, campo):
    repetidos = sorted({i for i in ids if ids.count(i) > 1})
    if repetidos:
        raise ErroDeConteudo(arquivo, f"{campo}.id", f"ids repetidos: {repetidos}")


def _ler_json(caminho):
    try:
        with open(caminho, encoding="utf-8") as arq:
            return json.load(arq)
    except json.JSONDecodeError as erro:
        raise ErroDeConteudo(caminho.name, f"linha {erro.lineno}",
                             f"JSON inválido: {erro.msg}") from erro


def carregar_modulo(caminho):
    """Lê e valida um módulo. Levanta ErroDeConteudo se estiver malformado."""
    caminho = Path(caminho)
    return validar_modulo(_ler_json(caminho), caminho.name)


def carregar_modulos(pasta=None):
    """Carrega todos os módulos de data/modulos/.

    Devolve (modulos_por_id, erros). Um arquivo quebrado vira uma mensagem na
    lista de erros e os outros continuam carregando — o app avisa em vez de
    não abrir.
    """
    pasta = Path(pasta or PASTA_DADOS / "modulos")
    modulos, erros = {}, []
    for caminho in sorted(pasta.glob("*.json")):
        try:
            modulo = carregar_modulo(caminho)
        except ErroDeConteudo as erro:
            erros.append(str(erro))
            continue
        if modulo["id"] in modulos:
            erros.append(f"{caminho.name}: id de módulo repetido '{modulo['id']}'")
            continue
        modulos[modulo["id"]] = modulo
    return modulos, erros


def carregar_niveis(caminho=None):
    """Lê e valida data/niveis.json."""
    caminho = Path(caminho or PASTA_DADOS / "niveis.json")
    dados = _ler_json(caminho)
    arquivo = caminho.name

    if "niveis" not in dados:
        raise ErroDeConteudo(arquivo, "niveis", "campo obrigatório ausente")

    for i, nivel in enumerate(dados["niveis"]):
        _exigir(nivel, ("id", "nome", "desbloqueio"), arquivo, f"niveis[{i}]")
        regra = nivel["desbloqueio"]
        tipo = regra.get("tipo")
        if tipo == "aberto":
            continue
        if tipo != "dominio":
            raise ErroDeConteudo(arquivo, f"niveis[{i}].desbloqueio.tipo",
                                 f"esperava 'aberto' ou 'dominio', veio {tipo!r}")
        _exigir(regra, ("niveis", "minimo"), arquivo, f"niveis[{i}].desbloqueio")
    return dados["niveis"]
