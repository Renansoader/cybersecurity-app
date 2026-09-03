# -*- coding: utf-8 -*-
"""Laboratorio 3.5 — dado que vira instrucao: chamada ao sistema operacional.

Nao executa nada perigoso: usa `echo`, presente em qualquer sistema, e
compara concatenar a entrada numa string de shell contra passar a mesma
entrada como argumento isolado (sem shell nenhum). A entrada usada
encadeia um segundo `echo` inofensivo — nao abre conexao nenhuma, nao
roda shell interativo, nao e um payload de ataque, so prova que o
separador de comando (;) do dado virou separador de comando de verdade.

Este laboratorio nao ensina a defesa em Python de novo — o modulo 1.6
(ferramentas/../1.6.t6) ja mostrou lista de argumentos vs shell=True
com codigo testado. Aqui o ponto e mais nu: mostrar que o mecanismo por
tras da injecao de comando e o mesmo mecanismo do SQL e do HTML, entrada
sem fronteira em relacao a instrucao — nao repetir a licao de subprocess.

Roda com: python comando_concatenado.py
"""

import subprocess


def executa_via_shell(entrada):
    """Concatena a entrada numa string e manda pro shell interpretar —
    dado e instrução no mesmo canal, sem fronteira nenhuma."""
    comando = f"echo mensagem: {entrada}"
    resultado = subprocess.run(comando, shell=True, capture_output=True, text=True)
    return comando, resultado.stdout.strip()


def executa_sem_shell(entrada):
    """A entrada vira UM argumento da lista — nunca é reinterpretada
    como separador de comando, porque não existe shell no meio."""
    resultado = subprocess.run(["echo", "mensagem:", entrada], capture_output=True, text=True)
    return ["echo", "mensagem:", entrada], resultado.stdout.strip()


def main():
    entrada_normal = "tudo certo"
    # separador de comando do shell desta máquina (cmd.exe, Windows): "&".
    # Em shells POSIX (bash, sh) o separador equivalente é ";" — o caractere
    # muda de shell para shell, o mecanismo (separador de dado virando
    # separador de comando) é o mesmo.
    entrada_com_separador = "oi & echo comando extra rodou"

    print("=== chamada normal, via shell ===")
    comando, saida = executa_via_shell(entrada_normal)
    print(f"  comando montado: {comando!r}")
    print(f"  saída: {saida!r}")

    print("\n=== entrada com '&' embutido, via shell (concatenação) ===")
    comando, saida = executa_via_shell(entrada_com_separador)
    print(f"  comando montado: {comando!r}")
    print(f"  saída: {saida!r}")
    print("  (duas linhas de saída — o shell tratou o '&' da entrada como separador real)")

    print("\n=== a mesma entrada, sem shell (lista de argumentos) ===")
    comando, saida = executa_sem_shell(entrada_com_separador)
    print(f"  comando montado: {comando!r}")
    print(f"  saída: {saida!r}")
    print("  (uma linha só — o '&' virou parte do texto do argumento, não separador)")

    print("\n=== leitura ===")
    print("  Por concatenação com shell, o '&' que estava dentro do dado do usuário")
    print("  foi lido pelo shell como o MESMO '&' que separa dois comandos digitados")
    print("  por um operador — o shell não tem como saber a diferença. Sem shell,")
    print("  passando a entrada como um item isolado da lista, o '&' nunca sai da")
    print("  posição de dado: é só um caractere dentro de uma string, como outro")
    print("  qualquer. É o mesmo mecanismo do apóstrofo no SQL e da tag no HTML —")
    print("  só troca o canal e o caractere que demarca a fronteira (';' em bash,")
    print("  '&' no cmd.exe, mas sempre um separador que o shell já reserva).")


if __name__ == "__main__":
    main()
