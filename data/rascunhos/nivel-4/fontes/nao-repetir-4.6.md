# O que os módulos publicados já ensinam — não repetir no 4.6

Levantado em 30/08/2026, sobre os 26 módulos publicados (911 questões). O 4.6
(MITRE ATT&CK e caça a ameaças) é o de maior risco de colisão do nível 4: ele
encosta em 0.2 (vocabulário de cadeia de ataque), 4.3 (camada e o que ela
entrega), 4.4 (cadeia de infecção como decisões) e 4.5 (contagem como métrica
falsa) ao mesmo tempo.

## O achado que mais importa: MITRE ATT&CK já é fonte em seis módulos — só nunca é conteúdo

Uma varredura por citação de `"fonte"` encontrou **MITRE ATT&CK citado em
0.2, 0.3, 1.1, 1.2, 1.3, 1.4, 2.6 e 3.2** — mais de 50 questões. Em nenhuma
delas o ATT&CK é objeto de estudo: ele é sempre a **origem documental** do
vocabulário de um evento já descrito de outro jeito (movimento lateral,
persistência, acesso a credenciais, ocultação de rastros, execução). O 3.2
vai além e cita **IDs de técnica específicos** (T1595, T1596.003, T1592.002,
T1591, T1593.003, M1056, M1047) como fonte de questões de OSINT — mas o ID
nunca aparece no enunciado nem na alternativa correta, só no campo `fonte`,
que o aluno não vê.

Isso significa duas coisas para o 4.6:

1. **O vocabulário de tática já é familiar** ao aluno que chegou até aqui —
   "movimento lateral", "persistência", "acesso a credenciais", "execução",
   "escalada de privilégio", "ocultação de rastros", "acesso inicial",
   "exfiltração", "comando e controle" já apareceram, soltos, em pelo menos
   seis módulos. O 4.6 **não pode ensinar essas palavras como se fossem
   novidade** — precisa assumi-las como dado e ensinar a **estrutura** que as
   organiza (tática × técnica × procedimento), não o glossário.
2. **Citar um ID de técnica como fonte é prática já estabelecida** no corpus
   (3.2 faz isso 12 vezes). O 4.6 pode seguir o mesmo padrão — desde que,
   como em 3.2, o ID nunca vire resposta correta decorável.

## 0.2 — Superfície de ataque e ecossistema

- **Objetivo 3**: "Distinguir vetor de ataque, ponto de entrada e movimento
  lateral". Teoria `0.2.t3` já ensina a cadeia vetor→ponto de entrada→alvo
  final, com MITRE ATT&CK como fonte.
- **0.2.q13, q19, q20, q21, q24, q25, q27**: cobrem exatamente a
  distinção vetor/ponto de entrada/movimento lateral e a ordem de um
  incidente simples.

**0.2 é dono de**: vetor de ataque, ponto de entrada, movimento lateral,
alvo final — como sequência básica de um incidente. O 4.6 não redefine
esses termos; usa-os como pré-requisito.

## 0.3 — Quem é o adversário

- **0.3.q13, q30**: tempo até detectar como métrica estratégica contra
  adversário persistente e capaz (já não repetido pelo 4.5; continua fora de
  cogitação para o 4.6 também).
- **0.3.q28, q29, q34**: sigla APT, por que campanhas começam com técnicas
  banais, ordem típica de uma campanha persistente.

**0.3 é dono de**: por que o adversário avançado importa mais que a
prevenção sozinha, e a ordem típica de uma campanha (não a nomenclatura de
técnica dentro dela).

## 4.3 — Defesa em profundidade

- **Objetivo 2**: "Medir uma pilha de defesa pelo que sobra quando uma
  camada falha, e não pela contagem de camadas."
- **4.3.q6, q12, q19, q35**: falha de modo comum, dependência
  compartilhada, camada ausente que o painel apresenta como presente.

**4.3 é dono de**: contar camada não mede proteção; o que sobra quando uma
camada falha é que mede. É o mesmo *molde* retórico que o 4.6 quer aplicar a
"contar técnica coberta não mede detecção" — **risco real de colisão de
forma, não de conteúdo**. Ver crítica ao eixo 4 abaixo.

## 4.4 — Malware

- **4.4.t2, q5**: "cadeia de infecção como sequência de decisões do
  adversário" — o que ele rejeitou e o que pagou por isso, não como diagrama
  de etapas.
- **4.4.t1**: taxonomia por eixo (propagação, carga útil, persistência), não
  por nome de família de malware.

**4.4 é dono de**: ler a cadeia de infecção como decisões, e a taxonomia por
eixo em vez de nome. O 4.6 não pode reabrir "cadeia como decisões" nem
propor uma segunda taxonomia concorrente — usa a cadeia de decisões como
pano de fundo em que uma técnica é *um* passo, sem redefinir a cadeia em si.

