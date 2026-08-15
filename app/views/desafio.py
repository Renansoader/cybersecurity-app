"""Desafios práticos guiados por checklist. O app nunca dá a solução."""

from app import theme


def montar(pai, app):
    theme.cabecalho(pai, "Desafios", "tarefa, dicas e checklist — nunca a solução")
    corpo = theme.corpo_tela(pai)

    theme.cartao_em_construcao(corpo, "Fase 7", [
        "Lista de desafios por nível, um por módulo a partir do nível 1",
        "Checklist de 4 a 7 itens, marcado à mão pelo usuário",
        "Dicas progressivas, sem código pronto",
        "Link para o lab externo quando houver",
    ])
