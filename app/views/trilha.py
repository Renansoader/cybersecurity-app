"""Mapa dos níveis e módulos, com cadeado nos bloqueados."""

import customtkinter as ctk

from app import theme


def montar(pai, app):
    theme.cabecalho(pai, "Trilha", "os seis níveis, do alicerce até carreira")
    corpo = theme.corpo_tela(pai)

    theme.cartao_em_construcao(corpo, "Fase 5", [
        "Mapa vertical dos níveis, com os módulos como cartões",
        "Cadeado nos níveis ainda bloqueados",
        "Barra de domínio em cada módulo",
        "Níveis 3 e 4 lado a lado: dá para escolher ofensivo ou defensivo",
    ])

    # a lista de níveis e módulos vem de data/niveis.json na Fase 2;
    # por enquanto, só o caminho de navegação até a tela de módulo
    ctk.CTkButton(corpo, text="Abrir tela de módulo", width=200,
                  command=lambda: app.ir_para("Módulo"),
                  **theme.botao_secundario()).pack(anchor="w", pady=(theme.GAP, 0))
