# O que os módulos publicados já ensinam — não repetir no 3.4

Levantado em 02/09/2026, sobre os 29 módulos publicados (1.016 questões).
O 3.4 (Web I) é o primeiro módulo do bloco ofensivo depois de 3.1-3.3 e
encosta em 1.4/1.5 (redes, HTTP, TLS), 2.x (autenticação, sessão,
controle de acesso), 3.1 (metodologia) e 3.2 (reconhecimento). Uma
colisão real e severa achada, não prevista no aviso do usuário.

## Colisão real e severa (achada, não estava no aviso) — 2.5 já é dono do eixo 2 quase por inteiro

**2.5 (Autenticação e identidade) tem um objetivo inteiro dedicado a
sessão e cookie, quase palavra por palavra o eixo 2 proposto:**

- **Objetivo declarado do 2.5**: *"Explicar como sessão e cookie
  sustentam o login e quais atributos e ciclos protegem a sessão"* — é
  o eixo 2 do 3.4 ("HTTP não guarda estado, sessão é invenção em cima
  dele") quase literalmente.
- **2.5.t3**, título *"Sessão e cookie: o que sobra depois do login"*.
- **2.5.q12**: *"Por que uma aplicação web precisa de sessão depois do
  login?"* — a pergunta central do eixo 2 proposto, já respondida.
- **2.5.q13**: o que `HttpOnly`, `Secure` e `SameSite` fazem no cookie
  de sessão.
- **2.5.q14**: fixação de sessão (identificador vindo pela URL,
  reaproveitado após login).
- **2.5.q15**: o que é preciso para logout realmente encerrar a sessão.
- **2.5.q16**: caça-erro sobre atributos de cookie de sessão.
- **2.5.q17**: propriedades que o identificador de sessão precisa ter
  (entropia, CSPRNG).
- **2.5.q18**: ordenação do ciclo de vida de uma sessão bem construída.
- **2.5.q19**: expiração por inatividade x expiração absoluta.

**2.5 é dono de**: por que sessão existe, os atributos de cookie que a
protegem (`HttpOnly`/`Secure`/`SameSite`), fixação de sessão, logout,
entropia do identificador, ciclo de vida completo — a mecânica e a
defesa da sessão, em profundidade. O 3.4 não pode reabrir "por que
sessão existe" nem "quais atributos protegem o cookie" como conteúdo
novo — seria o mesmo defeito de repetição que a seção 5 do PROGRESS.md
já lista como dívida.

## 1.5 — Redes II (transporte, HTTP e TLS)

- **1.5.t3 (objetivo 3)**: diferença entre HTTP e HTTPS, o que o
  certificado prova e o que não prova.
- **1.5.t4 (objetivo 4)**: handshake do TLS 1.3.
- **1.5.q13, q28**: códigos de status HTTP e o que dizem no log.
- **1.5.q24**: diferença prática entre GET e POST — já cita "segredos"
  e "logs" (GET expõe parâmetro na URL, cai em log e histórico).
- **1.5.q9, q30**: o que um certificado de validação de domínio prova
  (nada sobre a idoneidade do operador do site) — território de
  phishing/certificados, não de arquitetura de aplicação web.

**1.5 é dono de**: a distinção HTTP/HTTPS, o handshake TLS, o que um
certificado prova, os métodos GET/POST e por que GET vaza dado em log.
O 3.4 não redefine nenhum desses — usa como pré-requisito. Nenhuma
questão do 3.4 deveria perguntar "o que HTTPS acrescenta" ou "que
método HTTP usar" como se fosse achado novo.

## 2.6 — Controle de acesso

- **2.6.t1-t6**: DAC, MAC, RBAC, ABAC, Zero Trust — modelos gerais de
  decisão de acesso, aplicados a arquivos, sistemas e organizações.

**2.6 é dono de**: os modelos de controle de acesso em si (quem decide
o quê, com que critério). Não é dono da fronteira específica
cliente/servidor numa requisição HTTP — o eixo 1 e o eixo 3 do 3.4
("decisão sempre no servidor", "cliente nunca é confiável") tratam de
uma camada mais concreta e específica da web, sem redefinir os modelos
de controle de acesso do 2.6. Diferenciação a manter explícita no
texto, pela proximidade de tema.

## 3.1 — Metodologia de pentest

Fases, escopo, regras de engajamento, relatório como produto — processo
de teste, não técnica de exploração web. Sem colisão.

## 3.2 — OSINT e reconhecimento

Reconhecimento passivo/ativo, DNS/whois, transparência de certificado,
vazamento documental — fase de coleta de informação antes do ataque,
não exploração de aplicação em si. Sem colisão.

## 2.1–2.4, 2.7

Criptografia (simétrica, assimétrica, quebra prática), hash e senhas,
fator humano — nenhuma questão sobre requisição HTTP, sessão como alvo
web, mesma origem ou validação client-side encontrada nessas buscas.
Sem colisão.

---

## Território proposto para o 3.4, e a troca

| Eixo | Proposta original | Risco | Formulação final |
|---|---|---|---|
| 1 | Ciclo requisição/resposta: decisão de segurança sempre no servidor | Nenhum | Mantido — sem colisão |
| 2 | HTTP não guarda estado, sessão é invenção, tudo que carrega identidade vira alvo | **Severo** — objetivo inteiro e 8 questões do 2.5 | **Reformulado**: a mesma invenção que sustenta login (sessão/cookie, já ensinada no 2.5) é reenviada pelo navegador de forma automática, para qualquer requisição, não importa quem pediu — é esse reenvio automático, não a sessão em si, que abre a porta pro CSRF. O 3.4 não reensina atributo de cookie; usa `SameSite` (já ensinado em 2.5.q13) como a defesa que a mecânica do próprio protocolo exige |
| 3 | Cliente nunca é confiável: validação só no navegador é sugestão | Nenhum | Mantido — sem colisão |
| 4 | Regra de mesma origem: por que existe, o que acontece quando afrouxada | Nenhum | Mantido — sem colisão; conecta naturalmente com o eixo 2 reformulado (CSRF é o caso em que o navegador NÃO aplica a barreira de origem ao *enviar*, só ao *ler a resposta*) |

Decisão pendente de confirmação do usuário antes de escrever qualquer
questão — só o eixo 2 muda, e a mudança é a mesma família de troca já
usada no 4.7 (technical-mechanics já ensinado em outro módulo → eixo
vira a camada seguinte, não coberta).
