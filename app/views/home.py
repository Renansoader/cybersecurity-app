"""Dashboard: streak, meta diária e próximo passo."""

from app import theme


def montar(pai, app):
    theme.cabecalho(pai, "Início", "streak, meta do dia e o que estudar agora")
    corpo = theme.corpo_tela(pai)

    theme.cartao_em_construcao(corpo, "Fase 5", [
        "Streak de dias consecutivos, com escudo semanal",
        "Meta diária de 10, 20 ou 30 questões",
        "Botão grande \"Estudar agora\"",
        "Os três pontos fracos da semana",
        "Próximo módulo sugerido",
    ])
