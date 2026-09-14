# Levantamento de não-repetição — módulo 5.5 (Economia da segurança)

Método: leitura integral da teoria dos 5 módulos apontados (5.4, 5.1, 5.3,
4.1, 0.3), não só grep — a colisão mais provável do curso inteiro está
aqui, como avisado: 5.4 acabou de ensinar comparação de risco com custo
de mitigar contra dano esperado, e 5.1 ensinou custo de corrigir cedo ×
tarde. O risco real não é palavra repetida ("custo", "investimento",
"orçamento" vão aparecer nos dois lugares), é o mesmo mecanismo de
decisão sendo reembalado com vocabulário econômico.

## Por módulo

### 5.4 (GRC) — colisão SEVERA, é o dono do mecanismo de custo × dano por decisão

`5.4.t3` e `5.4.q27` já ensinam: comparar score de risco entre itens
heterogêneos, e decidir aceitar um risco de score alto quando o custo de
mitigar é desproporcional ao dano esperado — "não: a decisão também pesa
o custo da correção contra o dano — aqui o custo superou muito o
benefício" (`5.4.q27`). Isso é, literalmente, análise custo-benefício de
uma decisão de segurança, já registrada com autoridade e critério.

**O que sobra de fato**: nada, na dimensão "decidir se um risco específico
vale a pena mitigar". 5.4 já é dono desse mecanismo, numa decisão isolada
e num portfólio. 5.5 só se sustenta aqui se mudar de unidade de análise:
não é mais "este risco vale mitigar", é "o orçamento de segurança inteiro,
como fatia de recurso finito, compete com outras fatias (feature nova,
outro risco, nada) — e essa alocação agregada tem uma patologia sistêmica
que nenhuma decisão individual, por melhor que seja, corrige sozinha".
Qualquer eixo do 5.5 que cite "custo de mitigar × dano esperado" citando
uma única decisão está pisando em `5.4.t3`/`q27`, não abrindo território
novo — precisa citar como já coberto, nunca reensinar.

### 5.1 (Desenvolvimento seguro) — colisão SEVERA na metade do eixo 3 proposto

