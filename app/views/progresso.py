"""Estatísticas: heatmap anual, domínio por nível e desempenho por tag."""

import tkinter as tk
from datetime import date, timedelta

import customtkinter as ctk

from app import db, engine, theme

LADO = 11        # lado de cada quadradinho do heatmap, em pixels
ESPACO = 3
SEMANAS = 53


def montar(pai, app):
    theme.cabecalho(pai, "Progresso", "só a primeira tentativa conta no domínio")
    corpo = theme.corpo_tela(pai)
    rolagem = ctk.CTkScrollableFrame(corpo, fg_color=theme.BG_PRIMARY)
    rolagem.pack(fill="both", expand=True)

    _heatmap(rolagem)
    _dominio_por_nivel(rolagem, app)
    _desempenho_por_tag(rolagem, app)


def _heatmap(pai):
    card = theme.cartao(pai)
    card.pack(fill="x")
    ctk.CTkLabel(card, text="Um ano de estudo", font=theme.FONTE_CARTAO,
                 text_color=theme.TEXT_PRIMARY).pack(anchor="w", padx=theme.PAD_CARTAO,
                                                     pady=(theme.PAD_CARTAO, theme.GAP))

    hoje = date.today()
    inicio = hoje - timedelta(days=SEMANAS * 7 - 1)
    inicio -= timedelta(days=(inicio.weekday() + 1) % 7)   # começa no domingo
    atividade = db.atividade_por_dia(inicio.isoformat())
    meta = engine.meta_diaria()

    largura = SEMANAS * (LADO + ESPACO)
    tela = tk.Canvas(card, width=largura, height=7 * (LADO + ESPACO), bg=theme.BG_CARD,
                     highlightthickness=0)
    tela.pack(anchor="w", padx=theme.PAD_CARTAO)

    total = 0
    for semana in range(SEMANAS):
        for dia_semana in range(7):
            dia = inicio + timedelta(days=semana * 7 + dia_semana)
            if dia > hoje:
                continue
            n = atividade.get(dia.isoformat(), {}).get("n", 0)
            total += n
            x = semana * (LADO + ESPACO)
            y = dia_semana * (LADO + ESPACO)
            tela.create_rectangle(x, y, x + LADO, y + LADO, fill=_cor(n, meta), width=0)

    ctk.CTkLabel(card, text=f"{total} questões respondidas no período · meta diária {meta}",
                 font=theme.FONTE_LEGENDA, text_color=theme.TEXT_MUTED).pack(
        anchor="w", padx=theme.PAD_CARTAO, pady=(theme.GAP, theme.PAD_CARTAO))


def _cor(n, meta):
    if n == 0:
        return theme.BG_SECONDARY
    if n < meta / 2:
        return "#2c4a2c"
    if n < meta:
        return "#4d7c3f"
    return theme.SUCCESS


def _dominio_por_nivel(pai, app):
    card = theme.cartao(pai)
    card.pack(fill="x", pady=(theme.PAD_LINHA, 0))
    ctk.CTkLabel(card, text="Domínio por nível", font=theme.FONTE_CARTAO,
                 text_color=theme.TEXT_PRIMARY).pack(anchor="w", padx=theme.PAD_CARTAO,
                                                     pady=(theme.PAD_CARTAO, theme.GAP))

    liberados = engine.niveis_desbloqueados(app.modulos, app.niveis)
    for nivel in app.niveis:
        modulos = [m for m in app.modulos.values() if m["nivel"] == nivel["id"]]
        if not modulos:
            continue
        media = sum(engine.dominio(m) for m in modulos) / len(modulos)
        linha = ctk.CTkFrame(card, fg_color=theme.BG_SECONDARY,
                             corner_radius=theme.CORNER_RADIUS)
        linha.pack(fill="x", padx=theme.PAD_CARTAO, pady=3)
        rotulo = f"{'' if nivel['id'] in liberados else '🔒 '}Nível {nivel['id']}"
        ctk.CTkLabel(linha, text=rotulo, font=theme.FONTE_CORPO, text_color=theme.TEXT_PRIMARY,
                     width=90).pack(side="left", padx=theme.GAP, pady=10)
        ctk.CTkLabel(linha, text=f"{media:.0%}", font=theme.FONTE_DESTAQUE,
                     text_color=theme.ACCENT, width=54).pack(side="right", padx=theme.GAP)
        theme.barra_progresso(linha, media, width=420).pack(side="right")
    ctk.CTkFrame(card, fg_color=theme.BG_CARD, height=theme.GAP).pack()


def _desempenho_por_tag(pai, app):
    card = theme.cartao(pai)
    card.pack(fill="x", pady=(theme.PAD_LINHA, 0))
    ctk.CTkLabel(card, text="Tópicos mais fracos", font=theme.FONTE_CARTAO,
                 text_color=theme.TEXT_PRIMARY).pack(anchor="w", padx=theme.PAD_CARTAO,
                                                     pady=(theme.PAD_CARTAO, theme.GAP))

    desempenho = engine.desempenho_por_tag(app.modulos)
    if not desempenho:
        ctk.CTkLabel(card, text="Responda algumas questões para o desempenho por tópico aparecer.",
                     font=theme.FONTE_CORPO, text_color=theme.TEXT_MUTED).pack(
            anchor="w", padx=theme.PAD_CARTAO, pady=(0, theme.PAD_CARTAO))
        return

    piores = sorted(desempenho.items(), key=lambda par: par[1])[:8]
    for tag, media in piores:
        cor = theme.DANGER if media < 0.6 else theme.WARNING if media < 0.8 else theme.SUCCESS
        theme.linha_valor(card, tag, f"{media:.0%}", cor_valor=cor)
    ctk.CTkFrame(card, fg_color=theme.BG_CARD, height=theme.GAP).pack()
