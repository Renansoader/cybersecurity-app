# O que os módulos publicados já ensinam — não repetir no 3.5

Levantado em 02/09/2026, sobre os 30 módulos publicados (1.051
questões). O 3.5 (Web II) é o segundo módulo do bloco Web e encosta em
3.4 (recém-escrito), 3.7 (OWASP Top 10, ainda não escrito), 2.x
(autenticação, sessão, controle de acesso) e 1.6 (Python para
segurança). Uma colisão real e severa achada, não prevista no aviso do
usuário — exatamente o tipo de mordida que o 2.5 já deu no 3.4, então
esta seção foi conferida com atenção redobrada antes de qualquer
questão ser escrita.

## Colisão real e severa (achada) — 1.6 já é dono da defesa de injeção de comando em Python

**1.6 (Python para segurança) tem um bloco de teoria inteiro e quatro
questões sobre exatamente o terceiro canal do eixo 2 proposto
("chamada ao sistema operacional"):**

- **1.6.t6**, título *"Executar comandos sem abrir buraco"* — texto
  completo: *"O módulo subprocess executa programas. A diferença que
  importa é entre passar uma lista de argumentos e passar uma string
  com shell=True. Com lista, o sistema recebe o programa e os
  argumentos separadamente: um valor com ponto e vírgula vira apenas
  texto dentro do argumento. Com shell=True, a string inteira vai para
  o interpretador de comandos, e os metacaracteres passam a valer —
  entrada de usuário nesse caminho é injeção de comando pronta."*
- **1.6.q12** (caça-erro): qual a falha de um código com `shell=True` e
  entrada do usuário concatenada.
- **1.6.q13**: qual chamada de `subprocess.run` executa um programa
  passando entrada externa de forma segura — resposta: lista de
  argumentos, não string.
- **1.6.q20**: defesa mais robusta para um script que repassa nome de
  arquivo a um comando externo — resposta: lista de argumentos **e**
  validação contra lista permitida.
- **1.6.q14**: comportamento de `subprocess.run` com código de saída
  diferente de zero (tangencial, sobre tratamento de erro, não sobre
  injeção em si).

**1.6 é dono de**: a defesa específica em Python — lista de argumentos
em vez de string com `shell=True` — como o equivalente de
parametrização para o canal de comando do sistema operacional, já
demonstrada com código real e caça-erro. O 3.5 não pode reabrir "qual
chamada do `subprocess` é segura" como conteúdo novo, nem reensinar
`shell=True` como o vilão — isso já está publicado e testado.

## Território livre confirmado — SQL e XSS nunca foram ensinados

