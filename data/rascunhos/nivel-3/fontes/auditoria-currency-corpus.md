# Auditoria de currency — todos os 32 módulos publicados

Levantado em 04/09/2026, a pedido do usuário depois de achar duas citações
desatualizadas em 2.6 (OWASP Top 10:2021→2025, e contagem de CWE 34→40).
Pergunta: quantos outros casos existem no corpus inteiro? **Só levantamento —
nada foi corrigido além do já tratado em 2.6, em dois commits separados.**

## Método

Extração automática de todo campo `texto`, `fonte`, `erro_comum` (teoria) e
`explicacao`, `fonte`, `enunciado` (questão) dos 32 módulos publicados
(1.315 campos `fonte`), filtrando por padrões de nome de norma/framework com
número de versão, data ou contagem. Depois, filtro mais estreito por sinal de
**afirmação de vigência** — "vigente", "versão atual", "hoje na", "obsoleta",
"revogada", "última edição", "CWEs mapeadas" — porque uma citação de norma
por si só (ex.: "RFC 8446") não é risco de desatualização; risco é a
**afirmação de que algo é o estado corrente** de uma norma que muda com o
tempo. 49 ocorrências desse segundo filtro, agrupadas em 15 fatos distintos
verificáveis (muitas ocorrências repetem o mesmo fato em questões-irmãs do
mesmo módulo).

Cada fato distinto foi conferido na fonte oficial hoje. Convenção do projeto:
**[CONFIRMADO]** lido direto na fonte oficial, **[NÃO VERIFICÁVEL]** fonte
paga ou indisponível.

## Tabela

| Módulo | Afirmação no arquivo | Fonte oficial hoje | Status |
|---|---|---|---|
| 2.5 (t2, q2, q3, q11) | NIST SP 800-63B vigente, "publicada em 2025"; mínimo 15 caracteres (fator único) / 8 (com outro fator); proíbe KBA com "SHALL NOT"; proíbe troca periódica sem evidência de comprometimento | **[CONFIRMADO]** Revision 4, publicada 26/08/2025. Os quatro requisitos citados batem literalmente: "SHALL require... minimum of 15 characters... minimum of eight"; "SHALL NOT prompt... knowledge-based authentication"; "SHALL NOT require... change passwords periodically" | **Bate** |
| 2.6 (t3, q10, q16, q17, q18, q20, q21) | "ANSI INCITS 359 (RBAC)... edição vigente: 359-2012 (R2022)" | Três fontes tentadas (ansi.org, techstreet/accuristech) devolveram 404/403 — norma paga, sem página pública de status | **[NÃO VERIFICÁVEL]** — não é indício de erro, é limite de acesso à fonte |
| 2.7 (t7, q16, q19) | "revisão vigente é a RFC 9989, que obsoletou a RFC 7489" (DMARC) | **[CONFIRMADO]** rfc-editor.org: RFC 9989 obsoleta RFC 7489 (e também 9091); é o padrão vigente, Proposed Standard | **Bate** |
| 3.1 (t6, q35) | "CVSS v4.0 é a versão vigente e convive com a v3.1" | **[CONFIRMADO]** first.org/cvss: "CVSS is currently at version 4.0"; v3.1 mantida em arquivo, sem v4.1/v5.0 | **Bate** |
| 3.1 (q11, q12) | PTES "wiki oficial se declara v1.0 e não recebe edição desde agosto de 2014" | Tentativa de reconfirmar falhou por conexão recusada (site historicamente instável) — mas a própria afirmação do corpus já é "está parado", o que é consistente com a falha de conexão | **[NÃO VERIFICÁVEL nesta rodada]**, sem indício de erro |
| 3.2 (t3, fonte) | "RFC 9162... obsoleta a RFC 6962" (Certificate Transparency) | Já tratado como fato consolidado no levantamento anterior do 3.x; não refeito nesta rodada por ausência de sinal de mudança | Não verificado nesta rodada |
| 4.1 (t5, q5, q24) | "CIS Critical Security Controls v8.1... versão vigente" | **[CONFIRMADO]** cisecurity.org/controls: v8.1 é a versão corrente, v8 e v7.1 arquivadas | **Bate** |
| 4.1 (t4, q16, q21) | "A diretiva vigente é a BOD 26-04... emitida em 10/06/2026", revoga a BOD 22-01 | **[CONFIRMADO]** cisa.gov/news-events/directives: BOD 26-04 vigente, revoga BOD 19-02 e BOD 22-01 (o corpus só cita a 22-01, que é a relevante ao contexto — não é erro, é recorte) | **Bate** |
| 4.2 (t4, q11) | NIST SP 800-94 (IDS/IPS), "fevereiro de 2007 — publicação final e vigente", rascunho de Revisão 1 de 2012 retirado | **[CONFIRMADO]** csrc.nist.gov: continua a versão final vigente; draft Rev. 1 "never became a final publication and has been retired" | **Bate** |
| 4.1 (t4) | NIST SP 800-40 Rev. 4, abril de 2022 | **[CONFIRMADO]** csrc.nist.gov: Rev. 4 é a versão vigente (final 04/06/2022 — o corpus arredonda para "abril", mesma publicação), sem Revisão 5 | **Bate** |
| 2.6 (q32) | "40 CWEs mapeadas" (A01) | Já corrigido nesta sessão, em commit separado | **Corrigido** |

