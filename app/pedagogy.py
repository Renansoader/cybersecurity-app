"""Dicas progressivas, regra socrática e feedback de erro.

O modelo pedagógico do app mora aqui. Duas garantias que este módulo existe
para dar:

1. `questao_para_exibir()` devolve a questão sem nada que entregue a resposta.
   A tela só recebe o que pode ser mostrado antes da confirmação da tentativa.
2. As dicas saem uma a uma, sob pedido, e nunca de graça. Quem pediu dica fica
   registrado como "acerto com ajuda".

Não existe função que revele a resposta sem uma tentativa registrada. Isso é
proposital: a tela não tem como pular a etapa nem por engano.
"""

SEGUNDOS_PARA_DICA = 20

# Tudo que entrega a resposta e por isso não pode chegar à tela antes da
# confirmação da tentativa.
CAMPOS_DE_RESPOSTA = ("correta", "explicacao", "por_que_erradas",
                      "ordem_correta", "pares")


def questao_para_exibir(questao):
    """A questão como o usuário pode vê-la antes de responder.

    As dicas saem da lista: elas são liberadas uma por vez por proxima_dica().
    """
    visivel = {campo: valor for campo, valor in questao.items()
               if campo not in CAMPOS_DE_RESPOSTA}
    visivel["dicas_disponiveis"] = len(questao["dicas"])
    visivel.pop("dicas", None)

    if questao["tipo"] == "pareamento":
        # a lista de pares É o gabarito; a tela recebe as duas colunas soltas.
        # A coluna da direita sai em ordem alfabética: desfaz o pareamento e é
        # determinística. Se a repetição incomodar no uso, trocar por embaralho
        # com semente fixa por questão.
        visivel["coluna_esquerda"] = [par[0] for par in questao["pares"]]
        visivel["coluna_direita"] = sorted(par[1] for par in questao["pares"])
    return visivel


def dica_liberada(segundos_na_questao, dicas_pedidas, questao):
    """O botão de dica só aparece depois de 20 segundos, e enquanto houver dica."""
    return (segundos_na_questao >= SEGUNDOS_PARA_DICA
            and dicas_pedidas < len(questao["dicas"]))


def proxima_dica(questao, dicas_pedidas):
    """A próxima dica da lista, da mais vaga para a mais específica.

    Devolve None quando acabaram. A última dica não entrega a alternativa —
    isso é responsabilidade de quem escreve o conteúdo, não do código.
    """
    if dicas_pedidas >= len(questao["dicas"]):
        return None
    return questao["dicas"][dicas_pedidas]


def pergunta_socratica(questao):
    """Mostrada depois do "Confirmar" e antes do resultado, para forçar metacognição."""
    return questao["pergunta_socratica"]


def feedback(questao, escolha, acertou):
    """Blocos de feedback, na ordem em que devem aparecer.

    Quem errou vê primeiro por que a SUA escolha estava errada, e só depois a
    explicação — para o erro virar aprendizado, e não vergonha.
    """
    blocos = []
    justificativas = questao.get("por_que_erradas", {})

    if not acertou:
        justificativa = justificativas.get(str(escolha))
        if justificativa:
            blocos.append(("sua_escolha", justificativa))
        blocos.append(("explicacao", questao["explicacao"]))
        return blocos

    blocos.append(("explicacao", questao["explicacao"]))
    for indice in sorted(justificativas, key=int):
        blocos.append(("por_que_errada", justificativas[indice]))
    return blocos
