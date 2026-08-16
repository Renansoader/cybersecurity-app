"""Motor: primeira tentativa imutável, dica reduz peso, erro reagenda para 1 dia."""

from datetime import date

import pytest

from app import db, engine

HOJE = date(2026, 8, 14)


def questao(qid, tipo="conceitual", dificuldade=1, tags=("fundamentos",)):
    return {"id": qid, "tipo": tipo, "dificuldade": dificuldade, "tags": list(tags),
            "dicas": ["a", "b"], "objetivos": [0]}


@pytest.fixture
def motor(tmp_path, monkeypatch):
    monkeypatch.setattr(db, "CAMINHO", tmp_path / "teste.db")
    db.iniciar()
    return engine


@pytest.fixture
def modulos():
    return {
        "0.1": {"id": "0.1", "nivel": 0, "pre_requisitos": [],
                "questoes": [questao("0.1.q1"), questao("0.1.q2", tipo="cenario"),
                             questao("0.1.q3", tipo="ordenacao"),
                             questao("0.1.q4", tipo="caca_erro")]},
        "1.1": {"id": "1.1", "nivel": 1, "pre_requisitos": [],
                "questoes": [questao("1.1.q1")]},
    }


@pytest.fixture
def niveis():
    return [
        {"id": 0, "nome": "Alicerce", "desbloqueio": {"tipo": "aberto"}},
        {"id": 1, "nome": "Base", "desbloqueio": {"tipo": "dominio", "niveis": [0],
                                                  "minimo": 0.7}},
    ]


# --- a primeira tentativa é a que vale ---

def test_segunda_tentativa_nao_mexe_no_dominio(motor, modulos):
    modulo = modulos["0.1"]
    q = modulo["questoes"][0]

    primeira = motor.responder(q, "0.1", acertou=False, usou_dica=False,
                               segundos=20, hoje=HOJE)
    assert primeira["n_tentativa"] == 1
    assert primeira["conta_no_dominio"] is True
    assert primeira["peso"] == 0.0
    assert motor.dominio(modulo) == 0.0

    segunda = motor.responder(q, "0.1", acertou=True, usou_dica=False,
                              segundos=8, hoje=HOJE)
    assert segunda["n_tentativa"] == 2
    assert segunda["conta_no_dominio"] is False
    assert segunda["peso"] == 0.0
    assert motor.dominio(modulo) == 0.0, "acerto em revisão não pode virar domínio"


def test_acerto_de_primeira_sem_dica_vale_um_ponto(motor, modulos):
    modulo = modulos["0.1"]
    motor.responder(modulo["questoes"][0], "0.1", acertou=True, usou_dica=False,
                    segundos=10, hoje=HOJE)
    assert motor.dominio(modulo) == pytest.approx(1 / 4)


def test_dica_reduz_o_peso_pela_metade(motor, modulos):
    modulo = modulos["0.1"]
    motor.responder(modulo["questoes"][0], "0.1", acertou=True, usou_dica=True,
                    segundos=40, hoje=HOJE)
    assert motor.dominio(modulo) == pytest.approx(0.5 / 4)


# --- repetição espaçada ---

def test_erro_reagenda_para_um_dia(motor, modulos):
    q = modulos["0.1"]["questoes"][0]
    resultado = motor.responder(q, "0.1", acertou=False, usou_dica=False,
                                segundos=25, hoje=HOJE)

    assert resultado["srs"]["intervalo"] == 1
    assert resultado["srs"]["proxima_data"] == "2026-08-15"


def test_erro_depois_de_acertos_derruba_o_intervalo_para_um_dia(motor, modulos):
    q = modulos["0.1"]["questoes"][0]
    motor.responder(q, "0.1", acertou=True, usou_dica=False, segundos=10, hoje=HOJE)
    motor.responder(q, "0.1", acertou=True, usou_dica=False, segundos=10, hoje=HOJE)
    assert db.srs_obter(q["id"])["intervalo"] == pytest.approx(6.25)

    resultado = motor.responder(q, "0.1", acertou=False, usou_dica=False,
                                segundos=10, hoje=HOJE)
    assert resultado["srs"]["intervalo"] == 1
    assert resultado["srs"]["proxima_data"] == "2026-08-15"


