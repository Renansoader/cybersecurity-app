# Fontes — módulo 4.3 (Defesa em profundidade)

Levantado em 25/08/2026. Regra do projeto: recomendação técnica citada é a
**vigente**, conferida na fonte. O que não deu para conferir na fonte está
marcado como **conhecimento consolidado** e não vira afirmação de norma.

---

## Verificado em execução nesta máquina

| Arquivo | O que foi executado | O que a saída mostra |
|---|---|---|
| `lab/modo_de_falha_comum.py` | aritmética de confiabilidade sobre modelo declarado no próprio script; não toca em rede, disco nem processo | quatro camadas, mesmas probabilidades individuais: **1 em 417** supondo independência, **1 em 58** com uma dependência comum de 5% — a pilha real é **7× mais permissiva** com as mesmas quatro camadas. Ganho marginal das camadas dependentes: 6,90×, 2,10×, **1,20×** |
| `lab/classes_de_controle.py` | mesma cadeia de ataque de 6 passos por três conjuntos de controle; modelo declarado no script | só preventivo: para no passo 1, **0 passos observados**. Só detectivo: **completa os 6**, observa 4, 5 e 6. Misto: para no passo 1. **Com o filtro de anexo falhando**, o misto completa 3, para no 4, e o passo 4 sai **observado e revogável**. A contagem de controles não distingue os casos: 4, 3 e 4 |
| `lab/camadas_defender.txt` | `Get-MpComputerStatus` e `Get-MpPreference`, somente leitura | **seis proteções distintas em True** — antivírus, antispyware, tempo real, monitor de comportamento, IOAV e NIS — todas do mesmo produto, com a **mesma versão de motor** (1.1.26070.7) e as três idades de assinatura em **0 dia**. **1 regra ASR configurada** |

O artefato do Defender é o caso real do que os dois primeiros laboratórios
modelam: seis nomes de camada numa tela de status, um único motor por trás.

---

## Fontes documentais

- **NIST SP 800-53 Rev. 5** — famílias de controle e a distinção entre controle
  **preventivo, detectivo e corretivo**. A revisão 5 é a vigente; a rev. 4 foi
  retirada em setembro de 2021.
- **NIST SP 800-207, *Zero Trust Architecture*** (agosto de 2020) — os sete
  princípios, e a definição de que o zero trust move a decisão de acesso para um
  ponto de decisão por requisição, sem eliminar os controles de rede. É a
  publicação vigente; conferir se há rascunho de revisão antes de citar prazo.
- **CISA / NSA — orientação sobre arquitetura zero trust** — usada apenas para
  o ponto de que zero trust é programa plurianual, e não produto.
- **IEC 61508 e a literatura de confiabilidade** — origem do termo **falha de
  modo comum** (*common cause failure*): componentes redundantes que falham pelo
  mesmo motivo, o que anula a redundância. Conceito importado da engenharia de
  segurança funcional; a aritmética do laboratório é a aplicação direta.
- **MITRE ATT&CK** — usado só como vocabulário de etapas de cadeia; o módulo 4.6
  é que trata ATT&CK a fundo, então aqui não se ensina a matriz.

---

## Conhecimento consolidado, sem norma citada

- A expressão *defesa em profundidade* vem da doutrina militar e chega à
  segurança da informação sem definição normativa única. O módulo trata o termo
  como **arranjo de camadas com falhas independentes**, e diz isso explicitamente
  em vez de fingir que existe uma definição de padrão.
- *Falha aberta* e *falha fechada* são vocabulário operacional consolidado.
  **Cuidado de escopo**: `4.2.q13` já cobre a decisão para o equipamento de
  prevenção em linha. Aqui o assunto só entra na teoria, e nenhuma questão
  repete aquela resposta.

---

## Limites de escopo — o que este módulo NÃO ensina

Levantado de `nao-repetir-4.3.md`, que lista 55 respostas certas já publicadas
tocando camada, segmentação ou escolha de controle.

- **Segmentação para limitar movimento lateral** — `0.2.q23`, `0.3.q31` e o 4.2
  inteiro. Aqui a segmentação só aparece como exemplo de camada, nunca como
  resposta certa.
- **Firewall não cobre phishing** — `0.1.q18`. Não repetir.
- **Pessoas, processo e tecnologia** — `0.1.q27`. Eixo diferente do de classes
  de controle; não misturar os dois na mesma questão.
- **Controle compensatório** — `2.6.q16`. Não repetir.
- **Problema sistêmico × sintomático** — `3.1.q34`. Não repetir.
- **Posição de detecção e prevenção na rede** — `4.2.q11`, `4.2.q12`, `4.2.q13`.
  Não repetir.
