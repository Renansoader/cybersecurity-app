"""Sessão diária: uma questão por tela, com o fluxo socrático inteiro.

Estados de uma questão nova ou em revisão:
    respondendo -> socratica -> resultado

A dica só aparece depois de 20 segundos, a pergunta socrática entra entre o
"Confirmar" e o resultado, e o gabarito só é montado no estado de resultado.
Nada nesta tela lê `correta`, `ordem_correta` ou `pares`: a correção é
delegada a pedagogy.conferir().
"""

import customtkinter as ctk

from app import db, engine, pedagogy, theme

INTERVALO_CRONOMETRO = 1000  # ms


def montar(pai, app):
    Sessao(pai, app)


class Sessao:
    def __init__(self, pai, app, modulo_id=None):
        self.pai = pai
        self.app = app
        self.fila = self._montar_fila(modulo_id)
        self.indice = 0
        self.acertos = 0
        self.cronometro = None

        self.cabecalho = theme.painel(pai)
        self.cabecalho.pack(fill="x", padx=theme.PAD_TELA, pady=(theme.PAD_TELA, 0))
        self.rotulo_progresso = ctk.CTkLabel(self.cabecalho, text="", font=theme.FONTE_LEGENDA,
                                             text_color=theme.TEXT_MUTED)
        self.rotulo_progresso.pack(side="left")
        self.rotulo_tempo = ctk.CTkLabel(self.cabecalho, text="", font=theme.FONTE_LEGENDA,
                                         text_color=theme.TEXT_MUTED)
        self.rotulo_tempo.pack(side="right")

        self.corpo = theme.corpo_tela(pai)
        self._proxima()

    def _montar_fila(self, modulo_id):
        if modulo_id:
            modulo = self.app.modulos.get(modulo_id)
            return [(modulo_id, q) for q in modulo["questoes"]] if modulo else []
        return engine.montar_sessao(self.app.modulos, self.app.niveis,
                                    meta=engine.meta_diaria())

    # --- ciclo ---

    def _limpar(self):
        if self.cronometro:
            self.pai.after_cancel(self.cronometro)
            self.cronometro = None
        for widget in self.corpo.winfo_children():
            widget.destroy()

    def _proxima(self):
        self._limpar()
        if self.indice >= len(self.fila):
            return self._fim()

        self.modulo_id, self.questao = self.fila[self.indice]
        self.visivel = pedagogy.questao_para_exibir(self.questao)
        self.modo = engine.modo_da_questao(self.questao["id"])
        self.resposta = None
        self.dicas_pedidas = 0
        self.segundos = 0

        self.rotulo_progresso.configure(
            text=f"Questão {self.indice + 1} de {len(self.fila)}  ·  módulo {self.modulo_id}"
                 f"  ·  {self._rotulo_modo()}")
        self._desenhar_questao()
        if self.modo != "leitura":
            self._tique()

    def _rotulo_modo(self):
        return {"nova": "conteúdo novo", "revisao": "revisão vencida",
                "leitura": "modo leitura"}[self.modo]

    def _tique(self):
        self.segundos += 1
        self.rotulo_tempo.configure(text=f"{self.segundos // 60:02d}:{self.segundos % 60:02d}")
        if self.botao_dica and not self.botao_dica.winfo_ismapped():
            if pedagogy.dica_liberada(self.segundos, self.dicas_pedidas, self.questao):
                self.botao_dica.pack(anchor="w", pady=(theme.GAP, 0))
        self.cronometro = self.pai.after(INTERVALO_CRONOMETRO, self._tique)

    # --- estado 1: respondendo ---

    def _desenhar_questao(self):
        card = theme.cartao(self.corpo)
        card.pack(fill="both", expand=True)
        self.dentro = card

        if self.modo == "leitura":
            self._faixa_leitura(card)

        ctk.CTkLabel(card, text=self.visivel["enunciado"], font=theme.FONTE_CARTAO,
                     text_color=theme.TEXT_PRIMARY, wraplength=760,
                     justify="left").pack(anchor="w", padx=theme.PAD_CARTAO,
                                          pady=(theme.PAD_CARTAO, theme.GAP))

        for campo in ("artefato", "trecho"):
            if campo in self.visivel:
                caixa = ctk.CTkTextbox(card, height=140, fg_color=theme.BG_SECONDARY,
                                       text_color=theme.TEXT_PRIMARY, font=theme.code_font(11),
                                       corner_radius=theme.CORNER_RADIUS)
                caixa.insert("1.0", self.visivel[campo])
                caixa.configure(state="disabled")
                caixa.pack(fill="x", padx=theme.PAD_CARTAO, pady=(0, theme.GAP))

        self.area_resposta = theme.painel(card)
        self.area_resposta.configure(fg_color=theme.BG_CARD)
        self.area_resposta.pack(fill="x", padx=theme.PAD_CARTAO)
        self._montar_resposta()

        self.area_dicas = theme.painel(card)
        self.area_dicas.configure(fg_color=theme.BG_CARD)
        self.area_dicas.pack(fill="x", padx=theme.PAD_CARTAO, pady=(theme.GAP, 0))

        rodape = theme.painel(card)
        rodape.configure(fg_color=theme.BG_CARD)
        rodape.pack(fill="x", padx=theme.PAD_CARTAO, pady=theme.PAD_CARTAO)

        if self.modo == "leitura":
            self.botao_dica = None
            ctk.CTkButton(rodape, text="Próxima", command=self._avancar,
                          **theme.botao_primario()).pack(side="left")
            self._mostrar_feedback(card, ja_respondida=True)
            return

        self.botao_confirmar = ctk.CTkButton(rodape, text="Confirmar", command=self._confirmar,
                                             **theme.botao_primario())
        self.botao_confirmar.pack(side="left")
        # o botão de dica nasce escondido; o cronômetro o revela aos 20 segundos
        self.botao_dica = ctk.CTkButton(self.area_dicas, text="Preciso de uma dica",
                                        command=self._pedir_dica, **theme.botao_secundario())

    def _faixa_leitura(self, card):
        tentativa = db.primeira_tentativa(self.questao["id"])
        resultado = "acertou" if tentativa["acertou"] else "errou"
        ajuda = " (com dica)" if tentativa["usou_dica"] else ""
        ctk.CTkLabel(card, text=f"Você já respondeu esta questão em {tentativa['data']} — "
                               f"{resultado}{ajuda}. A tentativa registrada é imutável.",
                     font=theme.FONTE_LEGENDA, text_color=theme.WARNING,
                     wraplength=760, justify="left").pack(anchor="w", padx=theme.PAD_CARTAO,
                                                          pady=(theme.PAD_CARTAO, 0))

    def _montar_resposta(self):
        tipo = self.questao["tipo"]
        somente_leitura = self.modo == "leitura"

        if tipo == "ordenacao":
            self.widget_resposta = Ordenacao(self.area_resposta, self.visivel["itens"],
                                             somente_leitura)
        elif tipo == "pareamento":
            self.widget_resposta = Pareamento(self.area_resposta,
                                              self.visivel["coluna_esquerda"],
                                              self.visivel["coluna_direita"], somente_leitura)
        else:
            self.widget_resposta = Alternativas(self.area_resposta, self.visivel["alternativas"],
                                                somente_leitura)

    # --- dicas ---

    def _pedir_dica(self):
        dica = pedagogy.proxima_dica(self.questao, self.dicas_pedidas)
        if dica is None:
            return
        self.dicas_pedidas += 1
        ctk.CTkLabel(self.area_dicas, text=f"Dica {self.dicas_pedidas}: {dica}",
                     font=theme.FONTE_CORPO, text_color=theme.WARNING, wraplength=740,
                     justify="left").pack(anchor="w", pady=(theme.GAP, 0))
        if self.dicas_pedidas >= len(self.questao["dicas"]):
            self.botao_dica.pack_forget()

    # --- estado 2: pergunta socrática ---

    def _confirmar(self):
        resposta = self.widget_resposta.resposta()
        if resposta is None:
            self.botao_confirmar.configure(text="Escolha uma resposta primeiro")
            return
        self.resposta = resposta
        self.widget_resposta.travar()
        self.botao_confirmar.pack_forget()
        if self.botao_dica:
            self.botao_dica.pack_forget()

        self.caixa_socratica = theme.cartao(self.dentro)
        self.caixa_socratica.configure(fg_color=theme.BG_SECONDARY)
        self.caixa_socratica.pack(fill="x", padx=theme.PAD_CARTAO, pady=(theme.GAP, 0))
        ctk.CTkLabel(self.caixa_socratica, text=pedagogy.pergunta_socratica(self.questao),
                     font=theme.FONTE_CORPO, text_color=theme.TEXT_PRIMARY, wraplength=720,
                     justify="left").pack(anchor="w", padx=theme.PAD_CARTAO,
                                          pady=(theme.PAD_CARTAO, theme.GAP))
        linha = theme.painel(self.caixa_socratica)
        linha.configure(fg_color=theme.BG_SECONDARY)
        linha.pack(fill="x", padx=theme.PAD_CARTAO, pady=(0, theme.PAD_CARTAO))
        ctk.CTkButton(linha, text="Pensei — ver resultado", command=self._revelar,
                      **theme.botao_primario()).pack(side="left")
        ctk.CTkButton(linha, text="Voltar e revisar", command=self._voltar_a_responder,
                      **theme.botao_secundario()).pack(side="left", padx=theme.GAP)

    def _voltar_a_responder(self):
        self.caixa_socratica.destroy()
        self.widget_resposta.destravar()
        self.botao_confirmar.configure(text="Confirmar")
        self.botao_confirmar.pack(side="left")
        if self.botao_dica and pedagogy.dica_liberada(self.segundos, self.dicas_pedidas,
                                                      self.questao):
            self.botao_dica.pack(anchor="w", pady=(theme.GAP, 0))

    # --- estado 3: resultado ---

    def _revelar(self):
        if self.cronometro:
            self.pai.after_cancel(self.cronometro)
            self.cronometro = None
        self.caixa_socratica.destroy()

        acertou = pedagogy.conferir(self.questao, self.resposta)
        engine.responder(self.questao, self.modulo_id, acertou,
                         usou_dica=self.dicas_pedidas > 0, segundos=self.segundos)
        self.acertos += int(acertou)
        self._mostrar_feedback(self.dentro, acertou=acertou)

    def _mostrar_feedback(self, card, acertou=None, ja_respondida=False):
        if ja_respondida:
            tentativa = db.primeira_tentativa(self.questao["id"])
            acertou = bool(tentativa["acertou"])
            escolha = None
        else:
            escolha = self.resposta

        faixa = theme.cartao(card)
        faixa.configure(fg_color=theme.BG_SECONDARY)
        faixa.pack(fill="x", padx=theme.PAD_CARTAO, pady=(theme.GAP, 0))
        ctk.CTkLabel(faixa, text="Acertou" if acertou else "Errou", font=theme.FONTE_CARTAO,
                     text_color=theme.SUCCESS if acertou else theme.DANGER).pack(
            anchor="w", padx=theme.PAD_CARTAO, pady=(theme.PAD_CARTAO, theme.GAP))

        for rotulo, texto in pedagogy.feedback(self.questao, escolha, acertou):
            cor = {"sua_escolha": theme.DANGER, "explicacao": theme.TEXT_PRIMARY}.get(
                rotulo, theme.TEXT_MUTED)
            ctk.CTkLabel(faixa, text=texto, font=theme.FONTE_CORPO, text_color=cor,
                         wraplength=720, justify="left").pack(anchor="w", padx=theme.PAD_CARTAO,
                                                              pady=(0, theme.GAP))

        ctk.CTkLabel(faixa, text=f"Fonte: {self.questao['fonte']}", font=theme.FONTE_LEGENDA,
                     text_color=theme.TEXT_MUTED, wraplength=720,
                     justify="left").pack(anchor="w", padx=theme.PAD_CARTAO,
                                          pady=(0, theme.PAD_CARTAO))

        if not ja_respondida:
            ctk.CTkButton(faixa, text="Próxima", command=self._avancar,
                          **theme.botao_primario()).pack(anchor="w", padx=theme.PAD_CARTAO,
                                                         pady=(0, theme.PAD_CARTAO))

    def _avancar(self):
        self.indice += 1
        self._proxima()

    def _fim(self):
        self.rotulo_progresso.configure(text="Sessão concluída")
        self.rotulo_tempo.configure(text="")
        card = theme.cartao(self.corpo)
        card.pack(fill="x")
        total = len(self.fila)
        ctk.CTkLabel(card, text=f"{self.acertos} de {total} nesta sessão",
                     font=theme.FONTE_CARTAO, text_color=theme.TEXT_PRIMARY).pack(
            anchor="w", padx=theme.PAD_CARTAO, pady=(theme.PAD_CARTAO, theme.GAP))
        respondidas, _, minutos = engine.resumo_do_dia()
        ctk.CTkLabel(card, text=f"Hoje: {respondidas} questões, {minutos} min · "
                               f"meta diária {engine.meta_diaria()}",
                     font=theme.FONTE_CORPO, text_color=theme.TEXT_MUTED).pack(
            anchor="w", padx=theme.PAD_CARTAO, pady=(0, theme.GAP))
        ctk.CTkButton(card, text="Voltar ao início", command=lambda: self.app.ir_para("Início"),
                      **theme.botao_primario()).pack(anchor="w", padx=theme.PAD_CARTAO,
                                                     pady=(0, theme.PAD_CARTAO))
        engine.sincronizar_status(self.app.modulos, self.app.niveis)


