"""O botão "Refazer módulo do zero" é o único caminho destrutivo da interface.

Teste de fiação: garante que ele existe na tela, que cancelar não apaga nada e
que dois cliques apagam de verdade. Abre uma janela real — é o único jeito de
provar que o botão está ligado ao db, e não apenas desenhado.
"""

import pytest

from app import db, engine


@pytest.fixture
def app(tmp_path, monkeypatch):
    monkeypatch.setattr(db, "CAMINHO", tmp_path / "teste.db")
    db.iniciar()
    from main import App
    janela = App()
    janela.root.withdraw()          # não pisca na frente de quem roda os testes
    yield janela
    janela.root.destroy()


def procurar(widget, comeco):
    """Primeiro widget cujo texto começa com `comeco`."""
    for filho in widget.winfo_children():
        try:
            if filho.cget("text").startswith(comeco):
                return filho
        except Exception:
            pass
        achado = procurar(filho, comeco)
        if achado:
            return achado
    return None


def responder_tres(app):
    modulo = app.modulos["0.1"]
    for questao in modulo["questoes"][:3]:
        engine.responder(questao, "0.1", acertou=True, usou_dica=False, segundos=10)
    return modulo


def test_botao_refazer_existe_na_tela_de_modulo(app):
    responder_tres(app)
    app.abrir_modulo("0.1")
    app.root.update()

    assert procurar(app.corpo, "Refazer módulo do zero") is not None


def test_cancelar_nao_apaga_nada(app):
    responder_tres(app)
    app.abrir_modulo("0.1")
    app.root.update()

    procurar(app.corpo, "Refazer módulo do zero").invoke()
    app.root.update()
    assert procurar(app.corpo, "Apagar 3 tentativa") is not None, "não avisou quantas apaga"

    procurar(app.corpo, "Cancelar").invoke()
    app.root.update()

    assert len(db.questoes_vistas("0.1")) == 3
    assert procurar(app.corpo, "Refazer módulo do zero") is not None, "não desarmou"


def test_um_clique_sozinho_nao_apaga(app):
    responder_tres(app)
    app.abrir_modulo("0.1")
    app.root.update()

    procurar(app.corpo, "Refazer módulo do zero").invoke()
    app.root.update()

    assert len(db.questoes_vistas("0.1")) == 3


def test_dois_cliques_apagam_tentativas_srs_e_avisam(app):
    modulo = responder_tres(app)
    app.abrir_modulo("0.1")
    app.root.update()

    botao = procurar(app.corpo, "Refazer módulo do zero")
    botao.invoke()
    app.root.update()
    botao.invoke()
    app.root.update()

    assert db.questoes_vistas("0.1") == set()
    assert engine.dominio(modulo) == 0.0
    assert db.srs_do_modulo("0.1") == []
    assert procurar(app.corpo, "Tentativas do módulo") is not None, "não avisou o que aconteceu"


def test_depois_de_refazer_a_questao_volta_a_ser_nova(app):
    modulo = responder_tres(app)
    primeira = modulo["questoes"][0]["id"]
    assert engine.modo_da_questao(primeira) == "leitura"

    app.abrir_modulo("0.1")
    app.root.update()
    botao = procurar(app.corpo, "Refazer módulo do zero")
    botao.invoke()
    app.root.update()
    botao.invoke()
    app.root.update()

    assert engine.modo_da_questao(primeira) == "nova"
