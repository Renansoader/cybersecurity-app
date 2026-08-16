"""Dashboard: streak, meta diária, pontos fracos e o botão que decide por você."""

import customtkinter as ctk

from app import engine, theme


def montar(pai, app):
    theme.cabecalho(pai, "Início", "streak, meta do dia e o que estudar agora")
    corpo = theme.corpo_tela(pai)

    respondidas, acertos, minutos = engine.resumo_do_dia()
    meta = engine.meta_diaria()
    dias = engine.streak()

    topo = theme.cartao(corpo)
    topo.pack(fill="x")
    ctk.CTkLabel(topo, text=f"{dias} dia(s) seguidos com a meta batida" if dias
                            else "Nenhum dia seguido ainda — bata a meta de hoje para começar",
                 font=theme.FONTE_CARTAO, text_color=theme.SUCCESS if dias else theme.TEXT_MUTED
                 ).pack(anchor="w", padx=theme.PAD_CARTAO, pady=(theme.PAD_CARTAO, theme.GAP))

    barra = theme.barra_progresso(topo, min(respondidas / meta, 1.0) if meta else 0)
    barra.pack(fill="x", padx=theme.PAD_CARTAO)
    ctk.CTkLabel(topo, text=f"Hoje: {respondidas} de {meta} questões · {acertos} acertos"
                            f" · {minutos} min", font=theme.FONTE_LEGENDA,
                 text_color=theme.TEXT_MUTED).pack(anchor="w", padx=theme.PAD_CARTAO,
                                                   pady=(6, theme.GAP))

    acoes = theme.painel(topo)
    acoes.configure(fg_color=theme.BG_CARD)
    acoes.pack(fill="x", padx=theme.PAD_CARTAO, pady=(0, theme.PAD_CARTAO))
    ctk.CTkButton(acoes, text="Estudar agora", height=44, width=200,
                  command=lambda: app.ir_para("Sessão diária"),
                  **theme.botao_primario()).pack(side="left")

    ctk.CTkLabel(acoes, text="Meta:", font=theme.FONTE_CORPO,
                 text_color=theme.TEXT_MUTED).pack(side="left", padx=(theme.PAD_CARTAO, theme.GAP))
    for valor in engine.METAS:
        ativo = valor == meta
        ctk.CTkButton(acoes, text=str(valor), width=48,
                      command=lambda v=valor: _trocar_meta(app, v),
                      **(theme.botao_primario() if ativo else theme.botao_secundario())
                      ).pack(side="left", padx=3)

    _pontos_fracos(corpo, app)
    _proximo_modulo(corpo, app)


def _trocar_meta(app, valor):
    from app import db
    db.salvar_preferencia("meta_diaria", valor)
    app.ir_para("Início")


def _pontos_fracos(corpo, app):
    fracos = engine.pontos_fracos(app.modulos)
    card = theme.cartao(corpo)
    card.pack(fill="x", pady=(theme.PAD_LINHA, 0))
    ctk.CTkLabel(card, text="Pontos fracos da semana", font=theme.FONTE_CARTAO,
                 text_color=theme.TEXT_PRIMARY).pack(anchor="w", padx=theme.PAD_CARTAO,
                                                     pady=(theme.PAD_CARTAO, theme.GAP))
    if not fracos:
        ctk.CTkLabel(card, text="Ainda sem amostra suficiente. Um módulo entra aqui depois de"
                               " 30% das questões respondidas.", font=theme.FONTE_CORPO,
                     text_color=theme.TEXT_MUTED, wraplength=700,
                     justify="left").pack(anchor="w", padx=theme.PAD_CARTAO,
                                          pady=(0, theme.PAD_CARTAO))
        return
    from app import db
    for mid in fracos:
        modulo = app.modulos[mid]
        theme.linha_valor(card, f"{mid} — {modulo['titulo']}",
                          f"{db.dominio_sobre_vistas(mid):.0%}", cor_valor=theme.DANGER)
    ctk.CTkFrame(card, fg_color=theme.BG_CARD, height=theme.GAP).pack()


def _proximo_modulo(corpo, app):
    disponiveis = engine.modulos_disponiveis(app.modulos, app.niveis)
    pendentes = [m for m in disponiveis.values() if not engine.modulo_concluido(m)]
    if not pendentes:
        return
    proximo = sorted(pendentes, key=lambda m: m["id"])[0]
    card = theme.cartao(corpo)
    card.pack(fill="x", pady=(theme.PAD_LINHA, 0))
    ctk.CTkLabel(card, text="Próximo módulo sugerido", font=theme.FONTE_CARTAO,
                 text_color=theme.TEXT_PRIMARY).pack(anchor="w", padx=theme.PAD_CARTAO,
                                                     pady=(theme.PAD_CARTAO, 2))
    ctk.CTkLabel(card, text=f"{proximo['id']} — {proximo['titulo']}", font=theme.FONTE_CORPO,
                 text_color=theme.TEXT_MUTED).pack(anchor="w", padx=theme.PAD_CARTAO,
                                                   pady=(0, theme.GAP))
    ctk.CTkButton(card, text="Abrir módulo", command=lambda: app.abrir_modulo(proximo["id"]),
                  **theme.botao_secundario()).pack(anchor="w", padx=theme.PAD_CARTAO,
                                                   pady=(0, theme.PAD_CARTAO))
