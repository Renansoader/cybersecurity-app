# -*- coding: utf-8 -*-
"""Laboratorio 4.8 — o que um exame forense pode afirmar, e o que nao pode.

Modelo declarado: um conjunto fixo de evidencias coletadas num caso
fictício, e uma lista de afirmacoes que alguem poderia querer fazer a
partir delas. Cada afirmacao e classificada como SUSTENTADA (a evidencia
comprova) ou NAO SUSTENTADA (a evidencia e compativel, mas nao prova) —
sem executar nenhuma tecnica de ocultacao, so avaliando o que already
existe no conjunto de evidencias declarado abaixo.

Roda com: python o_que_o_exame_afirma.py
"""

EVIDENCIAS = [
    "hash do disco batendo com o hash da imagem original (cadeia intacta)",
    "arquivo malicioso encontrado com timestamp de criação de 03/09 02:14",
    "log de autenticação mostra login da conta 'ana.silva' às 02:10",
    "nenhum log de rede cobre o período entre 00h e 06h (fora da janela de retenção)",
    "o processo malicioso rodava sob o mesmo usuário do login das 02:10",
]

AFIRMACOES = [
    ("O arquivo encontrado é bit a bit idêntico ao que estava no disco original", "SUSTENTADA",
     "o hash bate — é exatamente o que a verificação de integridade prova, e só isso"),
    ("O arquivo malicioso foi criado às 03/09 02:14", "NAO SUSTENTADA",
     "timestamp de arquivo é atributo de metadado, alterável por quem tem acesso de escrita — sozinho, não prova quando o arquivo realmente chegou ali"),
    ("A pessoa dona da conta 'ana.silva' foi quem executou a ação", "NAO SUSTENTADA",
     "a evidência mostra que a CONTA foi usada, não que a PESSOA titular da conta estava ao teclado — credencial comprometida produz o mesmo log"),
    ("Não houve atividade maliciosa de rede entre 00h e 06h", "NAO SUSTENTADA",
     "a ausência de log nessa janela é ausência de cobertura, não ausência de evento — o sistema simplesmente não gravava nesse período"),
    ("O processo malicioso rodou com o mesmo contexto de usuário do login das 02:10", "SUSTENTADA",
     "é uma correlação de contexto de execução, diretamente registrada pelo sistema operacional — não depende de inferir intenção nem autoria humana"),
]


def main():
    print("=== evidências coletadas neste caso ===")
    for e in EVIDENCIAS:
        print(f"  - {e}")

    print("\n=== o que cada afirmação pode concluir a partir delas ===")
    sustentadas = 0
    for afirmacao, veredito, razao in AFIRMACOES:
        sustentadas += veredito == "SUSTENTADA"
        print(f"\n  afirmação: {afirmacao}")
        print(f"  veredito:  {veredito}")
        print(f"  razão:     {razao}")

    print(f"\n=== contagem ===")
    print(f"  {sustentadas} de {len(AFIRMACOES)} afirmações sustentadas diretamente pela evidência")
    print(f"  {len(AFIRMACOES) - sustentadas} soam plausíveis, mas exigem uma fonte independente a mais")

    print("\n=== leitura ===")
    print("  Duas das três afirmações não sustentadas envolvem exatamente os dois")
    print("  pontos fracos que este módulo já demonstrou em laboratório: timestamp")
    print("  como metadado alterável, e ausência de log como ausência de cobertura,")
    print("  não de evento. A terceira — autoria humana a partir de uma conta —")
    print("  é o mesmo problema que o curso já chamou de atribuição: usar uma")
    print("  credencial não prova quem digitou a senha.")


if __name__ == "__main__":
    main()
