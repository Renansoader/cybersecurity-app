# Levantamento de não-repetição — módulo 5.4 (GRC: governança, risco e conformidade)

Método: leitura dos objetivos e títulos de teoria dos 6 módulos apontados
(5.3, 5.2, 4.1, 2.6, 3.7, 0.3), não só grep — GRC é o módulo com maior
risco de virar vocabulário corporativo sem mecanismo do curso inteiro, o
risco real não é palavra repetida, é a mesma decisão já ensinada em outro
lugar sendo reembalada com nome novo.

## Por módulo

### 5.3 (Modelagem de ameaças) — colisão REAL no eixo 2 (risco como comparação)

`5.3.t5` já ensina triagem de um risco encontrado num exercício de
modelagem: mitigar, aceitar ou transferir, comparando custo de mitigação
contra dano esperado — **caso a caso, um risco hipotético por vez**,
descoberto num fluxo específico de um sistema em desenho.

**O que sobra de fato**: o eixo 2 proposto aqui não pode ser "a mesma
triagem, de novo" — precisa ser sobre o problema que só aparece quando
existem **muitos riscos ao mesmo tempo, de fontes diferentes, competindo
pelo mesmo orçamento de correção**: como comparar um risco técnico
(vulnerabilidade num servidor) com um risco de fornecedor e um risco de
processo, todos com "score" numérico, quando os números não têm a mesma
base de confiança nem a mesma unidade real por trás. 5.3 nunca compara
dois riscos entre si — só decide o que fazer com um. GRC compara muitos,
e o eixo 2 precisa nomear essa diferença de escopo explicitamente (triagem
de um risco × comparação de portfólio de riscos), citando `5.3.t5` como
referência do primeiro caso, não reensinando.

### 4.1 (Hardening) — colisão REAL no eixo 3 (conformidade × segurança)

`4.1.t6` ("o limite do checklist: conformidade não é segurança") já é,
literalmente, metade do argumento proposto para o eixo 3 — e numa unidade
de análise específica: desvio de **linha de base de configuração técnica**
contra um benchmark.

**O que sobra de fato**: o eixo 3 não pode se limitar a repetir essa
metade (conformidade sem segurança) — precisa fechar o **erro simétrico**,
que 4.1 nunca trata: segurança real sem conformidade demonstrável (um
controle que funciona, mas que ninguém registrou, então não sobrevive a
uma auditoria nem a uma transição de equipe). A unidade de análise também
muda: 4.1 é sobre configuração de uma máquina; o eixo 3 do 5.4 é sobre
conformidade **organizacional** com um marco de governança (framework,
contrato, obrigação regulatória — sem nomear qual). `4.1.t6` deve ser
citado como a metade já coberta, nunca reescrito.

### 2.6 (Controle de acesso) — colisão leve, resolvida por escopo

2.6 ensina **modelos técnicos de controle de acesso** (DAC, MAC, RBAC,
ABAC, Zero Trust) e quem decide tecnicamente uma permissão. O eixo 1
proposto ("quem decide, com base em quê, dono nomeado") corre risco de
soar parecido se usar exemplo de permissão de acesso.

**O que sobra de fato**: 2.6 nunca trata de **quem tem autoridade
organizacional para aceitar um risco, aprovar uma exceção ou responder
por uma decisão de segurança perante auditoria** — isso é ortogonal ao
mecanismo técnico de como uma permissão é armazenada ou avaliada. O eixo
1 fica livre se o exemplo nunca for "quem pode ler este arquivo" (2.6) e
sempre for "quem assina que este risco fica assim mesmo" — decisão sobre
decisão, não sobre acesso.

### 3.7 (OWASP Top 10) — colisão leve de forma retórica, não de mecanismo

