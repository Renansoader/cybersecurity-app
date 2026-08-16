"""Mapa dos níveis e módulos, com cadeado nos bloqueados."""

import customtkinter as ctk

from app import engine, theme


def montar(pai, app):
    theme.cabecalho(pai, "Trilha", "os seis níveis, do alicerce até carreira")
    corpo = theme.corpo_tela(pai)

    rolagem = ctk.CTkScrollableFrame(corpo, fg_color=theme.BG_PRIMARY)
    rolagem.pack(fill="both", expand=True)

    liberados = engine.niveis_desbloqueados(app.modulos, app.niveis)
    disponiveis = engine.modulos_disponiveis(app.modulos, app.niveis)

    for nivel in app.niveis:
        aberto = nivel["id"] in liberados
        modulos = sorted((m for m in app.modulos.values() if m["nivel"] == nivel["id"]),
                         key=lambda m: m["id"])
        _bloco_nivel(rolagem, app, nivel, modulos, aberto, disponiveis)


def _bloco_nivel(pai, app, nivel, modulos, aberto, disponiveis):
    card = theme.cartao(pai)
    card.pack(fill="x", pady=theme.PAD_LINHA)

    cadeado = "" if aberto else "🔒  "
    cor = theme.ACCENT if aberto else theme.BLOQUEADO
    ctk.CTkLabel(card, text=f"{cadeado}Nível {nivel['id']} — {nivel['nome']}",
                 font=theme.FONTE_CARTAO, text_color=cor, wraplength=740,
                 justify="left").pack(anchor="w", padx=theme.PAD_CARTAO,
                                      pady=(theme.PAD_CARTAO, 2))
    ctk.CTkLabel(card, text=_regra(nivel, aberto), font=theme.FONTE_LEGENDA,
                 text_color=theme.TEXT_MUTED, wraplength=740,
                 justify="left").pack(anchor="w", padx=theme.PAD_CARTAO, pady=(0, theme.GAP))

    if not modulos:
        ctk.CTkLabel(card, text="Conteúdo ainda não escrito.", font=theme.FONTE_CORPO,
                     text_color=theme.TEXT_MUTED).pack(anchor="w", padx=theme.PAD_CARTAO,
                                                       pady=(0, theme.PAD_CARTAO))
        return

    for modulo in modulos:
        _linha_modulo(card, app, modulo, aberto and modulo["id"] in disponiveis)
    ctk.CTkFrame(card, fg_color=theme.BG_CARD, height=theme.GAP).pack()


def _regra(nivel, aberto):
    regra = nivel["desbloqueio"]
    if regra["tipo"] == "aberto":
        return "Aberto desde o início."
    exigidos = ", ".join(str(n) for n in regra["niveis"])
    estado = "liberado" if aberto else "bloqueado"
    return f"Exige {regra['minimo']:.0%} de domínio médio no(s) nível(is) {exigidos} — {estado}."


def _linha_modulo(card, app, modulo, liberado):
    linha = ctk.CTkFrame(card, fg_color=theme.BG_SECONDARY, corner_radius=theme.CORNER_RADIUS)
    linha.pack(fill="x", padx=theme.PAD_CARTAO, pady=3)

    dominio = engine.dominio(modulo)
    concluido = engine.modulo_concluido(modulo)
    reforco = engine.modulo_em_reforco(modulo)

    marca = "✓" if concluido else ("!" if reforco else "")
    cor_marca = theme.SUCCESS if concluido else theme.DANGER
    ctk.CTkLabel(linha, text=marca, font=theme.FONTE_DESTAQUE, text_color=cor_marca,
                 width=20).pack(side="left", padx=(theme.GAP, 0), pady=10)

    ctk.CTkLabel(linha, text=f"{modulo['id']} — {modulo['titulo']}", font=theme.FONTE_CORPO,
                 text_color=theme.TEXT_PRIMARY if liberado else theme.TEXT_MUTED,
                 wraplength=380, justify="left").pack(side="left", padx=theme.GAP, pady=10)

    ctk.CTkButton(linha, text="Estudar" if liberado else "Bloqueado", width=100,
                  state="normal" if liberado else "disabled",
                  command=lambda: app.abrir_modulo(modulo["id"]),
                  **(theme.botao_primario() if liberado else theme.botao_secundario())
                  ).pack(side="right", padx=theme.GAP)

    ctk.CTkLabel(linha, text=f"{dominio:.0%}", font=theme.FONTE_LEGENDA,
                 text_color=theme.TEXT_MUTED, width=44).pack(side="right")
    barra = theme.barra_progresso(linha, dominio, width=150)
    barra.pack(side="right", padx=theme.GAP)
