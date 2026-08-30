"""Validar uma detecção provocando o evento de propósito, em miniatura.

Somente leitura no sistema real: cria e apaga só o próprio arquivo temporário
que ele mesmo gera. Não toca em serviço, registro nem processo de terceiros.

O ponto do módulo é este: uma regra nunca provocada de propósito é uma regra
sobre a qual você só tem opinião, não evidência. Aqui a "regra" é uma função
`detectar()` que varre um diretório atrás de um padrão; o "evento" é um arquivo
que o próprio script cria com esse padrão dentro. Medir o tempo entre criar e
detectar é o mesmo mecanismo do tempo até detectar de um SOC de verdade, só
que em segundos e numa escala em que dá para ver o relógio rodando.
"""
import os
import sys
import tempfile
import time

sys.stdout.reconfigure(encoding="utf-8")

PADRAO = "IOC-TESTE-4C1F9"  # marcador benigno, escolhido para nao colidir com nada real


def detectar(diretorio, padrao):
    """Varre arquivos do diretorio e devolve o primeiro que contem o padrao."""
    for nome in os.listdir(diretorio):
        caminho = os.path.join(diretorio, nome)
        if not os.path.isfile(caminho):
            continue
        try:
            with open(caminho, encoding="utf-8", errors="ignore") as f:
                if padrao in f.read():
                    return caminho
        except OSError:
            continue
    return None


if __name__ == "__main__":
    with tempfile.TemporaryDirectory() as diretorio:
        # fase 1: a regra existe, mas nunca foi provocada -- só há uma "crença" de que funciona
        print("regra escrita, nunca testada: nenhuma evidência de que dispara")

        # fase 2: provocar o evento de propósito
        alvo = os.path.join(diretorio, "artefato_suspeito.txt")
        t_evento = time.perf_counter()
        with open(alvo, "w", encoding="utf-8") as f:
            f.write(f"cabeçalho benigno\nmarcador: {PADRAO}\nrodapé benigno\n")

        achado = None
        tentativas = 0
        while achado is None:
            tentativas += 1
            achado = detectar(diretorio, PADRAO)
            if achado is None:
                time.sleep(0.05)
        t_deteccao = time.perf_counter()

        print("evento provocado em: t=0,000s")
        print(f"detectado em:        t={t_deteccao - t_evento:.3f}s, na varredura número {tentativas}")
        print(f"arquivo:             {os.path.basename(achado)}")
        print("\nsem provocar o evento, a única coisa que se sabe sobre a regra é que ela")
        print("foi escrita — não que ela detecta o que promete detectar.")
