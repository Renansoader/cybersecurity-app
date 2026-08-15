"""Tela de estudo de um módulo: abas de teoria e de questões."""

from app import theme


def montar(pai, app):
    theme.cabecalho(pai, "Módulo", "teoria em blocos curtos e as questões do módulo")
    corpo = theme.corpo_tela(pai)

    theme.cartao_em_construcao(corpo, "Fase 4", [
        "Aba Teoria: blocos de no máximo 8 linhas, com analogia e erro comum",
        "Aba Questões: uma por vez, seguindo o fluxo socrático",
        "Barra de domínio do módulo no topo",
        "Botão \"Refazer módulo do zero\", que avisa antes de zerar a estatística",
    ])
