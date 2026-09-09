# Levantamento de não-repetição — módulo 5.3 (Modelagem de ameaças)

Método: leitura dos objetivos e títulos de teoria dos 8 módulos apontados
(5.1, 5.2, 4.1, 4.3, 3.1, 3.6, 2.6, 1.4), não só grep — modelagem de
ameaças é método transversal, o risco real está em mecanismo repetido sob
vocabulário diferente, o que grep sozinho não pega. Acrescentado por
iniciativa própria: **3.7 (OWASP Top 10)**, fora da lista pedida, porque
seu recorte ("a lista como instrumento, não catálogo de siglas") é
estruturalmente análogo ao eixo 1 proposto aqui — precisa ser
diferenciado mesmo não tendo sido pedido.

## Por módulo

### 2.6 (Controle de acesso) — colisão REAL no eixo 3

2.6 já ensina RBAC, ABAC, menor privilégio, acúmulo de privilégio e Zero
Trust como arquitetura. Se o eixo 3 (vocabulário de categorias) usar a
categoria "elevação de privilégio" com o mesmo enquadramento de 2.6
(RBAC mal desenhado, acúmulo de permissão), é reensino direto.

**O que sobra de fato**: 2.6 ensina o **controle** (como impedir elevação
de privilégio depois que o sistema existe); modelagem de ameaça, se for
usar essa categoria, precisa ensinar o **raciocínio antecipatório** — em
que ponto do desenho, antes de o controle existir, alguém deveria ter
perguntado "o que acontece se este componente confiar demais no próximo".
A categoria pode aparecer, mas ancorada num sistema inventado sendo
desenhado, nunca reaproveitando o enquadramento de RBAC/ACL do 2.6.

### 3.6 (Web III) — colisão REAL no eixo 3

3.6 já ensina escalada horizontal e escalada vertical como "a mesma
lacuna — checagem incompleta de autorização — vista por ângulos
diferentes", com laboratório HTTP real. É, na prática, elevação de
privilégio aplicada e nomeada, só que em aplicação web já construída.

**O que sobra de fato**: nada, se o eixo 3 usar exemplo web. O eixo 3
precisa ficar em nível de **desenho**, não de aplicação já rodando — a
pergunta de modelagem de ameaça é "este fluxo entre dois componentes
deveria existir sem verificação?", feita **antes** do código, não "este
código tem uma checagem incompleta?", feita **depois** (isso já é 3.6).
Cross-referência recomendada em vez de reensino.

### 3.1 (Metodologia de pentest) — colisão leve no eixo 4

`3.1.t6` já ensina "o relatório é o produto: achado, risco e prioridade"
— priorização de achado real por impacto/exploração, depois de encontrado
num teste. O eixo 4 do 5.3 ("priorizar, aceitar, mitigar") corre risco de
duplicar esse raciocínio de priorização por risco.

**O que sobra de fato**: a diferença temporal é o que salva o eixo —
3.1 prioriza uma vulnerabilidade **já confirmada, já explorável**, num
sistema que já existe; modelagem de ameaça tria um risco **hipotético**,
antes de qualquer exploração, num sistema que pode nem ter sido
construído ainda. O eixo 4 precisa nomear essa diferença explicitamente
(triagem de projeto × triagem de achado) e citar `3.1.t6` como referência
cruzada de "como se prioriza depois de confirmado", não reensinar
priorização do zero.

### 4.1 (Hardening) — colisão leve de estrutura argumentativa no eixo 1