Varredura por `sql`, `sqli`, `xss`, `injecao`, `sanitiza`, `escape`,
`parametriz`, `contexto-de-saida` no corpus inteiro (todas as tags e o
texto de enunciado/explicação de todas as questões publicadas):
**nenhuma questão em nenhum módulo ensina o mecanismo de SQL injection
nem de XSS.** Os únicos dois hits fora do 1.6 foram falsos positivos
(`1.2.q18` menciona "mysqldump", não SQL injection) ou uma citação de
passagem: **2.5.q13** já explica o que `HttpOnly` faz *sobre* XSS
("HttpOnly impede que o cookie seja lido por `document.cookie`, o que
mitiga o roubo por XSS sem eliminar o XSS: o script continua podendo
agir dentro da sessão da vítima") — mas trata XSS como ameaça já
conhecida, sem nunca explicar o que é nem como acontece. Isso é
referência anterior, não posse: o 3.5 pode citar essa frase como fato
já estabelecido (a mesma técnica que 3.4 usou para SameSite/2.5.q13),
sem repetir o argumento, e sem que ela conflite com ensinar o mecanismo
de XSS pela primeira vez.

## 3.4 — Web I (recém-escrito)

- **3.4.t1**: decisão de segurança sempre no servidor — porque a
  requisição pode vir de qualquer lugar, não porque um canal confunde
  dado com instrução.
- **3.4.t2**: validação client-side é conveniência, não controle —
  sobre *quem* pode ser contornado (o cliente), não sobre *como* uma
  string vira instrução dentro de um parser.

**Risco de família retórica, não de conteúdo**: os dois módulos
discutem "não confiar em entrada não confiável", e é tentador tratar
como o mesmo assunto. Mas são claims diferentes — 3.4 é sobre **onde**
a validação precisa acontecer (servidor, sempre); 3.5 é sobre **por
que** uma entrada bem colocada no lugar errado do parser vira comando,
mesmo quando o servidor já é quem está processando. Um script que
recebe `nome_produto` do usuário e valida no servidor (3.4 satisfeito)
ainda pode ser vulnerável a SQL injection se concatenar esse valor
numa consulta (3.5 é sobre isso). Tratados como distintos, com
referência cruzada explícita no texto do 3.5, não repetição silenciosa
— mesmo padrão já usado entre 4.5 e 4.6.

## 2.5 — Autenticação e identidade

- **2.5.q13**: já citado acima — menção a XSS como consequência para
  justificar o atributo `HttpOnly`, sem ensinar o mecanismo.

**2.5 é dono de**: o que `HttpOnly` faz sobre o *sintoma* (roubo de
cookie via XSS). Não é dono do mecanismo de XSS em si — território
livre para o 3.5, que pode inclusive fechar o círculo citando de volta
que a defesa de cookie já foi ensinada no 2.5, mesmo sem eliminar a
causa.

## 2.6 — Controle de acesso

DAC, MAC, RBAC, ABAC, Zero Trust — modelos de decisão de acesso.
Nenhuma menção a injeção, parser ou canal de entrada. Sem colisão.

## 3.7 — OWASP Top 10 (ainda não escrito)

Reservado explicitamente pelo usuário como dono da **lista** de
vulnerabilidades. O 3.5 não pode virar um catálogo — ensina **um
mecanismo único** (confusão dado/instrução) através de exemplos
mínimos em três canais, não uma enumeração de categorias OWASP. Quando
o 3.7 for escrito, ele deve poder assumir que o aluno já reconhece o
mecanismo de injeção como família, e catalogar variantes/categorias em
cima disso — não reensinar o mecanismo.

## 3.1, 3.2 — Metodologia de pentest, OSINT

Sem menção a injeção, SQL, XSS ou comando em nenhuma questão. Sem
colisão.

---

## Território proposto para o 3.5, e a troca

| Eixo | Proposta original | Risco | Formulação final |
|---|---|---|---|
| 1 | Por que misturar dado e instrução no mesmo canal quebra a fronteira, falha de construção | Nenhum | Mantido — sem colisão com 3.4 (claim diferente, ver acima) |
| 2 | Mesmo mecanismo em canais diferentes: banco, marcação, sistema operacional | **Severo no 3º canal** — 1.6 já ensina a defesa de comando em Python com código real e caça-erro | **Reformulado**: o canal de sistema operacional entra como a prova mais nua do mecanismo (`os.system` concatenado, sem variante segura por lista de argumentos naquela chamada específica — diferente de `subprocess`), não como tutorial de defesa em Python; a defesa em si é referência cruzada explícita a `1.6.t6`, não reensinada |
| 3 | Filtrar é fraco, separar estruturalmente é forte; o que "contexto" significa | Baixo — só para o canal de comando, onde citar `1.6` evita redundância | Mantido para SQL (parametrização) e HTML (contexto de saída), com o canal de comando citando `1.6.q13`/`q20` como o exemplo já resolvido, em vez de resolvê-lo de novo |
| 4 | Contraponto defensivo, fechando o módulo | Nenhum | Mantido |

A troca no eixo 2 preserva o argumento pedagógico central do usuário —
reconhecer a família em três canais, "inclusive a variante que ainda
não existe" — sem duplicar o que 1.6 já demonstrou com código
executado e testado. Decisão pendente de confirmação antes de escrever
qualquer questão.