# --- widgets de resposta ---------------------------------------------------
# ponytail: sem arrastar e soltar. Botões de subir/descer e seleção por menu
# são feios e sólidos; arrastar em Tk é bonito e quebra. Trocar quando alguém
# reclamar do número de cliques, não antes.

class Alternativas:
    """Linhas clicáveis. CTkButton não quebra linha, e alternativa longa precisa."""

    def __init__(self, pai, alternativas, somente_leitura):
        self.escolhida = None
        self.travado = somente_leitura
        self.linhas = []

        for indice, texto in enumerate(alternativas):
            linha = ctk.CTkFrame(pai, fg_color=theme.BG_SECONDARY,
                                 corner_radius=theme.CORNER_RADIUS)
            linha.pack(fill="x", pady=3)
            numero = ctk.CTkLabel(linha, text=f"{indice + 1}", font=theme.FONTE_DESTAQUE,
                                  text_color=theme.ACCENT, width=24)
            numero.pack(side="left", padx=(theme.GAP, 0), pady=10)
            rotulo = ctk.CTkLabel(linha, text=texto, font=theme.FONTE_CORPO,
                                  text_color=theme.TEXT_PRIMARY, wraplength=660, justify="left")
            rotulo.pack(side="left", padx=theme.GAP, pady=10, anchor="w")

            for widget in (linha, numero, rotulo):
                widget.bind("<Button-1>", lambda _evento, i=indice: self._escolher(i))
            self.linhas.append((linha, numero, rotulo))

    def _escolher(self, indice):
        if self.travado:
            return
        self.escolhida = indice
        for i, (linha, numero, rotulo) in enumerate(self.linhas):
            ativo = i == indice
            linha.configure(fg_color=theme.ACCENT if ativo else theme.BG_SECONDARY)
            numero.configure(text_color=theme.BG_PRIMARY if ativo else theme.ACCENT)
            rotulo.configure(text_color=theme.BG_PRIMARY if ativo else theme.TEXT_PRIMARY)

    def resposta(self):
        return self.escolhida

    def travar(self):
        self.travado = True

    def destravar(self):
        self.travado = False


