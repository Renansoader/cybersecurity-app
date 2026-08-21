"""Ponto de entrada do app de estudo de cibersegurança."""

from pathlib import Path

import customtkinter as ctk

from app import content, db, theme
from app.views import (desafio, ferramentas, glossario, home, modulo,
                       progresso, sessao, trilha)

ctk.set_appearance_mode("dark")

# ordem dos itens da barra lateral
MENU = ["Início", "Trilha", "Sessão diária", "Desafios", "Glossário",
        "Ferramentas", "Progresso"]

# toda tela navegável. "Módulo" não fica no menu: chega-se a ele pela Trilha.
VIEWS = {
    "Início": home,
    "Trilha": trilha,
    "Módulo": modulo,
    "Sessão diária": sessao,
    "Desafios": desafio,
    "Glossário": glossario,
    "Ferramentas": ferramentas,
    "Progresso": progresso,
}

# qual item do menu fica aceso quando a tela não está no menu
DESTAQUE = {"Módulo": "Trilha"}


class App:
    def __init__(self):
        self.modulos, self.erros_de_conteudo = content.carregar_modulos()
        self.niveis = content.carregar_niveis()
        self.modulo_atual = None
        self.aviso = None   # mensagem de uma vez só, mostrada na próxima tela

        self.root = ctk.CTk()
        self.root.title("Cyber — Estudo de Cibersegurança")
        icone = Path(__file__).resolve().parent / "app.ico"
        if icone.exists():
            try:
                self.root.iconbitmap(icone)
            except Exception:
                pass  # .ico é coisa de Windows; em outro sistema fica o ícone padrão
        self.root.geometry("1180x760")
        self.root.minsize(*theme.JANELA_MIN)
        self.root.configure(fg_color=theme.BG_PRIMARY)

        self.sidebar = ctk.CTkFrame(self.root, width=theme.LARGURA_SIDEBAR,
                                    fg_color=theme.BG_SECONDARY, corner_radius=0)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)  # sem isso a barra encolhe até o texto

        self.corpo = theme.painel(self.root)
        self.corpo.pack(side="left", fill="both", expand=True)

        self.botoes = {}
        self._montar_sidebar()
        self.ir_para("Início")

    def _montar_sidebar(self):
        ctk.CTkLabel(self.sidebar, text="CYBER", font=theme.FONTE_TITULO,
                     text_color=theme.ACCENT).pack(anchor="w", padx=theme.PAD_CARTAO,
                                                   pady=(28, 0))
        ctk.CTkLabel(self.sidebar, text="estudo de cibersegurança", font=theme.FONTE_LEGENDA,
                     text_color=theme.TEXT_MUTED).pack(anchor="w", padx=theme.PAD_CARTAO,
                                                       pady=(0, 24))

        for rotulo in MENU:
            botao = ctk.CTkButton(self.sidebar, text=rotulo,
                                  command=lambda r=rotulo: self.ir_para(r),
                                  **theme.botao_menu())
            botao.pack(fill="x", padx=theme.GAP, pady=3)
            self.botoes[rotulo] = botao

        ctk.CTkLabel(self.sidebar, text=f"{len(self.modulos)} módulos carregados",
                     font=theme.FONTE_LEGENDA, text_color=theme.TEXT_MUTED).pack(
            side="bottom", pady=theme.PAD_CARTAO)

    def abrir_modulo(self, modulo_id, aviso=None):
        self.modulo_atual = modulo_id
        self.aviso = aviso
        self.ir_para("Módulo")

    def ir_para(self, tela):
        for widget in self.corpo.winfo_children():
            widget.destroy()

        aceso = DESTAQUE.get(tela, tela)
        for rotulo, botao in self.botoes.items():
            ativo = rotulo == aceso
            botao.configure(fg_color=theme.BG_CARD if ativo else "transparent",
                            text_color=theme.ACCENT if ativo else theme.TEXT_PRIMARY)

        if self.erros_de_conteudo:
            self._avisar_erros()
        VIEWS[tela].montar(self.corpo, self)

    def _avisar_erros(self):
        """Módulo malformado não pode derrubar o app: avisa qual arquivo e qual campo."""
        faixa = theme.cartao(self.corpo)
        faixa.configure(fg_color=theme.BG_SECONDARY)
        faixa.pack(fill="x", padx=theme.PAD_TELA, pady=(theme.PAD_TELA, 0))
        ctk.CTkLabel(faixa, text="Conteúdo com problema — estes arquivos não foram carregados:",
                     font=theme.FONTE_CORPO, text_color=theme.DANGER).pack(
            anchor="w", padx=theme.PAD_CARTAO, pady=(theme.GAP, 2))
        for erro in self.erros_de_conteudo:
            ctk.CTkLabel(faixa, text="• " + erro, font=theme.FONTE_LEGENDA,
                         text_color=theme.TEXT_MUTED, wraplength=860,
                         justify="left").pack(anchor="w", padx=theme.PAD_CARTAO, pady=(0, 2))
        ctk.CTkFrame(faixa, fg_color=theme.BG_SECONDARY, height=theme.GAP).pack()

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    db.iniciar()  # cria progress.db e o esquema no primeiro uso
    App().run()