def test_acerto_sem_dica_multiplica_por_dois_e_meio(motor, modulos):
    q = modulos["0.1"]["questoes"][0]
    resultado = motor.responder(q, "0.1", acertou=True, usou_dica=False,
                                segundos=10, hoje=HOJE)

    assert resultado["srs"]["intervalo"] == pytest.approx(2.5)
    assert resultado["srs"]["proxima_data"] == "2026-08-16"  # 14 + round(2,5) = 16


def test_acerto_com_dica_volta_mais_cedo_que_acerto_sem_dica(motor, modulos):
    com_dica = motor.responder(questao("a"), "0.1", acertou=True, usou_dica=True,
                               segundos=40, hoje=HOJE)
    sem_dica = motor.responder(questao("b"), "0.1", acertou=True, usou_dica=False,
                               segundos=10, hoje=HOJE)

    assert com_dica["srs"]["intervalo"] == pytest.approx(1.3)
    assert com_dica["srs"]["proxima_data"] < sem_dica["srs"]["proxima_data"]


def test_segundo_erro_na_mesma_questao_manda_revisar_a_teoria(motor, modulos):
    modulo = modulos["0.1"]
    q = modulo["questoes"][0]

    primeiro = motor.responder(q, "0.1", acertou=False, usou_dica=False,
                               segundos=20, hoje=HOJE)
    assert primeiro["revisar_teoria"] is False

    segundo = motor.responder(q, "0.1", acertou=False, usou_dica=False,
                              segundos=20, hoje=HOJE)
    assert segundo["revisar_teoria"] is True


# --- reforço: desempenho no que foi visto, não progresso no módulo ---

def modulo_de_dez(mid="9.9"):
    """Id de questão é único no app inteiro, não só dentro do módulo."""
    return {"id": mid, "nivel": 0, "pre_requisitos": [],
            "questoes": [questao(f"{mid}.q{i}") for i in range(10)]}


def test_modulo_recem_iniciado_nao_e_marcado_como_fraco(motor):
    """3 acertos limpos e 7 questões não vistas: domínio 0,3, desempenho 1,0."""
    modulo = modulo_de_dez()
    for q in modulo["questoes"][:3]:
        motor.responder(q, "9.9", acertou=True, usou_dica=False, segundos=10, hoje=HOJE)

    assert motor.dominio(modulo) == pytest.approx(0.3)
    assert db.dominio_sobre_vistas("9.9") == pytest.approx(1.0)
    assert motor.modulo_em_reforco(modulo) is False


def test_modulo_com_desempenho_ruim_e_marcado_como_fraco(motor):
    """8 vistas e 2 acertos: desempenho 0,25 sobre uma amostra que já vale."""
    modulo = modulo_de_dez()
    for q in modulo["questoes"][:2]:
        motor.responder(q, "9.9", acertou=True, usou_dica=False, segundos=10, hoje=HOJE)
    for q in modulo["questoes"][2:8]:
        motor.responder(q, "9.9", acertou=False, usou_dica=False, segundos=10, hoje=HOJE)

    assert db.dominio_sobre_vistas("9.9") == pytest.approx(0.25)
    assert motor.modulo_em_reforco(modulo) is True


def test_amostra_pequena_nao_basta_para_chamar_de_fraco(motor):
    modulo = modulo_de_dez()
    for q in modulo["questoes"][:2]:  # 20% do módulo, tudo errado
        motor.responder(q, "9.9", acertou=False, usou_dica=False, segundos=10, hoje=HOJE)

    assert db.dominio_sobre_vistas("9.9") == 0.0
    assert motor.modulo_em_reforco(modulo) is False, "20% do módulo não é amostra"


def test_pontos_fracos_ignora_modulo_sem_amostra(motor):
    fraco, bom, novo = modulo_de_dez("9.9"), modulo_de_dez("8.8"), modulo_de_dez("7.7")

    for q in fraco["questoes"][:5]:
        motor.responder(q, "9.9", acertou=False, usou_dica=False, segundos=10, hoje=HOJE)
    for q in bom["questoes"][:5]:
        motor.responder(q, "8.8", acertou=True, usou_dica=False, segundos=10, hoje=HOJE)
    motor.responder(novo["questoes"][0], "7.7", acertou=False, usou_dica=False,
                    segundos=10, hoje=HOJE)

    assert motor.pontos_fracos({"9.9": fraco, "8.8": bom, "7.7": novo}) == ["9.9", "8.8"]


