# Levantamento de não-repetição — módulo 5.1 (Desenvolvimento seguro)

## Nível 5 pode assumir tudo — confirmado, não suposto

`data/niveis.json`: nível 5 desbloqueia com `dominio` sobre `niveis: [3, 4]`,
mínimo 0,6. Como nível 3 e nível 4 desbloqueiam do nível 2, e nível 2 do
nível 1, e nível 1 do nível 0 — a cadeia inteira (0,1,2,3,4) é assumível a
partir do nível 5, o único nível para o qual isso vale sem ressalva. Primeiro
módulo do nível 5, e o único ponto do curso em que citar qualquer módulo
anterior como já visto é sempre válido.

## Método

Mesmo método dos levantamentos anteriores: contagem de menções por
padrão/regex nos 35 módulos publicados, cada acerto lido em contexto antes
de contar como colisão real.

## Eixo por eixo

### Eixo 1 — onde a decisão é barata (custo de corrigir cedo × tarde)

Busca por "custo de corrigir", "corrigir no desenho", "shift left", "mais
barato corrigir": **zero ocorrências em qualquer módulo.** Território
inteiramente livre.

### Eixo 2 — o que você herda sem escrever (dependência, versão transitiva)

**Colisão real, parcial.** `3.7` (OWASP Top 10) já usa duas questões nesse
território, mas só como exercício de classificação, não de mecanismo:

- `3.7.q30`: biblioteca desatualizada com vulnerabilidade conhecida há seis
  meses → mapeada para A03 Software Supply Chain Failures. A explicação
  para no diagnóstico ("a correção já existe e não foi aplicada"), não
  explica o que é uma árvore de dependências nem por que uma dependência
  transitiva existe.
- `3.7.q31`: atualização automática sem verificar assinatura → mapeada para
  A08 Software or Data Integrity Failures. Sobre integridade da cadeia de
  distribuição, não sobre herança de código-fonte.

`1.7.t6` (Git) menciona a cadeia de dependências de passagem: "o repositório
declara de que bibliotecas o projeto depende, e cada uma é código de
terceiro que entra no seu programa" — uma frase, sem desenvolver o
mecanismo de dependência **transitiva** (a dependência da sua dependência,
que você nunca escolheu diretamente).

**O que sobra livre**: por que uma dependência transitiva é código seu de
fato mesmo sem você tê-la visto (a árvore inteira, não só o pacote que você
digitou), e por que "não escrevi isso" não transfere responsabilidade —
nenhum módulo publicado desenvolve esse argumento estrutural. 3.7 classifica
o sintoma (dependência desatualizada = qual categoria); ninguém explica a
causa (por que a árvore existe e por que ela é sua).

**Reformulação proposta**: o eixo 2 não reclassifica os cenários que 3.7 já
classificou — cita `3.7.q30`/`q31` como referência cruzada ("essa forma de
achado já foi vista e categorizada") e constrói em cima: o mecanismo da
árvore transitiva, e por que a decisão de adicionar uma dependência é, na
prática, a decisão de confiar numa árvore inteira que você nunca leu.

### Eixo 3 — segredo em código e configuração

**Colisão severa — quase o mesmo argumento já publicado.** `1.7` (Git) tem
três blocos de teoria dedicados a exatamente esta tese:

- `1.7.t3`: "quando uma credencial vai para o repositório, a primeira
  reação costuma ser errada: apagar o arquivo e commitar. Isso não remove
  nada... A única resposta correta é tratar a credencial como comprometida
  e rotacioná-la."
- `1.7.t4`: limite do `.gitignore` — só afeta arquivo ainda não rastreado.
- `1.7.t5`: "prevenir é muito mais barato" — variável de ambiente, cofre,
  revisão antes de commitar, verificação automática.

Isso é literalmente "o problema não é o vazamento, é o ciclo de vida — e
remover do commit não resolve", a tese que o pedido original propôs para o
eixo 3. Publicar esse eixo como proposto seria republicar 1.7 com palavras
diferentes.

**O que sobra livre**: 1.7 é inteiramente sobre o **histórico do Git**
especificamente — commit, clone, reescrita de histórico. Nenhum módulo
cobre o resto do ciclo de vida de um segredo num sistema em produção: log
de pipeline de CI, imagem de contêiner ou artefato de build que embute a
credencial, mensagem de erro ou despejo de memória que a expõe em runtime.
E nenhum módulo conecta o problema à raiz estrutural: segredo estático
(uma string que nunca muda, compartilhada por tudo que precisa dela) tem a
mesma fraqueza que `3.9` já demonstrou para senha de rede em modo pessoal —
ninguém revoga uma cópia sem invalidar todas — o que explica, por
mecanismo e não por regra decorada, por que um cofre de segredo com
credencial dinâmica e de curta duração é estruturalmente diferente de
"esconder bem uma string fixa".

**Reformulação proposta**: o eixo 3 muda de "segredo commitado" (já é 1.7)
para "segredo tem ciclo de vida em cima do código inteiro, não só dentro
do repositório" — cross-referencia `1.7.t3` para a resposta já ensinada
(rotacionar, não apagar) sem reensinar, e cobre o que fica de fora do git:
pipeline, imagem, runtime — fechando com a conexão estrutural a `3.9`
(segredo estático × identidade dinâmica), backward, nível 3 para nível 5,
válido.

### Eixo 4 — revisão e teste automatizado como rede

Busca por "revisão de código", "teste automatizado", "SAST", "DAST",
"linter", "pipeline de CI": achados em `3.1`, `3.2`, `3.3`, `3.5`, `3.7`,
todos lidos em contexto — nenhum é o argumento "o que a automação pega, o
que ela nunca vai pegar". `3.5.q6` é o mais próximo (revisão de código
encontrando 50 consultas SQL repetidas), mas o ponto ali é "corrigir só o
primeiro exemplo não corrige o padrão" — sobre repetição de defeito, não
sobre o limite estrutural do que ferramenta automatizada enxerga. Nenhum
módulo desenvolve por que teste automatizado prova ausência de padrão
conhecido e nunca prova ausência de falha, nem por que isso decide onde
colocar atenção humana. **Território livre.**

### Eixo 5 — segurança como etapa final de entrega

Busca por "etapa final", "gate final", "última etapa": três achados
(`0.4`, `3.1`, `4.8`), todos sobre assuntos diferentes (descarte seguro de
mídia, triagem pós-achado de pentest, ordem de verificação forense — não
"segurança tratada como última etapa do processo de construir software").
**Território livre.**

## Recorte final, depois da medição

1. **Onde a decisão é barata** — livre, sem alteração.
2. **O que você herda sem escrever** — mantido, com cross-referência
   explícita a `3.7.q30`/`q31` (não reclassifica, constrói o mecanismo por
   trás).
3. **Segredo tem ciclo de vida em cima do código** — reformulado: sai do
   território do commit (já é 1.7) para o resto do ciclo de vida
   (pipeline, artefato de build, runtime) mais a conexão estrutural com o
   modelo de identidade de `3.9`.
4. **Revisão e teste automatizado como rede** — livre, sem alteração.
5. **O contraponto: segurança como etapa final** — livre, sem alteração.

Referências cruzadas deste módulo, todas backward e válidas pela tabela de
desbloqueio (nível 5 assume 0-4 inteiro): `1.7.t3` (segredo commitado),
`3.7.q30`/`q31` (classificação de dependência/integridade), `3.9.t5`
(segredo estático não distingue identidade), `4.1` (linha de base e
correção por risco, se necessário para o contraponto).
