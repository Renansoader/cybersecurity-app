"""A resposta não pode chegar à tela antes de o usuário confirmar uma tentativa."""

import pytest

from app import content, pedagogy

MODULO = content.carregar_modulo(
    content.PASTA_DADOS / "modulos" / "00-01-o-que-e-ciberseguranca.json")
QUESTOES = {q["id"]: q for q in MODULO["questoes"]}

# Todas as questões de todos os módulos, para as regras que valem para os 41.
TODOS_MODULOS, _ = content.carregar_modulos()
TODAS_QUESTOES = [q for m in TODOS_MODULOS.values() for q in m["questoes"]]
ORDENACAO = [q for q in TODAS_QUESTOES if q["tipo"] == "ordenacao"]
ALTERNATIVAS = [q for q in TODAS_QUESTOES if "alternativas" in q]
PAREAMENTO = [q for q in TODAS_QUESTOES if q["tipo"] == "pareamento"]


def primeira_do_tipo(tipo):
    """Busca por tipo, e não por id: reordenar o conteúdo não quebra o teste."""
    return next(q for q in MODULO["questoes"] if q["tipo"] == tipo)


@pytest.fixture
def multipla():
    return QUESTOES["0.1.q1"]


# --- nada de gabarito antes da hora ---

@pytest.mark.parametrize("questao", TODAS_QUESTOES, ids=lambda q: q["id"])
def test_questao_para_exibir_nao_leva_a_resposta(questao):
    visivel = pedagogy.questao_para_exibir(questao)
    assert set(visivel) & set(pedagogy.CAMPOS_DE_RESPOSTA) == set()


def test_questao_para_exibir_mantem_o_que_a_tela_precisa(multipla):
    visivel = pedagogy.questao_para_exibir(multipla)
    assert visivel["enunciado"] == multipla["enunciado"]
    assert sorted(visivel["alternativas"]) == sorted(multipla["alternativas"])
    assert visivel["dicas_disponiveis"] == len(multipla["dicas"])
    assert "dicas" not in visivel, "as dicas saem uma a uma, sob pedido"


# --- a ordem exibida tem que diferir da ordem correta ---
# Remover o campo de gabarito não basta: nesses dois tipos a ordem É a resposta.

@pytest.mark.parametrize("questao", ORDENACAO, ids=lambda q: q["id"])
def test_ordenacao_nao_e_exibida_na_ordem_correta(questao):
    visivel = pedagogy.questao_para_exibir(questao)
    na_ordem_correta = [questao["itens"][i] for i in questao["ordem_correta"]]

    assert "ordem_correta" not in visivel
    assert len(visivel["itens"]) == len(questao["itens"])
    assert sorted(visivel["itens"]) == sorted(questao["itens"]), "nenhum item sumiu"
    assert visivel["itens"] != na_ordem_correta, (
        f"{questao['id']}: confirmar sem mexer acertaria")


@pytest.mark.parametrize("questao", PAREAMENTO, ids=lambda q: q["id"])
def test_pareamento_nao_e_exibido_alinhado(questao):
    visivel = pedagogy.questao_para_exibir(questao)
    alinhada = [par[1] for par in questao["pares"]]

    assert "pares" not in visivel
    assert visivel["coluna_esquerda"] == [par[0] for par in questao["pares"]]
    assert sorted(visivel["coluna_direita"]) == sorted(alinhada), "nenhum item sumiu"
    assert visivel["coluna_direita"] != alinhada, (
        f"{questao['id']}: ligar linha a linha acertaria")


def test_exibicao_e_deterministica():
    """O mesmo item cai sempre no mesmo lugar: a tela não pode dançar."""
    questao = primeira_do_tipo("ordenacao")
    assert (pedagogy.questao_para_exibir(questao)["itens"]
            == pedagogy.questao_para_exibir(questao)["itens"])


def test_sorteio_que_cairia_na_ordem_proibida_e_rotacionado():
    """Cobre o galho em que o embaralho bate justamente na ordem que vazaria."""
    sorteio = pedagogy._permutar("semente-x", 5, proibida=range(5))
    rotacionado = pedagogy._permutar("semente-x", 5, proibida=sorteio)

    assert rotacionado != sorteio
    assert sorted(rotacionado) == list(range(5)), "continua sendo uma permutação"


# --- correção: o motor desfaz o embaralho ---

def test_correcao_desfaz_o_embaralho_da_ordenacao():
    questao = primeira_do_tipo("ordenacao")
    visivel = pedagogy.questao_para_exibir(questao)
    mapa = visivel["indices_originais"]

    # o usuário monta a sequência certa escolhendo as posições exibidas
    resposta_certa = [mapa.index(original) for original in questao["ordem_correta"]]
    assert pedagogy.conferir(questao, resposta_certa) is True

    # confirmar sem mexer, na ordem em que a tela mostrou, tem que dar errado
    assert pedagogy.conferir(questao, list(range(len(mapa)))) is False


