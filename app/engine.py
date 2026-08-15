"""Motor de sessão: repetição espaçada, seleção de questões e progressão.

Nada aqui desenha tela e nada aqui lê arquivo. O motor recebe os módulos já
carregados e validados por content.py, e fala com o banco só por db.py.

A regra que sustenta o resto: o domínio vem exclusivamente das primeiras
tentativas. Revisão do SRS mexe na retenção, nunca na estatística.
"""

from datetime import date, timedelta

from app import db

# Tabela de repetição espaçada da especificação (SM-2 simplificado, por questão)
MULTIPLICADOR_ACERTO = 2.5             # acerto de primeira, sem dica
MULTIPLICADOR_ACERTO_COM_DICA = 1.3    # dica cobra seu preço: volta mais cedo
INTERVALO_MINIMO = 1                   # dias; todo erro volta para cá

PESO_ACERTO = 1.0
PESO_ACERTO_COM_DICA = 0.5
PESO_ERRO = 0.0

DOMINIO_CONCLUSAO = 0.7
DOMINIO_REFORCO = 0.6
ERROS_PARA_REVISAR_TEORIA = 2

PROPORCAO_REVISAO = 0.6                # 60% revisão vencida, 40% conteúdo novo
JANELA_DIFICULDADE = 10                # últimas N primeiras tentativas


def peso(acertou, usou_dica):
    """Quanto a questão vale no domínio. Dica vale metade."""
    if not acertou:
        return PESO_ERRO
    return PESO_ACERTO_COM_DICA if usou_dica else PESO_ACERTO


# --- responder uma questão --------------------------------------------------

def responder(questao, modulo_id, acertou, usou_dica, segundos, hoje=None):
    """Registra a tentativa, reagenda a questão no SRS e diz o que aconteceu.

    Devolve um dicionário com o número da tentativa, se ela conta no domínio,
    quanto vale, o novo estado de SRS e se a teoria ligada precisa ser revista.
    """
    hoje = hoje or date.today()
    n_tentativa = db.registrar_tentativa(questao["id"], modulo_id, questao["tipo"],
                                         acertou, usou_dica, segundos)
    estado = _reagendar(questao["id"], modulo_id, acertou, usou_dica, hoje)
    conta_no_dominio = n_tentativa == 1
    return {
        "n_tentativa": n_tentativa,
        "conta_no_dominio": conta_no_dominio,
        "peso": peso(acertou, usou_dica) if conta_no_dominio else 0.0,
        "srs": estado,
        "revisar_teoria": estado["erros"] >= ERROS_PARA_REVISAR_TEORIA,
    }


def _reagendar(questao_id, modulo_id, acertou, usou_dica, hoje):
    anterior = db.srs_obter(questao_id)
    intervalo = anterior["intervalo"] if anterior else INTERVALO_MINIMO
    acertos = anterior["acertos"] if anterior else 0
    erros = anterior["erros"] if anterior else 0
    # `facilidade` é coluna da especificação e fica no valor padrão: os
    # multiplicadores desta versão são fixos (2,5 e 1,3), como na tabela 6.3.
    facilidade = anterior["facilidade"] if anterior else 2.5

    if not acertou:
        intervalo = INTERVALO_MINIMO
        erros += 1
    else:
        multiplicador = (MULTIPLICADOR_ACERTO_COM_DICA if usou_dica
                         else MULTIPLICADOR_ACERTO)
        intervalo = max(INTERVALO_MINIMO, intervalo * multiplicador)
        acertos += 1

    proxima_data = (hoje + timedelta(days=round(intervalo))).isoformat()
    db.srs_salvar(questao_id, modulo_id, intervalo, facilidade, proxima_data,
                  acertos, erros)
    return {"intervalo": intervalo, "proxima_data": proxima_data,
            "acertos": acertos, "erros": erros}


# --- domínio e progressão ---------------------------------------------------

def dominio(modulo):
    return db.dominio_modulo(modulo["id"], len(modulo["questoes"]))


def modulo_concluido(modulo):
    """Domínio ≥ 0,7 E todas as questões vistas ao menos uma vez."""
    if dominio(modulo) < DOMINIO_CONCLUSAO:
        return False
    ids = {questao["id"] for questao in modulo["questoes"]}
    return ids <= db.questoes_vistas(modulo["id"])


def modulo_em_reforco(modulo):
    """Módulo fraco: domínio abaixo de 60% ou questão errada duas vezes."""
    if db.questoes_vistas(modulo["id"]) and dominio(modulo) < DOMINIO_REFORCO:
        return True
    return any(linha["erros"] >= ERROS_PARA_REVISAR_TEORIA
               for linha in db.srs_do_modulo(modulo["id"]))


