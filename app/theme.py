"""Paleta, tipografia e componentes visuais do app.

Cores e fontes copiadas do fullstack-study-app (tema escuro, estilo Tokyo Night).
Os helpers no fim do arquivo concentram os padroes que la ficavam repetidos a mao
dentro de cada tela: cartao, cabecalho, botao primario/secundario, linha de
rotulo + valor e barra de progresso.
"""

import customtkinter as ctk

# --- cores (identicas as do fullstack-study-app) ---
BG_PRIMARY = "#1a1b26"
BG_SECONDARY = "#24283b"
BG_CARD = "#1f2335"

ACCENT = "#7aa2f7"
ACCENT_HOVER = "#5d7fd6"

SUCCESS = "#9ece6a"
WARNING = "#e0af68"
DANGER = "#f7768e"

TEXT_PRIMARY = "#c0caf5"
TEXT_MUTED = "#565f89"

# item bloqueado na trilha (cadeado)
BLOQUEADO = "#3b4261"

FONT_FAMILY = "Segoe UI"
CODE_FONT_FAMILY = "Consolas"

CORNER_RADIUS = 12


def font(size, weight="normal"):
    return (FONT_FAMILY, size, weight)


def code_font(size=11):
    return (CODE_FONT_FAMILY, size)


# --- tipografia: os tamanhos ja usados no outro app, agora com nome ---
FONTE_TITULO = font(24, "bold")    # marca / titulo grande
FONTE_SECAO = font(18, "bold")     # cabecalho de tela
FONTE_CARTAO = font(15, "bold")    # titulo dentro de um cartao
FONTE_DESTAQUE = font(13, "bold")  # valor numerico em destaque
FONTE_CORPO = font(13)
FONTE_LEGENDA = font(11)

# --- espacamento: os valores que as telas do fullstack repetiam ---
PAD_TELA = 20      # respiro contra as bordas da janela
PAD_CARTAO = 20    # respiro interno de um cartao
PAD_LINHA = 6      # entre cartoes empilhados
GAP = 10

LARGURA_SIDEBAR = 230
JANELA_MIN = (1100, 720)


# --- kwargs de botao ---
def botao_primario():
    """Acao principal da tela: fundo accent."""
    return dict(corner_radius=CORNER_RADIUS, fg_color=ACCENT, hover_color=ACCENT_HOVER,
                text_color=BG_PRIMARY, font=FONTE_CORPO)


def botao_secundario():
    """Acao de apoio: fundo discreto."""
    return dict(corner_radius=CORNER_RADIUS, fg_color=BG_SECONDARY, hover_color=BG_CARD,
                text_color=TEXT_PRIMARY, font=FONTE_CORPO)


def botao_opcao():
    """Alternativa de questao: largura total, texto alinhado a esquerda."""
    return dict(corner_radius=CORNER_RADIUS, fg_color=BG_SECONDARY, hover_color=ACCENT_HOVER,
                text_color=TEXT_PRIMARY, font=FONTE_CORPO, anchor="w")


def botao_menu():
    """Item da barra lateral. O estado ativo e aplicado por quem navega."""
    return dict(corner_radius=CORNER_RADIUS, fg_color="transparent", hover_color=BG_CARD,
                text_color=TEXT_PRIMARY, font=FONTE_CORPO, anchor="w", height=38)


# --- blocos de layout ---
def painel(pai, **kwargs):
    """Frame no fundo da janela, sem cor propria."""
    return ctk.CTkFrame(pai, fg_color=BG_PRIMARY, **kwargs)


def cartao(pai, **kwargs):
    """Superficie elevada: o bloco de conteudo padrao do app."""
    return ctk.CTkFrame(pai, fg_color=BG_CARD, corner_radius=CORNER_RADIUS, **kwargs)


def cabecalho(pai, titulo, subtitulo=None):
    """Faixa de topo de uma tela: titulo em accent, subtitulo apagado."""
    barra = painel(pai)
    barra.pack(fill="x", padx=PAD_TELA, pady=(PAD_TELA, GAP))
    ctk.CTkLabel(barra, text=titulo, font=FONTE_SECAO, text_color=ACCENT).pack(anchor="w")
    if subtitulo:
        ctk.CTkLabel(barra, text=subtitulo, font=FONTE_LEGENDA,
                     text_color=TEXT_MUTED).pack(anchor="w", pady=(2, 0))
    return barra


def corpo_tela(pai):
    """Area util abaixo do cabecalho, ja com o respiro das bordas."""
    area = painel(pai)
    area.pack(fill="both", expand=True, padx=PAD_TELA, pady=(0, PAD_TELA))
    return area


def linha_valor(pai, rotulo, valor, cor_valor=None):
    """Cartao de uma linha: rotulo a esquerda, valor em destaque a direita."""
    linha = cartao(pai)
    linha.pack(fill="x", pady=PAD_LINHA)
    ctk.CTkLabel(linha, text=rotulo, font=FONTE_CORPO,
                 text_color=TEXT_PRIMARY).pack(side="left", padx=PAD_CARTAO, pady=14)
    ctk.CTkLabel(linha, text=valor, font=FONTE_DESTAQUE,
                 text_color=cor_valor or ACCENT).pack(side="right", padx=PAD_CARTAO, pady=14)
    return linha


def barra_progresso(pai, valor, **kwargs):
    barra = ctk.CTkProgressBar(pai, progress_color=SUCCESS, fg_color=BG_SECONDARY,
                               corner_radius=CORNER_RADIUS, **kwargs)
    barra.set(valor)
    return barra


def cartao_em_construcao(pai, fase, itens):
    """Placeholder de tela ainda nao implementada.

    Existe so enquanto as fases nao entregam as telas de verdade; some junto
    com a ultima delas.
    """
    card = cartao(pai)
    card.pack(fill="x")
    ctk.CTkLabel(card, text="Em construção", font=FONTE_CARTAO,
                 text_color=TEXT_PRIMARY).pack(anchor="w", padx=PAD_CARTAO, pady=(PAD_CARTAO, 2))
    ctk.CTkLabel(card, text=f"Esta tela chega na {fase}.", font=FONTE_LEGENDA,
                 text_color=WARNING).pack(anchor="w", padx=PAD_CARTAO, pady=(0, GAP))
    for item in itens:
        ctk.CTkLabel(card, text="  •  " + item, font=FONTE_CORPO, text_color=TEXT_MUTED,
                     justify="left").pack(anchor="w", padx=PAD_CARTAO, pady=2)
    ctk.CTkFrame(card, fg_color=BG_CARD, height=PAD_CARTAO).pack()  # respiro no rodapé
    return card
