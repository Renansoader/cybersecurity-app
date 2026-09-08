# Levantamento de não-repetição — módulo 5.2 (Segurança em nuvem)

Método: grep por termo (`nuvem|cloud|IAM|AWS|Azure|GCP|efêmero|container|
kubernetes|bucket|responsab`) contra os JSON brutos de 4.1, 4.2, 4.8, 3.6,
2.6 e 5.1, seguido de leitura de cada trecho batido e dos objetivos/títulos
de teoria de cada módulo. Não é intuição — é contagem e leitura do
mecanismo real, contra o corpus publicado.

## Por módulo

### 2.6 (Controle de acesso) — colisão SEVERA no eixo 2

2.6 já ensina, como mecanismo formal: DAC, MAC, **RBAC**, **ABAC**, matriz
de permissão (ACL × capacidade), leitura de permissão real (bits POSIX,
ACL do Windows), acúmulo de privilégio, separação de funções, e **Zero
Trust como arquitetura, citando NIST SP 800-207** (`2.6.t6`). O eixo 2
proposto para 5.2 — "identidade vira o perímetro; permissão excessiva
como o defeito mais comum" — é, na formulação atual, quase o mesmo
enquadramento de `2.6.t6` mais o objetivo 2 do 2.6 ("aplicar menor
privilégio... reconhecer o acúmulo de privilégio"). Rodar esse eixo como
proposto reensinaria Zero Trust e permissão excessiva pela segunda vez.

**O que sobra de fato**: 2.6 fala de identidade e permissão de *pessoa e
processo dentro de um sistema*, avaliada por tabela local (POSIX/ACL) ou
papel/atributo. Não cobre: identidade de **carga de trabalho** (service
account, role assumida por máquina, não por humano), credencial
**temporária/de vida curta** como padrão em vez de exceção, política como
**documento** (JSON de permissão) em vez de tabela RBAC, e confiança
**entre contas/tenants** (uma conta assume papel em outra). Esse é
território livre — é uma forma de identidade que 2.6 nunca discute,
porque 2.6 não tem conceito de fronteira entre contas.

### 4.1 (Hardening) — colisão leve no eixo 1

`4.1.q24` já distingue explicitamente "infraestrutura de nuvem" de
"equipamento instalado nas dependências", tratando os dois como alvo do
mesmo mecanismo de linha de base — a resposta correta da questão diz que
"ambos cobrem ambientes locais e de nuvem; a separação entre eles é de
nível de abstração, não de local". Ou seja: 4.1 **já sabe** que hardening
se aplica a nuvem e trata isso como não-diferença.

**O que sobra de fato**: 4.1 nunca discute **quem** aplica a linha de
base em cada camada — o objetivo 4.1 é medir desvio e reduzir superfície,
não repartir a responsabilidade entre quem opera a infraestrutura física
e quem opera o que roda em cima dela. O eixo 1 do 5.2 ("o que muda quando
a infraestrutura não é sua") precisa ficar na linha divisória de
responsabilidade — quem tem obrigação de aplicar qual controle — não
reabrir "o que é uma linha de base" ou "como priorizar correção por
risco", que já é 4.1 inteiro.

### 4.2 (Segurança de rede) — sem colisão real

4.2 é modelo de rede com hardware/software de rede tradicional: filtro
com/sem estado, IDS/IPS, VLAN, DMZ, VPN, proxy, NAC. Nenhum trecho trata
de grupo de segurança definido por software, rede virtual isolada por
provedor, ou o fato de que, na nuvem, o "cabo" não existe. Nenhum eixo do
recorte proposto encosta em segmentação de rede — território sem uso
neste recorte, mas fica registrado como livre para o caso de um eixo
mudar.

### 4.8 (Forense digital) — sem colisão real, mas objetivo explícito de não-repetição já existe no próprio 4.8

4.8 já tem, no seu objetivo 1, a frase "sem repetir a ordem de
volatilidade já ensinada no 4.4" — mostra que este módulo tem histórico
de cuidado com fronteira. Mecanismos que 4.8 possui: efeito observador
(examinar altera), cadeia de custódia como matemática, correlação
temporal não é causa, ausência de log não é ausência de ação, limites
honestos de timestamp/atribuição. **Nenhum trecho fala de infraestrutura
que deixa de existir** — não há menção a contêiner, instância, ou
processo de captura correndo contra o relógio antes de o recurso ser
desligado/destruído.

**O que sobra de fato**: o eixo 4 proposto ("infraestrutura efêmera... o
que acontece com log, evidência e resposta a incidente") é território
livre — mas precisa ser referência cruzada, não reabertura, de "copiar
antes de examinar" (`4.8.t2`) e "ausência de log não é ausência de ação"
(`4.8.t5`). O ângulo novo genuíno é: quando o disco simplesmente some
(instância destruída, contêiner reciclado) antes que alguém chegue para
copiar, a única evidência que sobra é a que já tinha saído do host — o
que muda é a **janela de captura**, não o mecanismo de cadeia de custódia
em si, que 4.8 já ensina e não precisa repetir.

### 3.6 (Web III) — sem colisão, confirmado por leitura, não só grep

Todos os achados do grep foram falso positivo (conjugação verbal em
"-eriam" batendo com o radical de busca solto, sem relação com nuvem,
IAM ou responsabilidade). Regra 10 (achado de lente é hipótese, não
veredito) vale também para achado negativo — grep limpo não é prova
sozinho. **Confirmação por leitura direta** dos 4 objetivos e dos 6
títulos de teoria do 3.6: autenticado ≠ autorizado; verificação por
objeto a cada requisição; mais portas de entrada do que telas; escalada
horizontal e vertical como a mesma lacuna; lógica de negócio (requisição
fora de ordem); contraponto — verificação centralizada, estado no
servidor, menor privilégio como camada complementar. Nenhum objetivo ou
título toca modelo de nuvem, identidade de carga de trabalho ou fronteira
entre conta/tenant. Território sem interseção, confirmado por leitura.

### 5.1 (Desenvolvimento seguro) — colisão de terminologia, não de mecanismo

5.1 usa a palavra "responsabilidade" com frequência (`5.1.t3`, `5.1.q10`,
`5.1.q11`, `5.1.q35`), mas sempre no sentido de responsabilidade de
**autoria** — quem incluiu uma dependência transitiva responde pela
falha dela, mesmo sem tê-la escrito; segurança é processo do time
inteiro, não só de quem revisa por último. É um mecanismo de
**imputação de código**, não de **repartição operacional entre provedor
e cliente de infraestrutura**. Não há colisão de mecanismo — só cuidado
de vocabulário: o eixo 1 do 5.2 não pode reciclar a frase "responsabilidade
de quem escreveu/incluiu" do 5.1, para não soar como o mesmo argumento
reaplicado. Usar "responsabilidade **operacional**" ou "linha de
obrigação contratual" evita a colisão de leitura.

## Resumo por eixo do recorte proposto

| eixo | colide com | gravidade | ação |
|---|---|---|---|
| 1. o que muda quando a infra não é sua | 4.1 (leve), 5.1 (terminologia) | leve | manter, mas focar na linha de obrigação, não em "o que é hardening"; trocar vocabulário de "responsabilidade" do 5.1 |
| 2. identidade como perímetro / permissão excessiva | 2.6 (Zero Trust, RBAC/ABAC, menor privilégio) | **severa** | reformular: sair de "identidade é o novo perímetro" (é a tese de `2.6.t6`) para identidade de **carga de trabalho** e confiança **entre contas** — algo que 2.6 não tem categoria para discutir |
| 3. padrão inseguro por conveniência | nenhum módulo | nenhuma | livre |
| 4. infraestrutura efêmera / log / evidência / resposta a incidente | 4.8 (leve, cruzamento por referência) | leve | manter, citar `4.8.t2`/`t5` como mecanismo já ensinado, focar no ângulo novo: janela de captura que desaparece |
| 5. contraponto — o que a nuvem resolve | nenhum módulo | nenhuma | livre |

Nenhum eixo precisa ser eliminado. O eixo 2 precisa de reformulação real
antes de escrever — é o único caso desta série com colisão de mecanismo
inteiro (Zero Trust + RBAC/ABAC + menor privilégio), não só de
vocabulário ou de aplicação lateral.

## O que o 5.2 explicitamente NÃO vai cobrir, e de quem é o mecanismo

Registrado para que nenhum módulo futuro reabra a mesma discussão sem
medir primeiro:

| eixo do 5.2 | não vai cobrir | mecanismo é do |
|---|---|---|
| 1 | o que é uma linha de base, como medir desvio, como priorizar correção por risco, o limite do checklist de conformidade | 4.1 (Hardening) |
| 1 | responsabilidade por ter incluído uma dependência transitiva na árvore do próprio código | 5.1 (Desenvolvimento seguro) |
| 2 | DAC, MAC, RBAC, ABAC como modelos de decisão de acesso; leitura de permissão real (POSIX/ACL); acúmulo de privilégio e separação de funções entre pessoas; Zero Trust como arquitetura (NIST SP 800-207) | 2.6 (Controle de acesso) |
| 3 | — (território livre, nenhum módulo publicado toca "não mudei nada" como padrão inseguro por conveniência) | — |
| 4 | efeito observador (examinar altera evidência); cadeia de custódia como propriedade matemática; correlação temporal não é causa; ausência de log não é ausência de ação; limites honestos de timestamp/atribuição; ordem de volatilidade | 4.8 (Forense digital), que por sua vez já cede ordem de volatilidade ao 4.4 |
| 4 | filtro com/sem estado, IDS/IPS, VLAN, DMZ, VPN, proxy, NAC — segmentação de rede por hardware/software tradicional | 4.2 (Segurança de rede), mesmo sem uso direto neste recorte |
| 5 | — (território livre) | — |

## Amarra do eixo 2 — obrigatória antes de escrever

O eixo 2 só se sustenta se for **contrastivo** com o 2.6, não paralelo.
Pelo menos **três questões** do eixo precisam ter como distrator correto
(no sentido de "o erro real que a questão captura") a transposição
indevida da intuição de RBAC/menor-privilégio-de-pessoa para o caso de
carga de trabalho/máquina — quem responde certo aplicando o modelo do
2.6 sem ajuste erra a questão. Candidatos de contraste, a confirmar na
escrita:

1. **Rotação de credencial**: intuição humana é "trocar senha
   periodicamente"; o padrão certo para carga de trabalho é vida curta
   automática (a credencial expira sozinha, não é trocada por decisão).
   Quem aplica "política de troca periódica" (2.6/2.4) erra.
2. **Alcance de permissão**: intuição humana é "papel cobre todas as
   tarefas que a pessoa pode vir a fazer"; para carga de trabalho o
   alcance certo é a chamada/função específica, não o conjunto de casos
   que a aplicação inteira pode precisar. Quem generaliza "o papel deve
   cobrir tudo que o serviço pode fazer" repete o erro de RBAC de
   pessoa.
3. **Revisão de acesso**: intuição humana é revisão periódica (auditoria
   anual, desligar quem saiu — 2.6.q16/q28 já ensinam isso para pessoa);
   para carga de trabalho o controle certo é a credencial já nascer com
   prazo, não depender de alguém lembrar de revisar. Quem responde
   "agendar revisão trimestral" para credencial de máquina erra o eixo.
4. (reserva) **Confiança entre contas**: intuição de "a role define o
   que se pode fazer" ignora **quem pode assumir** a role — o distrator
   certo é achar que bastaria auditar as permissões da role, sem auditar
   quem tem permissão de assumi-la de outra conta.

Se, na escrita, esses contrastes não renderem questões honestas (sem
forçar a resposta), o eixo 2 cai e o levantamento é atualizado antes de
seguir — não se força o recorte para preencher vaga.

## Fechamento do eixo 2 — 3 contrastivas, cada uma com mecanismo próprio

O eixo 2 fechou com exatamente as 3 contrastivas exigidas pela amarra
acima, cada uma testando um mecanismo diferente da transposição indevida
de RBAC humano para carga de trabalho — não a mesma ideia reformulada
três vezes:

- **q3 — o valor da credencial.** O erro é aplicar troca por calendário
  (rotacionar a cada 90 dias) a uma credencial de máquina. O mecanismo
  testado é o **valor do segredo em si**: um valor estático, se vazar,
  fica utilizável até a próxima troca programada — a janela de exposição
  é o intervalo entre rotações.
- **q4 — o alcance da permissão.** O erro é conceder acesso amplo
  ("leitura e escrita em todos os tipos de registro") a uma identidade
  que só precisa de leitura de um tipo, copiando a lógica de "papel
  humano largo evita pedir de novo". O mecanismo testado é o **escopo da
  concessão**: alcance maior que o necessário multiplica o raio de dano
  de qualquer falha da aplicação, sem ganho de conveniência real (pedido
  de acesso pode ser automatizado também).
- **q9 — o gatilho de expiração.** O erro é agendar revisão trimestral de
  permissões, copiando auditoria de acesso humano. O mecanismo testado é
  **o que decide quando a permissão deveria acabar**: revisão por
  calendário pergunta "já é hora de olhar de novo?", não "essa tarefa
  ainda existe?" — a identidade pode sobreviver ao fim da tarefa por
  semanas mesmo com revisão mensal, porque o gatilho errado (data) está
  no lugar do gatilho certo (fim da tarefa).

As três could ser confundidas por usarem o mesmo pano de fundo (RBAC de
pessoa não se aplica a máquina) e concluir, todas, em "algo deveria
expirar/ser restrito automaticamente" — mas cada uma aponta para um
componente diferente do problema (valor do segredo × escopo da permissão
× gatilho do fim). Uma revisão adversarial já confirmou q3/q9 como quase
duplicatas numa primeira versão (mesma frase de conclusão, "credencial
nascer com prazo de validade e expirar sozinha") — corrigido separando
explicitamente o mecanismo de cada uma antes da publicação.

## Dívida registrada — confiança entre contas (quem pode assumir uma identidade de outra conta)

Durante a escrita, uma questão (`5.2.q14`, versão original) tentou cobrir
um quarto ângulo do eixo 2 — auditoria de **quem, em outras contas, tem
permissão de assumir uma identidade** — usando como fonte o próprio
levantamento de não-repetição em vez de um bloco de teoria do módulo.
A revisão adversarial (lente de precisão) confirmou: **nenhum dos seis
blocos de teoria do 5.2 cobre esse mecanismo** — `5.2.t2` é sobre
identidade de carga de trabalho em geral, `5.2.t3` é sobre RBAC de pessoa
× máquina, nenhum dos dois fala de confiança entre contas/tenants.

**Decisão**: a questão órfã foi cortada, não mantida com fonte fraca —
"questão sem teoria dona é dívida pior que citação torta". Substituída
por uma questão ancorada em `5.2.t2` + `5.2.t3` (identidade reutilizada
entre aplicações do mesmo time, não entre contas). O eixo 2 fechou com
os 3 contrastivos obrigatórios (acima) sem essa quarta cobertura.

**Confiança entre contas continua sendo território real e livre** —
nenhum módulo publicado até esta data (37 módulos) o cobre. Fica
registrado como candidato a **bloco extra dentro de um módulo futuro do
nível 5** (o mais próximo em tema seria um módulo de arquitetura/desenho
de nuvem multiconta, se algum dia existir) — nunca a módulo novo por si
só, pelo mesmo critério já usado para outras dívidas finas desta linha
(vishing/deepfake no 2.7, ver seção 5 do PROGRESS.md).
