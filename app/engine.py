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
FRACAO_MINIMA_PARA_JULGAR = 0.3        # abaixo disso não há amostra para julgar

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


def _fracao_vista(modulo):
    total = len(modulo["questoes"])
    return len(db.questoes_vistas(modulo["id"])) / total if total else 0.0


def modulo_em_reforco(modulo):
    """Módulo fraco: desempenho abaixo de 60% no que já foi feito.

    Usa dominio_sobre_vistas, e não o domínio: quem acabou de começar um módulo
    tem domínio baixo por definição, e chamar isso de fraco marcaria todo mundo
    nas primeiras questões. Abaixo de 30% do módulo visto, não há amostra que
    justifique o rótulo — nesses casos a resposta é False.

    A revisão de teoria por segundo erro na mesma questão não depende disto:
    ela sai imediatamente, no campo `revisar_teoria` de responder().
    """
    if _fracao_vista(modulo) < FRACAO_MINIMA_PARA_JULGAR:
        return False
    if db.dominio_sobre_vistas(modulo["id"]) < DOMINIO_REFORCO:
        return True
    return any(linha["erros"] >= ERROS_PARA_REVISAR_TEORIA
               for linha in db.srs_do_modulo(modulo["id"]))


def pontos_fracos(modulos, quantos=3):
    """Os módulos com pior desempenho, para o dashboard sugerir o que revisar.

    Mesmo critério do reforço: só entra módulo com amostra suficiente, e a
    comparação é sobre o que já foi visto.
    """
    candidatos = [(db.dominio_sobre_vistas(mid), mid) for mid, modulo in modulos.items()
                  if _fracao_vista(modulo) >= FRACAO_MINIMA_PARA_JULGAR]
    return [mid for _, mid in sorted(candidatos)[:quantos]]


METAS = (10, 20, 30)
META_PADRAO = 20


def meta_diaria():
    return int(db.preferencia("meta_diaria", META_PADRAO))


def resumo_do_dia(hoje=None):
    """(questões respondidas, acertos, minutos) do dia."""
    hoje = (hoje or date.today()).isoformat()
    dia = db.atividade_por_dia(hoje).get(hoje)
    if not dia:
        return 0, 0, 0
    return dia["n"], dia["acertos"], dia["segundos"] // 60


def streak(hoje=None):
    """Dias consecutivos com a meta batida, contando de trás para frente.

    O dia de hoje só quebra a sequência depois de terminado, então ele conta
    como neutro enquanto a meta não é atingida.

    ponytail: a meta atual é aplicada aos dias passados. Se a meta mudar, o
    streak é recalculado com o valor novo — guardar a meta de cada dia exigiria
    outra tabela, e o efeito é pequeno.
    """
    hoje = hoje or date.today()
    meta = meta_diaria()
    atividade = db.atividade_por_dia((hoje - timedelta(days=400)).isoformat())

    dias = 0
    dia = hoje
    if atividade.get(hoje.isoformat(), {}).get("n", 0) < meta:
        dia -= timedelta(days=1)   # hoje ainda está em aberto
    while atividade.get(dia.isoformat(), {}).get("n", 0) >= meta:
        dias += 1
        dia -= timedelta(days=1)
    return dias


def modo_da_questao(questao_id, hoje=None):
    """Como a tela deve abrir a questão. A decisão é do motor, não da view.

    "nova"    — sem primeira tentativa registrada; responde normalmente.
    "revisao" — já respondida e com revisão vencida no SRS; pode responder de
                novo, mas isso não toca o domínio.
    "leitura" — já respondida e sem revisão vencida; mostra o enunciado, a
                tentativa registrada e a explicação, sem alternativa clicável.
    """
    if db.primeira_tentativa(questao_id) is None:
        return "nova"
    agendamento = db.srs_obter(questao_id)
    hoje = hoje or date.today()
    if agendamento and agendamento["proxima_data"] <= hoje.isoformat():
        return "revisao"
    return "leitura"


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
    """Módulos cujo nível está liberado.

    O cadeado da especificação é por nível, e não por módulo: dentro de um
    nível aberto, todos os módulos ficam disponíveis. `pre_requisitos` do
    conteúdo é ordem sugerida — usada para sugerir o próximo módulo —, e não
    tranca: exigir a conclusão de um módulo de 36 questões para liberar o
    seguinte travaria o nível 0 inteiro no primeiro módulo.
    """
    liberados = niveis_desbloqueados(modulos, niveis)
    return {mid: m for mid, m in modulos.items() if m["nivel"] in liberados}


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