# --- streak e resumo do dia ---

def test_resumo_do_dia_conta_o_que_foi_respondido_hoje(motor):
    motor.responder(questao("a"), "0.1", acertou=True, usou_dica=False, segundos=90, hoje=HOJE)
    motor.responder(questao("b"), "0.1", acertou=False, usou_dica=False, segundos=30, hoje=HOJE)

    respondidas, acertos, minutos = motor.resumo_do_dia()
    assert (respondidas, acertos, minutos) == (2, 1, 2)


def test_streak_conta_dias_seguidos_com_a_meta_batida(motor, monkeypatch):
    db.salvar_preferencia("meta_diaria", 2)
    hoje = date(2026, 8, 15)

    # dois dias seguidos com a meta batida, e um dia anterior sem
    for dia, quantas in ((date(2026, 8, 12), 1), (date(2026, 8, 14), 2), (hoje, 2)):
        for i in range(quantas):
            with db.conexao() as con:
                con.execute(
                    "INSERT INTO tentativas (questao_id, modulo_id, tipo, acertou, usou_dica,"
                    " n_tentativa, segundos, data) VALUES (?, ?, 'conceitual', 1, 0, 1, 10, ?)",
                    (f"q-{dia}-{i}", "0.1", dia.isoformat()))

    assert motor.streak(hoje=hoje) == 2, "12/08 não bateu a meta e quebra a sequência"


def test_streak_nao_zera_por_hoje_ainda_estar_em_aberto(motor):
    db.salvar_preferencia("meta_diaria", 2)
    hoje = date(2026, 8, 15)
    with db.conexao() as con:
        for i in range(2):
            con.execute(
                "INSERT INTO tentativas (questao_id, modulo_id, tipo, acertou, usou_dica,"
                " n_tentativa, segundos, data) VALUES (?, ?, 'conceitual', 1, 0, 1, 10, ?)",
                (f"q{i}", "0.1", "2026-08-14"))

    # nada respondido hoje: o dia ainda está em aberto e não deve quebrar a sequência
    assert motor.streak(hoje=hoje) == 1


# --- modo da questão: quem decide é o motor ---

def test_questao_nunca_respondida_e_nova(motor, modulos):
    assert motor.modo_da_questao("0.1.q1", hoje=HOJE) == "nova"


def test_questao_respondida_hoje_volta_como_leitura_hoje(motor, modulos):
    q = modulos["0.1"]["questoes"][0]
    motor.responder(q, "0.1", acertou=True, usou_dica=False, segundos=10, hoje=HOJE)

    assert motor.modo_da_questao(q["id"], hoje=HOJE) == "leitura"


def test_a_mesma_questao_vira_revisao_na_data_agendada(motor, modulos):
    q = modulos["0.1"]["questoes"][0]
    resultado = motor.responder(q, "0.1", acertou=True, usou_dica=False,
                                segundos=10, hoje=HOJE)
    agendada = date.fromisoformat(resultado["srs"]["proxima_data"])

    assert motor.modo_da_questao(q["id"], hoje=date(2026, 8, 15)) == "leitura"
    assert motor.modo_da_questao(q["id"], hoje=agendada) == "revisao"


def test_erro_hoje_ja_volta_como_revisao_amanha(motor, modulos):
    q = modulos["0.1"]["questoes"][0]
    motor.responder(q, "0.1", acertou=False, usou_dica=False, segundos=10, hoje=HOJE)

    assert motor.modo_da_questao(q["id"], hoje=HOJE) == "leitura"
    assert motor.modo_da_questao(q["id"], hoje=date(2026, 8, 15)) == "revisao"


# --- progressão ---

def test_modulo_so_conclui_com_dominio_e_todas_as_questoes_vistas(motor, modulos):
    modulo = modulos["0.1"]
    for q in modulo["questoes"][:3]:
        motor.responder(q, "0.1", acertou=True, usou_dica=False, segundos=10, hoje=HOJE)

    assert motor.dominio(modulo) == pytest.approx(0.75)
    assert motor.modulo_concluido(modulo) is False, "falta ver a quarta questão"

    motor.responder(modulo["questoes"][3], "0.1", acertou=False, usou_dica=False,
                    segundos=10, hoje=HOJE)
    assert motor.modulo_concluido(modulo) is True