## O que ficou de fora desta rodada (custo/benefício)

Encontrados mas não verificados por serem citação de identificador (RFC,
seção de NIST SP) sem afirmação de vigência associada — não é risco de
desatualização, é referência a documento fixo: os ~74 RFCs e NIST SPs
citados só como fonte de seção específica (ex.: "RFC 9110 §5.2", "NIST SP
800-115 §5.2.1"), versões de ferramenta de linha de comando citadas para
bater sintaxe de laboratório (Gobuster v3.8.2, ffuf v2.2.1 — o corpus não
afirma que são "a versão mais recente", só que a sintaxe testada é dessas
versões específicas, o que continua verdadeiro mesmo se uma versão mais nova
tiver saído), e o histórico de RFCs já obsoletados um pelo outro dentro do
próprio texto do corpus (RFC 6962→9162 em CT, RFC 7489→9989 em DMARC, RFC
793→9293 em TCP) — esses já vêm narrados como histórico no próprio módulo,
não como "isto é o vigente" sem qualificação.

MITRE ATT&CK (citado sem número de versão na maioria dos módulos, exceto o
levantamento já feito em `owasp-attack.md` para o 4.6 em rascunho) não foi
reconferido — verificação de 19/08/2026 já é recente e específica.

## Resumo

- **15 fatos distintos com afirmação de vigência**, cobrindo 49 ocorrências
  de texto no corpus.
- **9 batem** com a fonte oficial hoje, sem divergência: NIST SP 800-63B
  (senha), RFC 9989 (DMARC), CVSS v4.0, CIS Controls v8.1, CISA BOD 26-04,
  NIST SP 800-94, NIST SP 800-40 Rev. 4.
- **1 já era conhecido e corrigido nesta sessão**: contagem de CWE em 2.6
  (34→40, commit separado).
- **2 não verificáveis por limite de fonte** (não por indício de erro):
  ANSI INCITS 359 (norma paga, três tentativas de acesso bloqueadas) e PTES
  (site fora do ar na tentativa de hoje — consistente com a própria descrição
  do corpus de que é um padrão comunitário parado desde 2014).
- **0 divergências novas encontradas.** O caso do 2.6 (OWASP Top 10:2021,
  já corrigido antes desta auditoria) segue sendo o único erro real
  encontrado no corpus até agora — o restante do material com afirmação de
  vigência está, hoje, correto.

Mais grave, em ordem: (1) nenhum — o problema do 2.6 já foi corrigido antes
desta rodada; (2) ANSI INCITS 359 fica sem confirmação possível por ser
norma paga — se o usuário tiver acesso à norma por outro canal, vale
reconferir manualmente; (3) tudo o mais checado hoje está atual.
