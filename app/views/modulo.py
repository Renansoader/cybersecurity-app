"""Tela de um módulo: teoria em blocos e entrada para as questões."""

import customtkinter as ctk

from app import db, engine, theme
from app.views import sessao as tela_sessao


def montar(pai, app):
    modulo = app.modulos.get(app.modulo_atual)
    if modulo is None:
        theme.cabecalho(pai, "Módulo", "nenhum módulo selecionado")
        theme.cartao_em_construcao(theme.corpo_tela(pai), "Trilha",
                                   ["Escolha um módulo na tela Trilha"])
        return

    dominio = engine.dominio(modulo)
    theme.cabecalho(pai, f"{modulo['id']} — {modulo['titulo']}",
                    f"domínio {dominio:.0%} · {len(modulo['questoes'])} questões · "
                    f"{'concluído' if engine.modulo_concluido(modulo) else 'em andamento'}")
    corpo = theme.corpo_tela(pai)

    if app.aviso:
        ctk.CTkLabel(corpo, text=app.aviso, font=theme.FONTE_CORPO, text_color=theme.WARNING,
                     anchor="w").pack(anchor="w", pady=(0, theme.GAP))
        app.aviso = None   # some na próxima navegação

    abas = ctk.CTkTabview(corpo, fg_color=theme.BG_CARD, segmented_button_fg_color=theme.BG_SECONDARY,
                          segmented_button_selected_color=theme.ACCENT,
                          segmented_button_selected_hover_color=theme.ACCENT_HOVER,
                          text_color=theme.TEXT_PRIMARY, corner_radius=theme.CORNER_RADIUS)
    abas.pack(fill="both", expand=True)
    _teoria(abas.add("Teoria"), modulo)
    _questoes(abas.add("Questões"), app, modulo)


def _teoria(aba, modulo):
    rolagem = ctk.CTkScrollableFrame(aba, fg_color=theme.BG_CARD)
    rolagem.pack(fill="both", expand=True)

    ctk.CTkLabel(rolagem, text="Objetivos deste módulo", font=theme.FONTE_CARTAO,
                 text_color=theme.ACCENT).pack(anchor="w", pady=(0, theme.GAP))
    for objetivo in modulo["objetivos"]:
        ctk.CTkLabel(rolagem, text="•  " + objetivo, font=theme.FONTE_CORPO,
                     text_color=theme.TEXT_MUTED, wraplength=700,
                     justify="left").pack(anchor="w", pady=2)

    for bloco in modulo["teoria"]:
        card = ctk.CTkFrame(rolagem, fg_color=theme.BG_SECONDARY,
                            corner_radius=theme.CORNER_RADIUS)
        card.pack(fill="x", pady=(theme.PAD_CARTAO, 0))
        ctk.CTkLabel(card, text=bloco["titulo"], font=theme.FONTE_CARTAO,
                     text_color=theme.TEXT_PRIMARY, wraplength=700,
                     justify="left").pack(anchor="w", padx=theme.PAD_CARTAO,
                                          pady=(theme.PAD_CARTAO, theme.GAP))
        ctk.CTkLabel(card, text=bloco["texto"], font=theme.FONTE_CORPO,
                     text_color=theme.TEXT_PRIMARY, wraplength=700,
                     justify="left").pack(anchor="w", padx=theme.PAD_CARTAO, pady=(0, theme.GAP))
        for campo, rotulo, cor in (("analogia", "Analogia", theme.ACCENT),
                                   ("erro_comum", "Erro comum", theme.WARNING)):
            if bloco.get(campo):
                ctk.CTkLabel(card, text=f"{rotulo}: {bloco[campo]}", font=theme.FONTE_CORPO,
                             text_color=cor, wraplength=700,
                             justify="left").pack(anchor="w", padx=theme.PAD_CARTAO,
                                                  pady=(0, theme.GAP))
        ctk.CTkLabel(card, text=f"Fonte: {bloco['fonte']}", font=theme.FONTE_LEGENDA,
                     text_color=theme.TEXT_MUTED, wraplength=700,
                     justify="left").pack(anchor="w", padx=theme.PAD_CARTAO,
                                          pady=(0, theme.PAD_CARTAO))


def _questoes(aba, app, modulo):
    vistas = db.questoes_vistas(modulo["id"])
    total = len(modulo["questoes"])

    ctk.CTkLabel(aba, text=f"{len(vistas)} de {total} questões já respondidas."
                           " A primeira tentativa de cada uma é a que conta.",
                 font=theme.FONTE_CORPO, text_color=theme.TEXT_MUTED, wraplength=700,
                 justify="left").pack(anchor="w", pady=(theme.GAP, theme.GAP))

    ctk.CTkButton(aba, text="Estudar este módulo", height=40,
                  command=lambda: _abrir_sessao(app, modulo["id"]),
                  **theme.botao_primario()).pack(anchor="w")

    ctk.CTkLabel(aba, text="Refazer do zero apaga todas as tentativas deste módulo e zera a"
                          " estatística. É a única forma de melhorar um domínio ruim.",
                 font=theme.FONTE_LEGENDA, text_color=theme.WARNING, wraplength=700,
                 justify="left").pack(anchor="w", pady=(theme.PAD_CARTAO, theme.GAP))
    _botao_refazer(aba, app, modulo)


def _botao_refazer(aba, app, modulo):
    """Dois cliques para apagar, com saída no meio.

    Sem o Cancelar, um clique por engano deixa o botão armado até a próxima
    vez que alguém encostar nele — e a próxima vez apaga.
    """
    linha = theme.painel(aba)
    linha.configure(fg_color="transparent")
    linha.pack(anchor="w", fill="x")

    armado = {"sim": False}   # estado explícito: winfo_ismapped() só vale após um update
    botao = ctk.CTkButton(linha, text="Refazer módulo do zero", **theme.botao_secundario())
    botao.pack(side="left")
    cancelar = ctk.CTkButton(linha, text="Cancelar", **theme.botao_secundario())

    def desarmar():
        armado["sim"] = False
        cancelar.pack_forget()
        botao.configure(text="Refazer módulo do zero", **theme.botao_secundario())

    def clicar():
        if not armado["sim"]:
            armado["sim"] = True
            vistas = len(db.questoes_vistas(modulo["id"]))
            botao.configure(text=f"Apagar {vistas} tentativa(s) e zerar? Clique de novo",
                            fg_color=theme.DANGER, hover_color=theme.DANGER,
                            text_color=theme.BG_PRIMARY)
            cancelar.pack(side="left", padx=theme.GAP)
            return
        db.apagar_tentativas_modulo(modulo["id"])
        app.abrir_modulo(modulo["id"],
                         aviso=f"Tentativas do módulo {modulo['id']} apagadas."
                               " O domínio voltou a zero.")

    botao.configure(command=clicar)
    cancelar.configure(command=desarmar)


def _abrir_sessao(app, modulo_id):
    """Sessão restrita a um módulo, sem passar pela seleção do motor."""
    app.ir_para("Sessão diária")
    for widget in app.corpo.winfo_children():
        widget.destroy()
    tela_sessao.Sessao(app.corpo, app, modulo_id=modulo_id)
