"""Dicas progressivas, regra socrática e feedback de erro.

O modelo pedagógico do app mora aqui. Duas garantias que este módulo existe
para dar:

1. `questao_para_exibir()` devolve a questão sem nada que entregue a resposta.
   A tela só recebe o que pode ser mostrado antes da confirmação da tentativa.
2. As dicas saem uma a uma, sob pedido, e nunca de graça. Quem pediu dica fica
   registrado como "acerto com ajuda".

Ordenação e pareamento exigem atenção extra: remover o campo de gabarito não
basta, porque nesses tipos a própria ordem dos itens é a resposta. O conteúdo
grava os itens já na sequência certa, então exibi-los como estão permitiria
acertar apenas confirmando sem mexer em nada. Os dois tipos são embaralhados
aqui, com semente derivada do id da questão — determinístico, testável, e
nunca igual à ordem correta.

O mesmo vale para múltipla escolha, e por um motivo descoberto tarde: o
conteúdo grava a alternativa correta no índice 0 em todas as questões escritas
até hoje. Sem embaralho, a resposta certa seria sempre a primeira linha da
tela, e o curso inteiro poderia ser respondido sem ler o enunciado. As
alternativas são permutadas aqui, e `conferir()` e `feedback()` recebem o
índice EXIBIDO e o traduzem de volta — a tela não sabe da tradução.
"""

import random

SEGUNDOS_PARA_DICA = 20

# Tudo que entrega a resposta e por isso não pode chegar à tela antes da
# confirmação da tentativa.
CAMPOS_DE_RESPOSTA = ("correta", "explicacao", "por_que_erradas",
                      "ordem_correta", "pares")


def _permutar(semente, total, proibida):
    """Permutação determinística de 0..total-1, garantidamente != `proibida`.

    A semente é o id da questão: o mesmo item cai sempre no mesmo lugar, então
    a tela não parece instável entre aberturas e o teste é reproduzível.

    Se o sorteio cair exatamente na ordem proibida, rotaciona uma posição — com
    dois ou mais índices distintos, uma rotação nunca reproduz a lista original.
    """
    if total < 2:
        return list(range(total))
    indices = random.Random(semente).sample(range(total), total)
    if indices == list(proibida):
        indices = indices[1:] + indices[:1]
    return indices


def mapa_de_exibicao(questao):
    """Permutação usada para exibir a questão, recalculada a partir do id.

    Ordenação: posição exibida -> índice do item original.
    Pareamento: posição exibida na coluna direita -> índice do par original.
    Múltipla escolha: posição exibida -> índice da alternativa original.
    Questão sem nenhum desses campos: None.
    """
    tipo = questao["tipo"]
    if tipo == "ordenacao":
        # a ordem proibida é a correta: exibi-la deixaria acertar sem mexer
        return _permutar(questao["id"], len(questao["itens"]),
                         proibida=questao["ordem_correta"])
    if tipo == "pareamento":
        # aqui a proibida é a identidade: direita alinhada com a esquerda
        total = len(questao["pares"])
        return _permutar(questao["id"], total, proibida=range(total))
    if "alternativas" in questao:
        # a identidade é proibida porque o conteúdo grava a correta no índice 0:
        # exibir na ordem do arquivo entregaria a resposta na primeira linha
        total = len(questao["alternativas"])
        return _permutar(questao["id"], total, proibida=range(total))
    return None


def _indice_original(questao, escolha):
    """Traduz o índice que o usuário clicou na tela para o índice do arquivo."""
    mapa = mapa_de_exibicao(questao)
    if mapa is None or not isinstance(escolha, int) or not 0 <= escolha < len(mapa):
        return escolha
    return mapa[escolha]


def questao_para_exibir(questao):
    """A questão como o usuário pode vê-la antes de responder.

    Em ordenação e pareamento acompanha o mapa de índices (`indices_originais`
    e `indices_direita`), para o motor corrigir a resposta contra o gabarito
    original. Ele é dado de correção, não conteúdo de tela: nada no app deve
    renderizá-lo.

    As dicas saem da lista; são liberadas uma por vez por proxima_dica().
    """
    visivel = {campo: valor for campo, valor in questao.items()
               if campo not in CAMPOS_DE_RESPOSTA}
    visivel["dicas_disponiveis"] = len(questao["dicas"])
    visivel.pop("dicas", None)

    if questao["tipo"] == "ordenacao":
        mapa = mapa_de_exibicao(questao)
        visivel["itens"] = [questao["itens"][i] for i in mapa]
        visivel["indices_originais"] = mapa

    if questao["tipo"] == "pareamento":
        # a lista de pares É o gabarito; a tela recebe as duas colunas soltas
        mapa = mapa_de_exibicao(questao)
        visivel["coluna_esquerda"] = [par[0] for par in questao["pares"]]
        visivel["coluna_direita"] = [questao["pares"][i][1] for i in mapa]
        visivel["indices_direita"] = mapa

    if "alternativas" in questao:
        mapa = mapa_de_exibicao(questao)
        visivel["alternativas"] = [questao["alternativas"][i] for i in mapa]
        visivel["indices_originais"] = mapa
    return visivel


def conferir_ordenacao(questao, resposta):
    """Corrige uma ordenação contra a ordem_correta original.

    `resposta` são as posições EXIBIDAS, na sequência em que o usuário as
    colocou. A tradução para os índices originais acontece aqui, e não na tela.
    """
    mapa = mapa_de_exibicao(questao)
    if len(resposta) != len(mapa):
        return False
    return [mapa[posicao] for posicao in resposta] == list(questao["ordem_correta"])


def conferir_pareamento(questao, resposta):
    """Corrige um pareamento contra os pares originais.

    `resposta[i]` é a posição escolhida na coluna direita exibida para a linha
    `i` da coluna esquerda.
    """
    mapa = mapa_de_exibicao(questao)
    if len(resposta) != len(mapa):
        return False
    return all(mapa[escolha] == linha for linha, escolha in enumerate(resposta))


def conferir(questao, resposta):
    """Corrige qualquer tipo de questão. Devolve True se acertou.

    `resposta` é sempre o que a tela viu: em múltipla escolha, o índice da linha
    clicada na ordem EXIBIDA. A tradução para o índice do arquivo acontece aqui.
    """
    tipo = questao["tipo"]
    if tipo == "ordenacao":
        return conferir_ordenacao(questao, resposta)
    if tipo == "pareamento":
        return conferir_pareamento(questao, resposta)
    return _indice_original(questao, resposta) == questao["correta"]


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
        # `escolha` vem da tela, na ordem exibida; a justificativa está indexada
        # pelo índice do arquivo
        justificativa = justificativas.get(str(_indice_original(questao, escolha)))
        if justificativa:
            blocos.append(("sua_escolha", justificativa))
        blocos.append(("explicacao", questao["explicacao"]))
        return blocos

    blocos.append(("explicacao", questao["explicacao"]))
    for indice in sorted(justificativas, key=int):
        blocos.append(("por_que_errada", justificativas[indice]))
    return blocos