class Ordenacao:
    """Lista reordenável por botões de subir e descer."""

    def __init__(self, pai, itens, somente_leitura):
        self.posicoes = list(range(len(itens)))   # posições exibidas, na ordem montada
        self.itens = itens
        self.pai = pai
        self.somente_leitura = somente_leitura
        self.area = theme.painel(pai)
        self.area.configure(fg_color=theme.BG_CARD)
        self.area.pack(fill="x")
        self._redesenhar()

    def _redesenhar(self):
        for widget in self.area.winfo_children():
            widget.destroy()
        for lugar, posicao in enumerate(self.posicoes):
            linha = ctk.CTkFrame(self.area, fg_color=theme.BG_SECONDARY,
                                 corner_radius=theme.CORNER_RADIUS)
            linha.pack(fill="x", pady=3)
            ctk.CTkLabel(linha, text=f"{lugar + 1}", font=theme.FONTE_DESTAQUE,
                         text_color=theme.ACCENT, width=28).pack(side="left", padx=(theme.GAP, 0))
            ctk.CTkLabel(linha, text=self.itens[posicao], font=theme.FONTE_CORPO,
                         text_color=theme.TEXT_PRIMARY, wraplength=580,
                         justify="left").pack(side="left", padx=theme.GAP, pady=8, expand=True,
                                              anchor="w")
            if not self.somente_leitura:
                ctk.CTkButton(linha, text="▼", width=34, command=lambda i=lugar: self._mover(i, 1),
                              **theme.botao_secundario()).pack(side="right", padx=(0, theme.GAP))
                ctk.CTkButton(linha, text="▲", width=34, command=lambda i=lugar: self._mover(i, -1),
                              **theme.botao_secundario()).pack(side="right", padx=4)

    def _mover(self, lugar, passo):
        destino = lugar + passo
        if 0 <= destino < len(self.posicoes):
            self.posicoes[lugar], self.posicoes[destino] = (self.posicoes[destino],
                                                            self.posicoes[lugar])
            self._redesenhar()

    def resposta(self):
        return list(self.posicoes)

    def travar(self):
        self.somente_leitura = True
        self._redesenhar()

    def destravar(self):
        self.somente_leitura = False
        self._redesenhar()