def test_nivel_seguinte_abre_com_setenta_por_cento_do_anterior(motor, modulos, niveis):
    assert motor.niveis_desbloqueados(modulos, niveis) == {0}

    for q in modulos["0.1"]["questoes"][:3]:
        motor.responder(q, "0.1", acertou=True, usou_dica=False, segundos=10, hoje=HOJE)

    assert motor.niveis_desbloqueados(modulos, niveis) == {0, 1}


def test_modulo_bloqueado_fica_fora_da_sessao(motor, modulos, niveis):
    sessao = motor.montar_sessao(modulos, niveis, meta=10, hoje=HOJE)
    assert {mid for mid, _ in sessao} == {"0.1"}


def test_sincronizar_status_grava_o_que_o_motor_calculou(motor, modulos, niveis):
    motor.responder(modulos["0.1"]["questoes"][0], "0.1", acertou=True,
                    usou_dica=False, segundos=10, hoje=HOJE)
    motor.sincronizar_status(modulos, niveis)

    status = db.status_modulos()
    assert status["0.1"]["desbloqueado"] == 1
    assert status["0.1"]["dominio"] == pytest.approx(0.25)
    assert status["1.1"]["desbloqueado"] == 0


# --- sessão diária ---

def test_sessao_respeita_a_meta_e_nao_repete_questao(motor, modulos, niveis):
    sessao = motor.montar_sessao(modulos, niveis, meta=3, hoje=HOJE)
    ids = [q["id"] for _, q in sessao]

    assert len(sessao) == 3
    assert len(set(ids)) == 3


def test_sessao_nao_poe_dois_tipos_iguais_em_sequencia(motor, modulos, niveis):
    sessao = motor.montar_sessao(modulos, niveis, meta=4, hoje=HOJE)
    tipos = [q["tipo"] for _, q in sessao]

    assert all(a != b for a, b in zip(tipos, tipos[1:]))


def test_sessao_mistura_revisao_vencida_com_conteudo_novo(motor, modulos, niveis):
    # duas questões erradas hoje: voltam amanhã
    for q in modulos["0.1"]["questoes"][:2]:
        motor.responder(q, "0.1", acertou=False, usou_dica=False, segundos=10, hoje=HOJE)

    amanha = date(2026, 8, 15)
    sessao = motor.montar_sessao(modulos, niveis, meta=4, hoje=amanha)
    ids = {q["id"] for _, q in sessao}

    assert {"0.1.q1", "0.1.q2"} <= ids, "as vencidas entram"
    assert {"0.1.q3", "0.1.q4"} <= ids, "e o resto vem de conteúdo novo"


def test_sessao_prioriza_a_tag_mais_fraca(motor, niveis):
    modulos = {"0.1": {"id": "0.1", "nivel": 0, "pre_requisitos": [], "questoes": [
        questao("0.1.q1", tags=["cripto"]),
        questao("0.1.q2", tags=["redes"], tipo="cenario"),
        questao("0.1.q3", tags=["cripto"], tipo="ordenacao"),
        questao("0.1.q4", tags=["redes"], tipo="caca_erro"),
    ]}}
    # erra uma de cripto e acerta uma de redes: cripto fica com a média pior
    motor.responder(modulos["0.1"]["questoes"][0], "0.1", acertou=False,
                    usou_dica=False, segundos=10, hoje=HOJE)
    motor.responder(modulos["0.1"]["questoes"][1], "0.1", acertou=True,
                    usou_dica=False, segundos=10, hoje=HOJE)

    # meta 1 e sem revisão vencida hoje: sobra só a vaga de conteúdo novo
    sessao = motor.montar_sessao(modulos, niveis, meta=1, hoje=HOJE)
    assert [q["id"] for _, q in sessao] == ["0.1.q3"], "a questão de cripto vem antes"


def test_dificuldade_alvo_sobe_com_dez_acertos_limpos(motor):
    assert motor.dificuldade_alvo() == 1  # sem histórico, começa fácil

    for i in range(10):
        motor.responder(questao(f"q{i}"), "0.1", acertou=True, usou_dica=False,
                        segundos=8, hoje=HOJE)
    assert motor.dificuldade_alvo() == 3

    for i in range(3):
        motor.responder(questao(f"e{i}"), "0.1", acertou=False, usou_dica=False,
                        segundos=8, hoje=HOJE)
    assert motor.dificuldade_alvo() == 1