def niveis_desbloqueados(modulos, niveis):
    """Ids dos níveis liberados, pela média de domínio dos níveis exigidos."""
    dominios = {mid: dominio(m) for mid, m in modulos.items()}
    liberados = set()
    for nivel in niveis:
        regra = nivel["desbloqueio"]
        if regra["tipo"] == "aberto":
            liberados.add(nivel["id"])
            continue
        alvo = [dominios[mid] for mid, m in modulos.items()
                if m["nivel"] in regra["niveis"]]
        if alvo and sum(alvo) / len(alvo) >= regra["minimo"]:
            liberados.add(nivel["id"])
    return liberados


def modulos_disponiveis(modulos, niveis):
    """Módulos de nível liberado e com os pré-requisitos concluídos."""
    liberados = niveis_desbloqueados(modulos, niveis)
    concluidos = {mid for mid, m in modulos.items() if modulo_concluido(m)}
    return {mid: m for mid, m in modulos.items()
            if m["nivel"] in liberados and set(m["pre_requisitos"]) <= concluidos}


def sincronizar_status(modulos, niveis):
    """Grava em modulos_status o que o motor calculou. Só escrita, sem decisão."""
    liberados = niveis_desbloqueados(modulos, niveis)
    for mid, modulo in modulos.items():
        db.salvar_status_modulo(mid, modulo["nivel"] in liberados,
                                modulo_concluido(modulo), dominio(modulo))


# --- aprendizagem dinâmica --------------------------------------------------

def desempenho_por_tag(modulos):
    """Média de peso das primeiras tentativas, por tag. Tag sem dado fica fora."""
    por_id = {q["id"]: q for m in modulos.values() for q in m["questoes"]}
    soma, total = {}, {}
    for linha in db.primeiras_tentativas():
        questao = por_id.get(linha["questao_id"])
        if questao is None:
            continue
        valor = peso(linha["acertou"], linha["usou_dica"])
        for tag in questao["tags"]:
            soma[tag] = soma.get(tag, 0.0) + valor
            total[tag] = total.get(tag, 0) + 1
    return {tag: soma[tag] / total[tag] for tag in soma}


def dificuldade_alvo(janela=JANELA_DIFICULDADE):
    """Sobe quando as últimas N foram acerto de primeira sem dica; desce com 3 erros."""
    ultimas = db.ultimas_primeiras_tentativas(janela)
    if len(ultimas) < janela:
        return 1
    if all(linha["acertou"] and not linha["usou_dica"] for linha in ultimas):
        return 3
    if sum(1 for linha in ultimas if not linha["acertou"]) >= 3:
        return 1
    return 2


def montar_sessao(modulos, niveis, meta=20, hoje=None):
    """Sessão diária: 60% revisão vencida + 40% novo, sem repetir tipo em sequência.

    Devolve uma lista de (modulo_id, questao). Se não houver revisão vencida
    suficiente, a sobra é preenchida com conteúdo novo.
    """
    hoje = hoje or date.today()
    disponiveis = modulos_disponiveis(modulos, niveis)
    por_id = {q["id"]: (mid, q) for mid, m in disponiveis.items() for q in m["questoes"]}

    limite_revisao = round(meta * PROPORCAO_REVISAO)
    revisao = [por_id[linha["questao_id"]]
               for linha in db.srs_vencidos(hoje.isoformat())
               if linha["questao_id"] in por_id][:limite_revisao]

    vistas = {linha["questao_id"] for linha in db.primeiras_tentativas()}
    ja_escolhidas = {questao["id"] for _, questao in revisao}

    fraqueza = desempenho_por_tag(modulos)
    media = sum(fraqueza.values()) / len(fraqueza) if fraqueza else 1.0
    alvo = dificuldade_alvo()

    def prioridade(item):
        _, questao = item
        notas = [fraqueza[tag] for tag in questao["tags"] if tag in fraqueza]
        # tag mais fraca primeiro; depois a dificuldade mais perto do alvo
        return (min(notas) if notas else media,
                abs(questao["dificuldade"] - alvo),
                questao["id"])

    novas = sorted((item for qid, item in por_id.items()
                    if qid not in vistas and qid not in ja_escolhidas),
                   key=prioridade)

    return _variar_tipos(revisao + novas[:max(0, meta - len(revisao))])


def _variar_tipos(sessao):
    """Evita duas questões seguidas do mesmo tipo, mantendo a ordem no resto."""
    restantes = list(sessao)
    ordenada = []
    while restantes:
        indice = next(
            (i for i, (_, questao) in enumerate(restantes)
             if not ordenada or questao["tipo"] != ordenada[-1][1]["tipo"]),
            0,  # só sobrou o mesmo tipo: aceita a repetição em vez de travar
        )
        ordenada.append(restantes.pop(indice))
    return ordenada