class Pareamento:
    """Um menu por linha da esquerda, escolhendo o item da direita."""

    def __init__(self, pai, esquerda, direita, somente_leitura):
        self.direita = direita
        self.menus = []
        for texto in esquerda:
            linha = ctk.CTkFrame(pai, fg_color=theme.BG_SECONDARY,
                                 corner_radius=theme.CORNER_RADIUS)
            linha.pack(fill="x", pady=3)
            ctk.CTkLabel(linha, text=texto, font=theme.FONTE_CORPO,
                         text_color=theme.TEXT_PRIMARY, width=200, wraplength=200,
                         justify="left", anchor="w").pack(side="left", padx=theme.GAP, pady=8)
            menu = ctk.CTkOptionMenu(linha, values=["escolha..."] + list(direita),
                                     width=520, font=theme.FONTE_CORPO,
                                     fg_color=theme.BG_CARD, button_color=theme.ACCENT,
                                     button_hover_color=theme.ACCENT_HOVER,
                                     text_color=theme.TEXT_PRIMARY,
                                     dropdown_font=theme.FONTE_CORPO)
            menu.set("escolha...")
            menu.pack(side="left", padx=(0, theme.GAP), pady=8)
            self.menus.append(menu)
        if somente_leitura:
            self.travar()

    def resposta(self):
        escolhas = []
        for menu in self.menus:
            valor = menu.get()
            if valor == "escolha...":
                return None
            escolhas.append(self.direita.index(valor))
        return escolhas

    def travar(self):
        for menu in self.menus:
            menu.configure(state="disabled")

    def destravar(self):
        for menu in self.menus:
            menu.configure(state="normal")