3.7 fecha com "instrumento, não prova": cobrir as dez categorias do Top
10 não prova que a aplicação está segura. É a mesma forma retórica do
eixo 4 proposto ("'nós fazemos isso' e 'conseguimos mostrar que fazemos'
são coisas diferentes").

**O que sobra de fato**: o mecanismo é diferente — 3.7 é sobre os limites
de uma lista de categorias de vulnerabilidade técnica como prova de
segurança de uma aplicação; o eixo 4 do 5.4 é sobre **evidência de
processo organizacional** (existe registro de que um controle rodou,
independente de a aplicação estar seguro ou não). Não é reescrita, mas o
eixo 4 precisa evitar repetir a mesma frase de efeito sem mecanismo novo
por trás — nomear a diferença (lista de categoria técnica × trilha de
evidência de processo) já na primeira questão do eixo.

### 5.2 (Segurança em nuvem) — colisão leve de vocabulário, não de mecanismo

`5.2.t1` fala de responsabilidade compartilhada entre provedor e cliente
— "quem decide o quê" também aparece lá, mas numa dimensão técnica
específica (qual camada da pilha cada lado opera).

**O que sobra de fato**: nenhuma colisão de mecanismo — 5.2 nunca trata
de autoridade organizacional para aceitar risco ou de trilha de
auditoria. Cuidado só de vocabulário: o eixo 1 não deve usar "linha de
responsabilidade" como frase de efeito sem diferenciar do sentido técnico
já fixado em 5.2.

### 0.3 (Quem é o adversário) — colisão leve de forma, não de mecanismo

`0.3.t6` ("do adversário para o plano: defesa proporcional") ensina a
proporcionalizar defesa pelo perfil do atacante (motivação × capacidade)
— outra forma de "decisão proporcional a alguma coisa", parecida em
formato com o eixo 2 (risco como número que orienta decisão).

**O que sobra de fato**: mecanismos totalmente diferentes — 0.3 decide a
partir do **perfil do atacante**, um eixo qualitativo de dois fatores;
GRC decide a partir de **comparação numérica entre riscos heterogêneos**
num portfólio, sem depender de nomear um adversário específico. Nenhuma
reescrita necessária, só evitar a mesma frase de efeito ("resposta
proporcional") sem apontar o que está sendo comparado a quê.

## Resumo por eixo do recorte proposto

| eixo | colide com | gravidade | ação |
|---|---|---|---|
| 1. governança — quem decide, dono nomeado | 2.6 (leve), 5.2 (leve, vocabulário) | leve | exemplo nunca sobre permissão de acesso (2.6) nem sobre camada técnica (5.2) — sempre sobre autoridade de aceitar risco/exceção |
| 2. risco como comparação, não sentimento | 5.3.t5 (REAL), 0.3.t6 (leve, forma) | **severa** | nomear a diferença de escopo: triagem de um risco (5.3) × comparação de portfólio de riscos heterogêneos (5.4); nunca decidir sobre um adversário nomeado (0.3) |
| 3. conformidade × segurança, erros simétricos | 4.1.t6 (REAL, metade do argumento) | **severa** | citar 4.1 como a metade já coberta (conformidade sem segurança); eixo só se justifica pelo erro simétrico (segurança sem conformidade demonstrável) |
| 4. auditoria e evidência | 3.7 (leve, forma retórica) | leve | nomear mecanismo novo (trilha de evidência de processo) na primeira questão, não só repetir "cobertura não é prova" |
| 5. limite honesto do GRC | nenhum módulo específico, padrão retórico já usado em 5.3.t6/3.7.t4/4.1.t6 | nenhuma de conteúdo, risco de fórmula repetida | mecanismo próprio: GRC governa decisão e papel, não impede ataque nem detecta técnica nova — um risco aceito e assinado por autoridade correta ainda pode virar incidente real |

Nenhum eixo precisa ser eliminado. Eixos 2 e 3 têm colisão severa de
mecanismo (não só de forma) e precisam da amarra mais forte antes de
escrever — ver crítica ao recorte abaixo.

## Achado próprio: molde de MÓDULO, não de dica — "o limite honesto do método" como fecho

Os três últimos módulos do nível 5 (5.1, 5.2, 5.3) fecham, todos, com um
bloco de teoria estruturado como "aqui está o limite honesto do que este
método não cobre, mesmo aplicado corretamente" — e o eixo 5 proposto aqui
para o 5.4 repetiria o padrão pela quarta vez seguida. Isso não é o mesmo
tipo de achado que as nove variantes de molde de dica já catalogadas
(§5/§7 do PROGRESS.md): aquelas vivem no nível da frase (prefixo de dica,
qualificador de alternativa). Esta vive no nível da **arquitetura do
módulo** — a mesma forma de fechar um conteúdo inteiro, reaplicada sem
que nenhuma ferramenta do projeto (`chutador_de_forma.py`,
`medidor_molde_dica.py`, `validar_modulo.py`) meça esse nível, porque
todas operam dentro de uma questão ou de um módulo isolado, nunca
comparando a forma estrutural entre módulos.

Para o 5.4, a exigência não é abandonar o eixo 5 (o limite do GRC é
mecanismo genuíno, ver tabela acima) — é blindar contra a fórmula: cada
questão do eixo 5 precisa de um **caso concreto onde o processo foi
seguido corretamente e mesmo assim falhou** (risco aceito, assinado,
revisado no prazo, e mesmo assim virou incidente real). Uma questão do
eixo 5 que funciona sem esse caso concreto é a frase de efeito de novo,
sem mecanismo por trás — mesmo critério de descarte já usado para molde
de dica, aplicado agora um nível acima.
