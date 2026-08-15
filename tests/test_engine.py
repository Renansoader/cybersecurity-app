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
    assert motor.modulo_em_reforco(modulo) is True


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
