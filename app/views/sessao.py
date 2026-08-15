"""Sessão diária: mistura de revisão vencida no SRS e conteúdo novo."""

from app import theme


def montar(pai, app):
    theme.cabecalho(pai, "Sessão diária", "60% revisão vencida, 40% conteúdo novo")
    corpo = theme.corpo_tela(pai)

    theme.cartao_em_construcao(corpo, "Fase 5", [
        "Uma questão por tela, sem rolagem para ver as alternativas",
        "Dica só aparece depois de 20 segundos, e uma por clique",
        "Pergunta socrática antes de revelar o resultado",
        "Cronômetro discreto e progresso da sessão no topo",
        "Teclado: 1-4 escolhem, Enter confirma, D pede dica, Esc sai",
    ])
