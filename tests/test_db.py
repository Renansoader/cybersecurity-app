"""A regra "só a primeira tentativa conta" é garantida pelo banco, não pelo código."""

import inspect
import sqlite3

import pytest

from app import db


@pytest.fixture
def banco(tmp_path, monkeypatch):
    monkeypatch.setattr(db, "CAMINHO", tmp_path / "teste.db")
    db.iniciar()
    return db


def test_segunda_primeira_tentativa_estoura_integrity_error(banco):
    """Duas linhas com n_tentativa = 1 para a mesma questão: o banco recusa."""
    banco.registrar_tentativa("0.1.q1", "0.1", "conceitual",
                              acertou=False, usou_dica=False, segundos=12)

    with pytest.raises(sqlite3.IntegrityError):
        with banco.conexao() as con:
            con.execute(
                "INSERT INTO tentativas (questao_id, modulo_id, tipo, acertou,"
                " usou_dica, n_tentativa, segundos, data)"
                " VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                ("0.1.q1", "0.1", "conceitual", 1, 0, 1, 4, "2026-08-14"),
            )

    # e a tentativa original continua sendo a que vale, com o resultado original
    assert banco.primeira_tentativa("0.1.q1")["acertou"] == 0


def test_n_tentativa_e_calculado_pelo_banco(banco):
    """Quem chama nunca informa o número da tentativa; o db conta sozinho."""
    assert "n_tentativa" not in inspect.signature(db.registrar_tentativa).parameters

    numeros = [
        banco.registrar_tentativa("0.1.q1", "0.1", "conceitual",
                                  acertou=False, usou_dica=False, segundos=9)
        for _ in range(3)
    ]
    assert numeros == [1, 2, 3]


def test_n_tentativa_nao_se_repete_apos_apagar_uma_linha_do_meio(banco):
    """Por isso o cálculo é MAX + 1, e não COUNT + 1."""
    for _ in range(3):
        banco.registrar_tentativa("0.1.q1", "0.1", "conceitual",
                                  acertou=False, usou_dica=False, segundos=9)

    with banco.conexao() as con:
        con.execute("DELETE FROM tentativas WHERE questao_id = ? AND n_tentativa = 2",
                    ("0.1.q1",))

    assert banco.registrar_tentativa("0.1.q1", "0.1", "conceitual",
                                     acertou=True, usou_dica=False, segundos=5) == 4


def test_dominio_ignora_revisoes_e_conta_meio_ponto_com_dica(banco):
    banco.registrar_tentativa("0.1.q1", "0.1", "conceitual",
                              acertou=True, usou_dica=False, segundos=10)   # 1,0
    banco.registrar_tentativa("0.1.q2", "0.1", "conceitual",
                              acertou=True, usou_dica=True, segundos=30)    # 0,5
    banco.registrar_tentativa("0.1.q3", "0.1", "cenario",
                              acertou=False, usou_dica=False, segundos=15)  # 0

    # revisões do SRS: acertos em 2ª tentativa não podem mexer no domínio
    banco.registrar_tentativa("0.1.q3", "0.1", "cenario",
                              acertou=True, usou_dica=False, segundos=8)
    banco.registrar_tentativa("0.1.q2", "0.1", "conceitual",
                              acertou=True, usou_dica=False, segundos=7)

    assert banco.dominio_modulo("0.1", total_questoes=4) == pytest.approx(1.5 / 4)


def test_dominio_zero_sem_tentativas(banco):
    assert banco.dominio_modulo("0.1", total_questoes=6) == 0.0


def test_refazer_modulo_libera_uma_nova_primeira_tentativa(banco):
    banco.registrar_tentativa("0.1.q1", "0.1", "conceitual",
                              acertou=False, usou_dica=False, segundos=11)
    banco.apagar_tentativas_modulo("0.1")

    assert banco.primeira_tentativa("0.1.q1") is None
    assert banco.registrar_tentativa("0.1.q1", "0.1", "conceitual",
                                     acertou=True, usou_dica=False, segundos=6) == 1
    assert banco.dominio_modulo("0.1", total_questoes=1) == 1.0


def test_questoes_vistas_lista_so_primeiras_tentativas(banco):
    banco.registrar_tentativa("0.1.q1", "0.1", "conceitual",
                              acertou=True, usou_dica=False, segundos=10)
    banco.registrar_tentativa("0.1.q1", "0.1", "conceitual",
                              acertou=True, usou_dica=False, segundos=5)
    banco.registrar_tentativa("0.1.q2", "0.1", "conceitual",
                              acertou=False, usou_dica=False, segundos=10)

    assert banco.questoes_vistas("0.1") == {"0.1.q1", "0.1.q2"}
