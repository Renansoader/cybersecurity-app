"""Glossário pesquisável de termos. Modo consulta, sem pontuação."""

from app import theme


def montar(pai, app):
    theme.cabecalho(pai, "Glossário", "consulta livre, sem pontuação")
    corpo = theme.corpo_tela(pai)

    theme.cartao_em_construcao(corpo, "Fase 6", [
        "Busca instantânea conforme você digita",
        "Termo em português e em inglês",
        "Definição curta e o módulo onde o termo aparece",
    ])
