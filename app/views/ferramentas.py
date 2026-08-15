"""Catálogo de ferramentas por categoria. Modo consulta, sem pontuação."""

from app import theme


def montar(pai, app):
    theme.cabecalho(pai, "Ferramentas", "catálogo por categoria, com alerta de uso legal")
    corpo = theme.corpo_tela(pai)

    theme.cartao_em_construcao(corpo, "Fase 6", [
        "As nove categorias do infográfico de referência",
        "Para que serve e quando usar cada ferramenta",
        "Alerta de uso legal: só com autorização por escrito e escopo definido",
    ])