`4.1.t6` ("o limite do checklist: conformidade não é segurança") tem a
mesma forma retórica do eixo 1 proposto ("lista de vulnerabilidade
conhecida não é modelagem de ameaça") — mesmo tipo de argumento
("checklist/lista ≠ a coisa real"), objeto diferente (conformidade de
configuração × modelo de ameaça).

**O que sobra de fato**: o mecanismo é diferente (4.1 fala de desvio de
linha de base medível; 5.3 fala de antecipação de cenário de ataque não
catalogado), então não é reescrita do mesmo conteúdo — mas o eixo 1
precisa evitar repetir a **mesma frase de efeito** ("X não é Y") sem
mecanismo novo por trás, sob risco de soar como o 4.1 com curativo
trocado.

### 4.3 (Defesa em profundidade) — colisão leve conceitual, não de mecanismo

`4.3.t6` (Zero Trust: o que muda na decisão de acesso) e `4.3.t3` (falha
de modo comum: camadas que parecem independentes e caem pelo mesmo
motivo) tocam adjacente ao eixo 2 (fronteira de confiança) — falha de
modo comum é sobre camadas de defesa correlacionadas, fronteira de
confiança é sobre onde, no desenho, dois componentes deixam de confiar
um no outro. Mecanismos diferentes, mas ambos tratam de "onde a
suposição de proteção quebra".

**O que sobra de fato**: eixo 2 fica livre se ficar em **decomposição do
sistema** (que componente fala com qual, onde a confiança muda de nível)
— isso 4.3 nunca faz, ele fala de camada de controle (preventivo/
detectivo/corretivo), não de fronteira entre componentes de um desenho.

### 1.4 (Redes I) — colisão leve, resolvida por referência

`1.4.t3`/`1.4.t4` (público/privado, NAT) já ensinam que tradução de
endereço não é fronteira de segurança por si só. Se o eixo 2 usar rede
como exemplo de fronteira de confiança, precisa citar isso como
conhecido, não reexplicar NAT.

**O que sobra de fato**: tudo, desde que o exemplo de fronteira de
confiança não seja rede pública/privada — um exemplo de dois **processos
de aplicação** trocando dado (ex.: serviço A confia cegamente no valor
que o serviço B manda) ilustra o mecanismo sem tocar em IP/NAT.

### 5.1 (Desenvolvimento seguro) e 5.2 (Segurança em nuvem) — sem colisão de mecanismo, cuidado de sequência

Nenhum dos dois ensina modelagem de ameaça como método. Mas os dois já
estabeleceram a tese "pensar em segurança cedo é mais barato" (5.1.t1/t2)
e "a linha de responsabilidade não desaparece, ela se desloca" (5.2.t1) —
modelagem de ameaça é, em certo sentido, a ferramenta que **operacionaliza**
"pensar cedo" do 5.1. O eixo 1 pode e deve citar 5.1 como o motivo de a
pergunta valer a pena ser feita cedo, sem reensinar o argumento de custo
composto.

**Nenhuma colisão de mecanismo com 5.2** — identidade de carga de
trabalho, responsabilidade compartilhada e infraestrutura efêmera são
mecanismos específicos de nuvem, não do método de modelagem de ameaça em
si (que é aplicável a qualquer sistema, com ou sem nuvem).

### 3.7 (OWASP Top 10) — fora da lista pedida, colisão de forma argumentativa no eixo 1, verificado por iniciativa própria

3.7 já fez, para uma lista diferente, exatamente o argumento que o eixo 1
propõe: "a lista como instrumento, não catálogo de siglas reensinadas".
O objeto de 3.7 é uma lista de **vulnerabilidades já exploradas e
catalogadas por prevalência** (OWASP Top 10); o objeto do eixo 1 é a
**ausência de lista** — modelar ameaça é o que se faz quando não existe
catálogo prévio cobrindo o sistema específico que está sendo desenhado.

**O que sobra de fato**: a diferença é genuína (catálogo de prevalência
histórica × antecipação sem catálogo), mas o eixo 1 precisa nomear essa
diferença explicitamente logo no início, ou vai soar como "3.7 de novo,
com o nome trocado" para quem já viu os dois módulos.

## Resumo por eixo do recorte proposto

| eixo | colide com | gravidade | ação |
|---|---|---|---|
| 1. o que é modelar ameaça / lista não é isso | 4.1.t6 (forma), 3.7 (forma, fora da lista) | leve, de forma | nomear a diferença logo no início: antecipação sem catálogo × lista de vulnerabilidade/checklist já existente |
| 2. decompor o sistema / fronteira de confiança | 4.3 (leve), 1.4 (leve, resolvido por referência) | leve | manter, exemplo de fronteira entre dois processos de aplicação, não rede pública/privada |
| 3. vocabulário de categorias | 2.6 (REAL), 3.6 (REAL) | **severa** | ancorar toda categoria em sistema sendo desenhado, nunca em aplicação web já construída ou modelo de RBAC já ensinado |
| 4. priorizar/aceitar/mitigar | 3.1.t6 (leve) | leve | nomear a diferença temporal: triagem de projeto (antes) × triagem de achado confirmado (depois), citar 3.1 por referência |
| 5. limite honesto / modelo envelhece | nenhum módulo específico, padrão retórico repetido no corpus | nenhuma de conteúdo | manter, mecanismo próprio (mudança do sistema invalida o modelo) |

Nenhum eixo precisa ser eliminado. O eixo 3 é o único com colisão severa
de mecanismo (não só de forma) — precisa da amarra mais forte antes de
escrever: cada categoria de ameaça tem que ser demonstrada num sistema
inventado em fase de desenho, nunca reaproveitando o exemplo de RBAC do
2.6 ou de autorização web do 3.6.
