# O que os módulos publicados já ensinam — não repetir no 3.6

Levantado em 03/09/2026, sobre os 31 módulos publicados (1.086
questões). O 3.6 (Web III) fecha o bloco Web e encosta em 2.6
(controle de acesso, já publicado e testado), 3.4 e 3.5 (recém-
escritos), 3.7 (OWASP Top 10, ainda não escrito). O aviso do usuário
apontava "2.3 e 2.4" como donos de RBAC/menor privilégio — **os
números estão errados**: por título e conteúdo, quem é dono disso é o
**2.6** (2.3 é Criptografia III, 2.4 é Hash e senhas; nenhum dos dois
menciona controle de acesso). Conferido antes de escrever qualquer
questão, como o aviso pediu.

## Colisão real e severa (achada) — 2.6 já ensina IDOR como mecanismo, não como sigla

**2.6 (Controle de acesso) tem 6 das 35 questões (17%) sobre
referência direta insegura a objeto, com o mesmo enquadramento que o
eixo 2 do 3.6 propõe** — "o mecanismo, não o nome da sigla":

- **2.6.q19**: cenário com endpoint de pedidos, id trocado de 1234
  para 1235, servidor responde com o pedido de outra pessoa.
  `pergunta_socratica`: *"O servidor sabe quem está pedindo. Ele
  chegou a checar se o pedido é dessa pessoa?"* `explicacao` nomeia
  IDOR, cita OWASP A01 (34 CWEs mapeadas) e distingue autenticação
  ("quem é") de autorização por objeto ("pode ver aquele objeto").
- **2.6.q20**: "qual correção realmente fecha o IDOR" — descarta
  esconder link (controle no cliente), id aleatório (ofuscação, não
  autorização) e rate limit (reduz varredura, não fecha o acesso
  pontual); a resposta é verificação de propriedade no servidor, "em
  um lugar reutilizável, e não repetida em cada handler".
- **2.6.q30**: por que id aleatório não é solução de menor privilégio
  (a decisão continua sem checar o recurso).
- **2.6.q32**: ordem de prioridade para herdar um sistema com "IDOR
  nos endpoints, sem revisão de acesso e com permissão por usuário" —
  a resposta começa pelo IDOR, por ser explorável agora por qualquer
  conta autenticada.
- **2.6.q33, q35**: tangenciais (RBAC/Zero Trust citando IDOR como
  exemplo de quebra de controle de acesso na aplicação, sem ensinar
  mecanismo novo).