`5.1.t1`/`t2` já ensinam o mecanismo central do eixo 3 proposto ("o custo
que não aparece na planilha"): o custo de uma decisão insegura cresce
porque dependentes reais se acumulam sobre ela com o tempo (design → código
→ teste → produção, custo medido como "quantas coisas precisam ser
tocadas junto", 1 para 8 no laboratório do módulo) — e o texto já nomeia
o resultado como "decisão insegura vira dívida permanente" quando a
correção deixa de valer o custo. Isso é dívida técnica de segurança,
com mecanismo e número de laboratório, não estimativa de mercado.

**O que sobra de fato**: 5.1 mede o custo de *mudar uma decisão técnica já
tomada* (dependentes que se acumulam sobre um código). Não cobre o custo
de *não ter feito a decisão nenhuma vez* (o projeto de segurança que nunca
foi para o orçamento, o headcount que nunca foi contratado) nem o custo
de oportunidade no sentido econômico estrito (o que a organização deixou
de fazer — outra feature, outro risco mitigado — porque o dinheiro/tempo
foi para onde foi). O eixo 3 do 5.5 só se sustenta citando `5.1.t2` como
a metade já coberta (dívida técnica acumulada por decisão) e restringindo
o território novo à alocação agregada de recurso finito entre alternativas
concorrentes — o problema de portfólio orçamentário, não o de uma decisão
técnica isolada.

### 5.3 (Modelagem de ameaças) — colisão REAL, mesma raiz que 5.4

`5.3.t5` já registra "aceitar: o custo de mitigar supera o dano esperado,
decisão legítima desde que registrada" — a mesma frase-mecanismo que 5.4
depois estende para portfólio. Não é uma colisão nova além da já descrita
para 5.4; é a mesma raiz, citada duas vezes no corpus (5.3 documenta o
caso de uma ameaça só, 5.4 documenta a comparação de várias). Qualquer
questão do 5.5 que reencene "aceitar risco porque mitigar custa mais que
o dano" precisa citar `5.3.t5` e `5.4.t3`/`q27` como já cobertos, nas duas
camadas (decisão única e portfólio) — 5.5 não abre uma terceira camada
aqui, a menos que essa camada seja genuinamente "múltiplas decisões
concorrendo pelo mesmo orçamento ao longo do tempo", não "um risco vale a
pena".

### 4.1 (Hardening) — colisão leve, resolvida por escopo

`4.1.t4` ("Correção: do prazo fixo à prioridade por risco") parece
econômico à primeira vista, mas o mecanismo é outro: prioriza correção
por exposição, exploração confirmada e automatizabilidade — fatores de
*urgência técnica*, não de custo-benefício financeiro. `4.1.t6` (limite do
checklist) também não é economia, é o limite de uma lista de conformidade
como prova de segurança — já territorializado por `5.4.t4`/`t5`.

**O que sobra de fato**: nenhuma colisão de mecanismo. Cuidado só de
vocabulário: se o 5.5 usar "priorizar correção", precisa deixar claro que
o critério aqui é custo/orçamento, não exposição/exploração (4.1) nem
comparação de score (5.3/5.4) — três critérios de priorização diferentes
já existem no corpus, um quarto (orçamento agregado) só se justifica
nomeando a diferença.

### 0.3 (Quem é o adversário) — colisão leve de forma, não de mecanismo

`0.3.t6` ("defesa proporcional ao risco real", motivação × capacidade do
adversário) tem forma parecida com "gastar o orçamento proporcional a
alguma coisa" — mas o mecanismo é orientado por perfil de ameaça, não por
custo/incentivo econômico. Nenhuma colisão real.

**O que sobra de fato**: livre, com cuidado de não reciclar a mesma frase
de efeito ("resposta proporcional") sem apontar o que está sendo pesado
contra o quê — em 0.3 é motivação×capacidade do atacante, em 5.5 seria
custo×orçamento, eixos ortogonais.

## Resumo por eixo do recorte proposto

| eixo | colide com | gravidade | ação |
|---|---|---|---|
| 1. defeito estrutural (sucesso invisível, fracasso espetacular) | nenhum módulo | nenhuma | livre — nenhum módulo do corpus trata da assimetria de visibilidade entre prevenção (invisível) e falha (espetacular) |
| 2. incentivo desalinhado (quem paga ≠ quem sofre) | nenhum módulo | nenhuma | livre — governança (5.4) trata de quem *decide* e registra, nunca de quem *paga* vs quem *sofre* o resultado da decisão |
| 3. custo fora da planilha (dívida, oportunidade, custo de não fazer) | 5.1.t2 (REAL, dívida técnica acumulada), 5.3.t5 + 5.4.t3/q27 (REAL, custo de mitigar × dano, decisão única e portfólio) | **severa** | restringir a alocação agregada de orçamento finito entre alternativas concorrentes ao longo do tempo — nunca reensinar dívida por decisão (5.1) nem custo-benefício de uma decisão/portfólio de risco (5.3/5.4) |
| 4. argumentar por orçamento sem inventar número | nenhum módulo (evidência de prática em 5.4.t5 é próxima em forma, distante em mecanismo — lá é "fez × provou que fez", aqui é "custa × dá pra medir honestamente") | leve, resolvida por escopo | livre, citando 5.4.t5 só como precedente de forma (rigor de evidência), nunca como mecanismo repetido |
| 5. limite honesto da análise econômica | nenhum módulo de conteúdo — mas é a QUINTA vez seguida que um módulo do nível 5 fecha com "aqui está o limite honesto do método" (5.1, 5.2, 5.3, 5.4 já fizeram isso) | **achado de arquitetura de módulo, não de conteúdo** | ver seção abaixo |

Eixos 1, 2 e 4 estão livres — são o território real do módulo. Eixo 3
precisa de restrição forte antes de escrever (só alocação agregada de
orçamento, nunca decisão isolada). Eixo 5 tem colisão de forma, não de
conteúdo — ver crítica ao recorte.

## Achado próprio: quinta reincidência do molde de MÓDULO — "limite honesto" como fecho

Os quatro módulos anteriores do nível 5 (5.1 "contraponto: segurança como
etapa final", 5.2 "contraponto: o que a nuvem realmente resolve", 5.3
"limite honesto: o que o método não pega", 5.4 "limite honesto do GRC")
fecham todos com o mesmo formato estrutural: um bloco de teoria dizendo
"aqui está o que este método/enfoque não cobre, mesmo aplicado
corretamente". Se o eixo 5 do 5.5 repetir a fórmula sem mecanismo próprio,
é a quinta reincidência consecutiva — pior que a nona/décima variante de
dica, porque está no nível da arquitetura do módulo inteiro, não da frase.

Isso não significa que o mecanismo seja falso — economia explica por que
o subinvestimento acontece estruturalmente e não corrige o incentivo
sozinha, é um limite genuíno. Mas dado que seria a quinta reincidência
arquitetônica seguida, sem um mecanismo tão novo quanto o resto do
módulo justificaria, a decisão é **não abrir eixo 5 no 5.5**. O limite
estrutural do argumento econômico fica registrado aqui como conteúdo
disponível, não descartado — candidato a fechar o nível 5 inteiro no
5.6 (último módulo do nível), numa síntese que compare os limites já
vistos em governança (5.4), modelagem de ameaça (5.3) e economia (5.5)
em vez de repetir a fórmula módulo a módulo uma quinta e sexta vez.

## Decisões finais, pós-crítica do recorte

- **Eixo 3 restringido**: só alocação agregada de orçamento finito entre
  alternativas concorrentes ao longo do tempo (portfólio de decisões
  competindo por um recurso fixo) — nunca decisão isolada de aceitar/
  mitigar (já é 5.3/5.4) nem dívida técnica de uma decisão específica
  (já é 5.1). Cita as duas colisões como já cobertas, nunca reensina.
- **Eixo 5 cortado deste módulo**: quinta reincidência do molde de fecho
  "limite honesto" sem mecanismo novo o bastante pra justificar — síntese
  do nível fica candidata ao 5.6.
- **Módulo fecha com 4 eixos, não 5**: 1 (defeito estrutural de
  visibilidade), 2 (incentivo desalinhado), 3 (orçamento como recurso
  finito, escopo estreito), 4 (argumentar por orçamento sem inventar
  número). 35 questões redistribuídas entre os quatro.