## 4.5 — SIEM e monitoramento

- **4.5.t3**: correlação nasce de uma pergunta, e quem escreve a regra antes
  da pergunta produz ruído.
- **4.5.t5**: regra nunca testada é regra que não existe; validar provocando
  o evento de propósito.
- **4.5.t6, q31–q35**: contar regra e contar alerta mede esforço de
  configuração, não resultado; a métrica que importa é tempo até detectar.

**4.5 é dono de**: pergunta-antes-da-regra, validação por provocação
proposital, e "contagem de regra/alerta ≠ eficácia de detecção". Os três são
o risco de colisão mais alto do 4.6 — ver crítica ao recorte, abaixo.

## 3.1 — Metodologia de pentest

- **3.1.q8, q9, q28**: red team mede capacidade de detecção e resposta; sem
  quem detecte, não há o que medir; ausência de alerta durante o teste vira
  achado próprio, relacionando ação executada a alerta que deveria ter
  disparado.

**3.1 é dono de**: red team como *exercício* que mede detecção depois do
fato, de fora para dentro, numa janela de tempo contratada. Não é dono de
metodologia rotineira de caça a ameaças (hunting como prática contínua do
time interno, hipótese antes de olhar o dado) — território livre, mas
próximo o bastante para exigir diferenciação explícita no texto.

## 3.2 — OSINT e reconhecimento

Já usa IDs de técnica ATT&CK como fonte (ver seção acima). Não ensina a
estrutura tática/técnica/procedimento nem o mapeamento comportamento→nome.

---

## Território proposto para o 4.6, e o risco de cada eixo

| Eixo proposto | Risco de colisão | Com quem |
|---|---|---|
| Tática × técnica × procedimento | Baixo — nenhum módulo ensina a estrutura, só usa os nomes soltos | 0.2, 1.1–1.4 (vocabulário, não estrutura) |
| Mapear comportamento observado → técnica (artefato antes do nome) | Médio — a lógica "evidência antes de rótulo" é a mesma família de raciocínio do 4.5 ("pergunta antes da regra") e do processo de verificação do projeto inteiro ("o que dá para executar, executa") | 4.5.t3 (estrutural, não de conteúdo) |
| Caça guiada por hipótese (hipótese antes do dado) | Médio-alto — é quase a mesma frase de 4.5.t3 aplicada a um verbo diferente (caçar em vez de correlacionar) | 4.5.t3 |
| Limites do mapa de cobertura (contagem ≠ detecção) | Alto — é o MESMO argumento de 4.5.t6, aplicado a "técnica" em vez de "regra/alerta" | 4.5.t6, 4.3 (objetivo 2, mesmo molde retórico) |

A tabela confirma o que a mensagem do usuário já antecipava: os eixos 3 e 4
do recorte proposto encostam de verdade no 4.5, não por acidente de palavra,
mas porque são a mesma ideia aplicada a um objeto vizinho.

## Decisão final, depois da crítica

**Eixo 3 — reformulado.** Em vez de "formular hipótese antes de olhar o
dado" (quase verbatim 4.5.t3), o eixo passa a ensinar a **relação** entre
caça e regra, não uma cópia do argumento pergunta-antes-da-regra:

- Uma regra de correlação (4.5) existe para um padrão **recorrente** que
  vale a pena expressar como limiar. A caça existe para o padrão **raro
  demais** para virar limiar sozinho — é trabalho manual justamente porque
  automatizar ainda não compensa.
- O modo de falha da caça sem hipótese não é fadiga de alerta (isso é do
  4.5): é **viés de confirmação / apofenia** — quem navega o dado sem uma
  pergunta falsificável primeiro encontra "padrão" em qualquer janela que
  olhar, porque comparar muitas coisas ao acaso sempre produz alguma
  coincidência que parece sinal.
- Quando uma caça confirma algo repetível, o resultado certo é **fazer
  aquilo virar regra** — fechando o ciclo com o 4.5 explicitamente, em vez
  de reapresentar o argumento dele como se fosse novo.

**Eixo 4 — mantido, ancorado em "regra nunca testada" (4.5.t5), não em
"contagem ≠ resultado" (4.5.t6).** O gancho mecânico específico: uma célula
pintada num mapa de cobertura significa que existe um log ou uma regra
mapeada para aquela técnica — não que a detecção foi validada. É o mesmo
mecanismo de "regra nunca disparada de propósito é regra que não existe",
aplicado à unidade "técnica" em vez de "regra individual". O texto do 4.6
cita o 4.5 explicitamente como o mesmo argumento aplicado a objeto vizinho,
em vez de reapresentar como achado novo.
