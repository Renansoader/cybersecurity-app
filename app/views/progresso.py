"""Estatísticas: heatmap, domínio por nível e pontos fracos."""

from app import theme


def montar(pai, app):
    theme.cabecalho(pai, "Progresso", "só a primeira tentativa conta no domínio")
    corpo = theme.corpo_tela(pai)

    theme.cartao_em_construcao(corpo, "Fase 5", [
        "Heatmap anual de estudo, no estilo do gráfico de contribuições do GitHub",
        "Domínio por nível e por módulo",
        "Desempenho por tag, para achar o tópico fraco",
        "Histórico de simulados",
    ])