def test_correcao_desfaz_o_embaralho_do_pareamento():
    questao = primeira_do_tipo("pareamento")
    visivel = pedagogy.questao_para_exibir(questao)
    mapa = visivel["indices_direita"]

    resposta_certa = [mapa.index(linha) for linha in range(len(questao["pares"]))]
    assert pedagogy.conferir(questao, resposta_certa) is True
    assert pedagogy.conferir(questao, list(range(len(mapa)))) is False


def test_correcao_de_alternativa_simples(multipla):
    mapa = pedagogy.mapa_de_exibicao(multipla)
    exibida_certa = mapa.index(multipla["correta"])

    assert pedagogy.conferir(multipla, exibida_certa) is True
    assert pedagogy.conferir(multipla, (exibida_certa + 1) % len(mapa)) is False


def test_resposta_de_tamanho_errado_nao_conta_como_acerto():
    questao = primeira_do_tipo("ordenacao")
    assert pedagogy.conferir(questao, [0, 1]) is False


# --- múltipla escolha: a correta não pode ser sempre a primeira linha ---
# O conteúdo grava a alternativa certa no índice 0 em todas as questões escritas
# até hoje. Sem embaralho, o curso inteiro seria respondido sem ler o enunciado.

@pytest.mark.parametrize("questao", ALTERNATIVAS, ids=lambda q: q["id"])
def test_alternativas_nao_saem_na_ordem_do_arquivo(questao):
    visivel = pedagogy.questao_para_exibir(questao)

    assert "correta" not in visivel
    assert sorted(visivel["alternativas"]) == sorted(questao["alternativas"]), (
        "nenhuma alternativa sumiu ou apareceu")
    assert visivel["alternativas"] != questao["alternativas"], (
        f"{questao['id']}: exibida na ordem do arquivo, com a correta na primeira linha")


@pytest.mark.parametrize("questao", ALTERNATIVAS, ids=lambda q: q["id"])
def test_conferir_traduz_o_indice_exibido(questao):
    mapa = pedagogy.mapa_de_exibicao(questao)
    exibida_certa = mapa.index(questao["correta"])

    assert pedagogy.conferir(questao, exibida_certa) is True
    for outra in range(len(mapa)):
        if outra != exibida_certa:
            assert pedagogy.conferir(questao, outra) is False


def test_a_correta_se_espalha_pelas_quatro_posicoes():
    """Se a certa caísse sempre na mesma linha, o embaralho não teria resolvido."""
    posicoes = [pedagogy.mapa_de_exibicao(q).index(q["correta"]) for q in ALTERNATIVAS]
    distribuicao = {p: posicoes.count(p) for p in set(posicoes)}

    assert len(distribuicao) >= 4, f"a correta só cai em {sorted(distribuicao)}"
    maior = max(distribuicao.values()) / len(posicoes)
    assert maior < 0.4, f"a correta cai {maior:.0%} das vezes na mesma linha: {distribuicao}"


# --- dicas ---

def test_dica_so_libera_depois_de_vinte_segundos(multipla):
    assert pedagogy.dica_liberada(19, 0, multipla) is False
    assert pedagogy.dica_liberada(20, 0, multipla) is True


def test_dicas_saem_na_ordem_e_acabam(multipla):
    assert pedagogy.proxima_dica(multipla, 0) == multipla["dicas"][0]
    assert pedagogy.proxima_dica(multipla, 2) == multipla["dicas"][2]
    assert pedagogy.proxima_dica(multipla, len(multipla["dicas"])) is None
    assert pedagogy.dica_liberada(300, len(multipla["dicas"]), multipla) is False


# --- feedback ---

def test_quem_errou_ve_primeiro_por_que_a_escolha_dele_estava_errada(multipla):
    """A tela manda a linha clicada; a justificativa está indexada pelo arquivo."""
    mapa = pedagogy.mapa_de_exibicao(multipla)
    exibida_errada = mapa.index(2)

    blocos = pedagogy.feedback(multipla, escolha=exibida_errada, acertou=False)

    assert blocos[0][0] == "sua_escolha"
    assert blocos[0][1] == multipla["por_que_erradas"]["2"]
    assert blocos[1][0] == "explicacao"


def test_quem_acertou_ve_a_explicacao_e_depois_os_distratores(multipla):
    mapa = pedagogy.mapa_de_exibicao(multipla)
    blocos = pedagogy.feedback(multipla, escolha=mapa.index(multipla["correta"]),
                               acertou=True)

    assert blocos[0] == ("explicacao", multipla["explicacao"])
    assert [rotulo for rotulo, _ in blocos[1:]] == ["por_que_errada"] * 3


def test_feedback_de_questao_sem_alternativas_nao_quebra():
    questao = primeira_do_tipo("ordenacao")
    blocos = pedagogy.feedback(questao, escolha=None, acertou=False)
    assert blocos == [("explicacao", questao["explicacao"])]