**2.6 é dono de**: o mecanismo de IDOR (id previsível, servidor não
confere propriedade), a correção correta (verificação de propriedade
no servidor, não ofuscação nem controle no cliente) e a priorização
por explorabilidade. Isso é exatamente o eixo 2 da proposta do usuário
("trocar um identificador na requisição e receber o recurso de outra
pessoa — o mecanismo, não o nome da sigla") — **não pode ser reescrito
como conteúdo novo no 3.6**, sob pena de ser a mesma pergunta com
número de questão diferente.

## Colisão parcial (achada) — 3.4 já estabeleceu "decisão sempre no servidor"

O objetivo 1 do 3.4 é literal: *"Explicar por que a decisão de
segurança de uma ação sempre precisa acontecer no servidor, nunca na
interface que a solicita"* — e o objetivo 3, *"validação client-side é
conveniência para o usuário legítimo, não controle contra quem decide
contornar a interface"*. O eixo 1 proposto para o 3.6 ("por que
esconder o botão não protege nada, e por que a verificação precisa
acontecer em cada requisição") **é a mesma premissa do 3.4, aplicada a
autorização em vez de a qualquer decisão de segurança**.

Não é a mesma questão do caso do 2.6 (ali era o mecanismo inteiro
duplicado; aqui é a premissa geral já estabelecida servindo de
alicerce para uma aplicação nova), mas escrever o eixo 1 como se "servidor
decide, não a tela" fosse novidade repete o argumento central do 3.4.
**Formulação final do eixo 1**: assume "a decisão é do servidor" como
fato já ensinado (referência cruzada a 3.4.t1), e a pergunta nova do
3.6 é a que 3.4 não fez — **dado que o servidor decide, decidir o quê
exatamente?** Autenticado ≠ autorizado para *este* objeto específico é
o corte: 3.4 ensinou "onde" a decisão mora; 3.6 ensina "sobre qual
escopo" ela precisa avaliar (o recurso pedido, não só a sessão).

## Território livre confirmado — escalada horizontal/vertical e lógica de negócio

Varredura por `escalada horizontal`, `escalada vertical`, `privilégio
horizontal/vertical`, `lógica de negócio` no corpus inteiro: nenhuma
ocorrência fora de contexto não relacionado (o único hit de
"escalação de privilégio" é `1.1` — Linux, sudo/SUID, escalonamento de
privilégio de sistema operacional local, categoria totalmente
diferente da escalada de conta via requisição web). **Zero questões
publicadas ensinam a mesma falha vista de ângulos horizontal/vertical,
e zero ensinam abuso de lógica de negócio (ordem de etapas, valor fora
do intervalo do formulário).** Território livre confirmado para os
eixos 3 e 4 do usuário.

## 3.5 — Web II (recém-escrito)

Injeção (SQL, XSS, comando) como confusão dado/instrução. Nenhuma
menção a autorização, objeto, escalada ou lógica de negócio. Sem
colisão — os dois módulos ficam claramente distintos: 3.5 é sobre dado
que vira instrução; 3.6 é sobre requisição sintaticamente correta que
não deveria ter sido atendida.

## 3.7 — OWASP Top 10 (ainda não escrito)

Reservado pelo usuário como dono da lista. O 3.6 não pode virar
catálogo de siglas (IDOR, BOLA, BFLA como nomenclatura) — ensina o
**mecanismo de autorização por objeto** e deixa a nomenclatura OWASP
como referência de passagem (mesmo tratamento que 2.6.q19 já deu:
nomear uma vez, na explicação, sem fazer da sigla o objeto de estudo).
Quando o 3.7 for escrito, ele assume que o aluno já reconhece a falha
por trás da sigla.

## 3.1, 3.2, 3.3 — Metodologia, OSINT, varredura

Sem menção a autorização, objeto ou controle de acesso em nenhuma
questão. Sem colisão.

---

## Território proposto para o 3.6, e a troca

| Eixo | Proposta original | Risco | Formulação final |
|---|---|---|---|
| 1 | Autorização por objeto, não por tela — esconder botão não protege, verificação a cada requisição | **Parcial** — premissa "servidor decide" é o objetivo 1 do 3.4 | Reformulado: assume "servidor decide" como já ensinado (3.4.t1), pergunta nova é *sobre qual escopo* — autenticado ≠ autorizado para o objeto específico |
| 2 | Referência direta a objeto — trocar identificador, receber recurso de outra pessoa, o mecanismo | **Severo** — 2.6 já ensina isso com 6 questões (mecanismo, correção certa, priorização) | **Substituído**: o 3.6 não reensina o mecanismo de IDOR nem sua correção (referência cruzada explícita a `2.6.q19`/`q20`); assume o aluno já reconhece "id trocado, servidor não confere dono" e usa esse caso como ponto de partida conhecido para os eixos 3 e 4, que 2.6 não cobre |
| 3 | Escalada horizontal e vertical como a mesma falha vista de ângulos diferentes | Nenhum — território livre confirmado | Mantido |
| 4 | Lógica de negócio — requisição válida, ordem errada, valor que o formulário nunca ofereceria | Nenhum — território livre confirmado | Mantido, e vira o eixo com mais peso do módulo já que o eixo 2 original foi absorvido pelo 2.6 |

A troca no eixo 2 é a mais estrutural desta série até agora: não é uma
reformulação de enquadramento (como no 3.4/3.5), é a remoção do eixo
como conteúdo novo, porque 2.6 já o esgotou com o mesmo enquadramento
que o usuário pediu.

## Eixo 2 novo (substituto) — confirmado livre, 03/09/2026

Proposta do usuário pro espaço vago: "a aplicação tem mais portas de
entrada do que telas" — API que o app usa, endpoint legado, parâmetro
de versão, verbo HTTP não testado — e onde a verificação de
autorização deveria morar para que esquecer uma porta não abra o
cofre. Varredura por `endpoint`, `API`, `método HTTP`, `verbo HTTP`,
`versão da requisição` no corpus inteiro:

- **3.2 (OSINT)**: zero ocorrências de `endpoint`. Objetivo 2 fala em
  "mapa de superfície a partir de fonte pública" — DNS, certificado,
  metadado — território de descoberta passiva, nada sobre onde a
  verificação de autorização deveria morar. Sem colisão.
- **3.3 (Varredura e enumeração)**: zero ocorrências de `endpoint`.
  `3.3.t5` ensina o limite da enumeração de conteúdo web ("não
  encontrado" significa "não estava na wordlist", nunca "não existe")
  — claim sobre a **técnica de descoberta**, não sobre **arquitetura
  de autorização**. Risco de família retórica (os dois falam de
  "caminho escondido que existe mesmo sem ter sido encontrado"), não
  de conteúdo: 3.3 é a perspectiva de quem procura de fora sem
  credencial; o eixo 2 do 3.6 é a perspectiva de quem já tem acesso a
  uma porta e pode ter esquecido de proteger outra. Cross-reference
  explícita evita repetição silenciosa, mesmo padrão já usado entre
  3.4/3.5.
- **4.1 (Hardening)**: único hit de `endpoint` é literal — "RPC
  endpoint mapper" (porta 135, serviço Windows), não rota de API. Sem
  relação. Objetivo 2 ("reduzir superfície: serviço, porta, conta,
  recurso") é sobre desligar o que não precisa existir — infraestrutura
  e sistema operacional, não roteamento de aplicação web. Sem colisão.
- **0.2 (Superfície de ataque)**: define vetor/ponto de
  entrada/movimento lateral como vocabulário geral, nível 0, sem
  nenhuma especificidade web. Terreno citável (vocabulário anterior),
  não posse do conteúdo do eixo.

**Livre.** Nenhum módulo publicado ensina que a verificação de
autorização precisa viver num ponto central (middleware/camada de
roteamento) em vez de replicada por handler, nem a consequência de
replicá-la (rota nova, verbo esquecido, versão antiga = buraco novo).

## Recorte final dos 4 eixos

O peso que o eixo 2 original teria (removido, ver acima) vai para o
eixo 2 novo (superfície de rotas/verbos e ponto central de
verificação) — o módulo mantém 4 eixos de peso comparável, não 3 mais
um sobrecarregado:

1. Escopo da autorização sobre o objeto pedido (assume "servidor
   decide" do 3.4; pergunta nova é sobre qual escopo).
2. **Novo**: superfície de rotas/verbos/versões e por que a
   verificação precisa morar num ponto central, não replicada.
3. Escalada horizontal e vertical como a mesma falha por ângulos
   diferentes.
4. Lógica de negócio — requisição válida, ordem ou valor que o
   formulário nunca ofereceria.

Confirmado, pronto para escrever.
