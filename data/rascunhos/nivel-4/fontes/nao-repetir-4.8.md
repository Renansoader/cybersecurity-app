# O que os módulos publicados já ensinam — não repetir no 4.8

Levantado em 02/09/2026, sobre os 28 módulos publicados (981 questões). O
4.8 (Forense digital) fecha o nível 4 e encosta em quatro vizinhos:
4.4 (artefato de malware, volatilidade), 4.5 (log como fonte), 4.7
(decisão de contenção sob pressão), 0.4 (aspecto legal e cadeia de
custódia). Uma colisão real achada, não prevista no pedido do usuário.

## Colisão real (achada, não estava no aviso) — 4.4 já é dono do eixo 1 (ordem de volatilidade)

**4.4 (Malware) já ensina "ordem de volatilidade importa na coleta de
evidência" como conceito central, não como menção lateral:**

- **4.4.q16**: diferença entre duas decisões de tirar o host do caminho, a
  partir de uma saída real.
- **4.4.q17**: *"Por que a ordem de volatilidade importa na hora de
  coletar evidência?"* — praticamente o título do eixo 1 proposto,
  literalmente.
- **4.4.q18**: cenário de decisão de contenção sob prazo curto, ligado à
  volatilidade.
- **4.4.q24**: memória capturada antes de desligar — que perguntas isso
  responde.
- **4.4.q27**: pareamento artefato × o que acontece com ele ao desligar
  pela tomada — RAM, conexões de rede, arquivo temporário.
- **4.4.t2, 4.4.t3** (teoria): cadeia de infecção como decisões, o que se
  perde e o que sobrevive a um desligamento.

**4.4 é dono de**: por que a ordem de volatilidade importa, e o que cada
camada perde ao desligar um host — como **decisão de contenção sob
pressão** (o mesmo domínio do 4.7, aplicado à técnica em vez de à
autoridade). O 4.8 não pode reabrir "por que a ordem importa" como
achado novo.

## 4.7 — Resposta a incidentes

- Eixo 1 do 4.7 (autoridade de decisão pré-combinada) e eixo 2 (custo de
  agir com informação incompleta) já tratam a tensão "agir agora x
  esperar" — mas na camada organizacional (quem decide, quando vale
  esperar), não na camada técnica de o que uma evidência sustenta.

**4.7 é dono de**: quem decide, com que informação, sob que prazo — a
decisão de responder. Não é dono de como uma evidência é lida ou do que
ela prova depois de coletada — território livre para o 4.8.

## 4.5 — SIEM e monitoramento

- **4.5.q17**: timestamp como problema de normalização entre fontes de
  log de formatos diferentes — sobre comparar logs, não sobre timestamp
  como alvo de manipulação antiforense.
- **4.5.t5**: "regra nunca testada é regra que não existe" — mecanismo de
  verificação por provocação, já reusado no 4.7 (fechar vs mudar).

**4.5 é dono de**: log como fonte de detecção (custo, normalização,
correlação). Não é dono de log como evidência que precisa resistir a
contestação numa investigação — ângulo diferente, mesmo objeto.

## 4.6 — MITRE ATT&CK e caça a ameaças

- **4.6.t2**: "do artefato para o nome, nunca do nome para o artefato" —
  não pular de um rótulo pronto para a conclusão, examinar o artefato
  primeiro.

**Risco de família retórica, não de conteúdo**: o argumento de 4.6.t2
("não conclua sem examinar") e o eixo 3 proposto para o 4.8
("correlação temporal não é prova de causa") são primos — os dois
avisam contra concluir demais a partir de pouco. Mas são claims
diferentes: 4.6 é sobre **classificar** um comportamento (que técnica é
essa?), 4.8 é sobre **provar** um evento (isso realmente aconteceu, e
nessa ordem?). Tratados como distintos, com referência cruzada
explícita no texto do 4.8, não repetição silenciosa.

## 0.3 — Quem é o adversário

- **0.3.q33**: *"Por que a atribuição de autoria de um ataque é
  considerada um problema difícil?"* — já ensina que atribuição é
  problema difícil, em nível estratégico/introdutório.

**0.3 é dono de**: o argumento estratégico de por que atribuir autoria é
difícil. O 4.8 não reabre esse argumento — pode usá-lo como pré-requisito
ao discutir o que uma evidência técnica pode e não pode provar sobre
quem agiu.

## 0.4 — Ética, escopo e lei

Conferido: **nenhuma questão do 0.4 trata de cadeia de custódia,
perícia ou integridade de evidência** — o módulo cobre LGPD/ANPD,
Lei 12.737, Marco Civil e escopo de teste, não procedimento forense.
Sem colisão no eixo 2 (integridade e cadeia de custódia).

---

## Território proposto para o 4.8, e a troca

| Eixo | Proposta original | Risco | Formulação final |
|---|---|---|---|
| 1 | Ordem de volatilidade: o que se perde primeiro e por que a ordem não é preferência, é física | **Alto** — quase o título literal de 4.4.q17 | **Aquisição sem alterar**: o próprio ato de capturar evidência pode alterá-la (RAM muda ao ser lida, conectar um disco sem bloqueio de escrita já grava timestamp) — não repete a ordem de camadas do 4.4, ensina o custo físico de cada método de captura |
| 2 | Integridade e cadeia de custódia como propriedade demonstrável | Nenhum | Mantido — sem colisão |
| 3 | O que uma evidência sustenta e o que não sustenta | Baixo — família retórica com 4.6.t2, claim diferente | Mantido, com referência cruzada explícita a 4.6.t2 no texto |
| 4 | Limites honestos: antiforense, timestamp manipulável, o que um exame não afirma | Nenhum | Mantido — sem colisão; timestamp aqui é manipulação deliberada, diferente do timestamp de normalização do 4.5.q17 |

Decisão pendente de confirmação do usuário antes de escrever qualquer
questão — só o eixo 1 muda.
