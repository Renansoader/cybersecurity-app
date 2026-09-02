# O que os módulos publicados já ensinam — não repetir no 4.7

Levantado em 02/09/2026, sobre os 27 módulos publicados (946 questões). O 4.7
(Resposta a incidentes) é penúltimo do nível 4 e encosta em quatro vizinhos
ao mesmo tempo: 4.3 (camadas e o que sobra quando falham), 4.5 (detecção e
tempo até detectar), 4.6 (comportamento adversário e caça) e 0.3 (o
argumento estratégico de tempo até detectar). Duas colisões achadas nesta
varredura não estavam no aviso do usuário e mudaram o recorte.

## Recorte proposto originalmente (para registro)

1. Conter x preservar evidência: a tensão entre desligar agora e investigar
   depois.
2. Decidir com informação incompleta e prazo curto — quem decide o quê, e o
   que se decide antes do incidente para não decidir durante.
3. Comunicação como parte técnica da resposta — quem é avisado, quando, e o
   que a lei brasileira exige (ANPD, 3 dias úteis).
4. Pós-incidente que muda o sistema, não só encerra o chamado.

## Colisão 1 (achada, não estava no aviso) — 4.4 já é dono do eixo 1

**4.4 (Malware) tem 9 questões — 26% do módulo — sobre exatamente "conter x
preservar evidência":**

- **4.4.q16**: diferença entre duas decisões de tirar o host do caminho, a
  partir de uma saída real.
- **4.4.q17**: servidor com cifra em andamento, equipe discute isolar ou
  desligar — o que sustenta a escolha.
- **4.4.q18**: por que a ordem de volatilidade importa na coleta de
  evidência.
- **4.4.q24**: memória capturada antes de desligar — que perguntas isso
  responde.
- **4.4.q25**: caça-erro num procedimento de resposta que esconde um custo.
- **4.4.q26**: *"estação sem sinal de cifra em curso, equipe tem 10 minutos.
  O que fazer? isolar mantendo ligada / desligar da tomada / observar /
  reiniciar"* — é o eixo 1 proposto, literalmente.
- **4.4.q27**: pareamento artefato × o que acontece com ele ao desligar pela
  tomada.
- **4.4.q28**: comando para contar conexões abertas sem alterar nada, antes
  de decidir.
- **4.4.q35**: uma hora, host suspeito, qual sequência de ação entrega mais
  informação.

**4.4 é dono de**: a decisão técnica de contenção em si — isolar vs
desligar vs reiniciar, ordem de volatilidade, captura de memória, comandos
de verificação não-destrutivos. O 4.7 não pode reabrir essa decisão como se
fosse conteúdo novo.

## Colisão 2 (achada, não estava no aviso) — 0.4 já é dono do eixo 3 (a parte legal)

**0.4 (Ética, escopo e lei) já ensina o prazo ANPD e o procedimento de
comunicação:**

- Uma questão dá a alternativa correta *"Comunicar à ANPD e aos titulares
  afetados em até 3 dias úteis da ciência"*, com fonte **Resolução CD/ANPD
  nº 15/2024, arts. 6º e 9º** — o prazo já está confirmado na fonte, não é
  número de memória.
- Uma questão caça-erro usa um procedimento interno de 4 passos
  ("1. Conter o incidente e corrigir a falha técnica. 2. Avaliar
  internamente. 3. Se a imprensa noticiar, preparar comunicado. 4. Comunicar
  a ANPD apenas se houver determinação judicial") e pede qual item contraria
  a LGPD — resposta: o item 4, comunicação à ANPD não depende de ordem
  judicial.
- Outra questão separa LGPD × Lei 12.737/2012 × Marco Civil como três
  normas que podem incidir sobre o mesmo incidente ao mesmo tempo.
- Outra confirma que o dever de comunicar corre mesmo com a autoria do
  ataque desconhecida — a maioria dos casos.

**0.4 é dono de**: o prazo legal em si, a fonte normativa, e "conter não
substitui comunicar" como argumento jurídico. Reescrever isso no 4.7 seria
o mesmo defeito de repetição que a seção 5 do PROGRESS.md já lista como
dívida não tratada (pares de questão com vocabulário em comum).

## 4.3 — Defesa em profundidade

- **4.3.q34**: "incidente foi contido no passo 4 de uma cadeia de 6" — usa
  contenção como **evidência de que a pilha de defesa funcionou**, não como
  processo de resposta. Ângulo diferente: 4.3 mede a arquitetura, não a
  decisão de resposta.

**4.3 é dono de**: classificação de controle, falha de modo comum, zero
trust. Não é dono de decisão de resposta — sem colisão real, só vizinhança
de vocabulário (a palavra "contido").

## 4.5 — SIEM e monitoramento

- **4.5.t6, q31–q35**: MTTD (tempo até detectar) como métrica que separa
  monitoramento real de contagem de regra/alerta.

**4.5 é dono de**: como você descobre que há um incidente, e a métrica de
quanto tempo isso levou. O 4.7 começa depois desse ponto — quando já se
sabe que há um incidente, o que fazer. Não repete MTTD como conceito, pode
citá-lo como fato já estabelecido ("o relógio que o 4.5 ensinou a medir é o
mesmo que continua correndo durante a resposta").

## 4.6 — MITRE ATT&CK e caça a ameaças

- Vocabulário tática/técnica/procedimento, mapeamento comportamento→técnica,
  caça por hipótese, limites do mapa de cobertura.

**4.6 é dono de**: como você entende o que o adversário fez. O 4.7 não
remapeia comportamento a técnica — usa a técnica já identificada como dado
de entrada para a decisão de resposta, sem reabrir a classificação.

## 0.3 — Quem é o adversário

- **0.3.q13, q30**: contra adversário determinado e capaz, a métrica que
  importa deixa de ser prevenção e passa a ser detecção/resposta; exemplo
  de invasor com sete meses de permanência.

**0.3 é dono de**: o argumento estratégico de por que resposta importa (a
motivação, em nível de curso introdutório). O 4.7 não repete esse argumento
— assume que o aluno já sabe por que resposta importa, e ensina como
executá-la.

---

## Território final do 4.7, depois da crítica

| Eixo | Formulação final | Por quê |
|---|---|---|
| 1 | **Autoridade de decisão pré-combinada**: quem tem poder de mandar desligar um sistema crítico, e por que isso precisa estar decidido antes do incidente — a ausência de dono da decisão é o defeito, não a técnica de contenção em si (essa é do 4.4) | Original colidia com 4.4; reformulado para a camada organizacional que o 4.4 não cobre |
| 2 | Decidir com informação incompleta e prazo curto — o que se decide antes do incidente para não decidir durante (funde parcialmente com o eixo 1 reformulado) | Sem colisão encontrada |
| 3 | **Cadeia de comunicação interna e disciplina operacional**: quem dentro da empresa precisa saber e quando (técnico → jurídico → direção → comunicação), o que não se discute em canal que o adversário pode monitorar, como a resposta técnica se sincroniza com a obrigação legal — sem reensinar o prazo ANPD, só referenciá-lo como fato já estabelecido no 0.4 | Original colidia com 0.4; reformulado para a camada operacional interna que o 0.4 não cobre |
| 4 | Pós-incidente que muda o sistema, não só encerra o chamado | Sem colisão real — só um gancho conceitual solto em 0.1.q33 |

Decisão confirmada com o usuário em 02/09/2026 antes de escrever qualquer
questão.
