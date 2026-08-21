# OWASP + MITRE ATT&CK — estado das listas de referência (verificação independente, 19/08/2026)

Convenção: **[CONFIRMADO]** = lido diretamente na página oficial citada.
**[CONSOLIDADO]** = não consta na fonte oficial; vem de fontes secundárias cruzadas.

---

## 1. OWASP Top 10 — versão vigente

**A versão vigente é a OWASP Top 10:2025. CONFIRMADO de forma independente.**

- [CONFIRMADO] A página do projeto afirma literalmente: "The most current released
  version is the OWASP Top Ten 2025."
  https://owasp.org/www-project-top-ten/
- [CONFIRMADO] O repositório oficial do documento afirma: "We have released the
  OWASP Top 10:2025 (Final)" — ou seja, é versão final, não release candidate.
  https://github.com/OWASP/Top10
- [CONFIRMADO] `https://owasp.org/Top10/` redireciona para `OWASP Top 10:2025`.
- [CONFIRMADO] As dez categorias de 2025, como listadas na fonte
  (https://owasp.org/Top10/2025/), batem exatamente com o arquivo
  `owasp-versao-VERIFICADA.md` do fio principal. Nenhuma divergência.

| Id | Categoria (2025) |
|---|---|
| A01:2025 | Broken Access Control |
| A02:2025 | Security Misconfiguration |
| A03:2025 | Software Supply Chain Failures |
| A04:2025 | Cryptographic Failures |
| A05:2025 | Injection |
| A06:2025 | Insecure Design |
| A07:2025 | Authentication Failures |
| A08:2025 | Software or Data Integrity Failures |
| A09:2025 | Security Logging and Alerting Failures |
| A10:2025 | Mishandling of Exceptional Conditions |

Lista de 2021, para comparação:

| Id | Categoria (2021) |
|---|---|
| A01:2021 | Broken Access Control |
| A02:2021 | Cryptographic Failures |
| A03:2021 | Injection |
| A04:2021 | Insecure Design |
| A05:2021 | Security Misconfiguration |
| A06:2021 | Vulnerable and Outdated Components |
| A07:2021 | Identification and Authentication Failures |
| A08:2021 | Software and Data Integrity Failures |
| A09:2021 | Security Logging and Monitoring Failures |
| A10:2021 | Server Side Request Forgery (SSRF) |

[CONFIRMADO] https://owasp.org/Top10/2021/

---

## 2. O que mudou de 2021 para 2025

Fonte primária: https://owasp.org/Top10/2025/0x00_2025-Introduction/

[CONFIRMADO] A introdução diz: **"There are two new categories and one consolidation
in the Top Ten for 2025."**

### Categorias novas (2)

- [CONFIRMADO] **A03:2025 — Software Supply Chain Failures.** Expande
  A06:2021-Vulnerable and Outdated Components para cobrir toda a cadeia de
  suprimentos: dependências, sistemas de build e infraestrutura de distribuição.
  Não é só "componente desatualizado" mais.
- [CONFIRMADO] **A10:2025 — Mishandling of Exceptional Conditions.** Categoria
  inteiramente nova, sem antecessora em 2021. Cobre tratamento indevido de erros,
  erros de lógica e cenários de *fail-open*.

### Consolidação (1)

- [CONFIRMADO] **A10:2021 — Server-Side Request Forgery (SSRF) deixou de existir
  como categoria própria e foi absorvida em A01:2025 — Broken Access Control.**
- [CONSOLIDADO] Justificativa divulgada: boa parte dos casos de SSRF é, no fundo,
  falha de controle de acesso. https://www.fastly.com/blog/new-2025-owasp-top-10-list-what-changed-what-you-need-to-know

### Renomeadas (2)

- [CONFIRMADO] A07: "Identification and Authentication Failures" (2021) →
  **"Authentication Failures"** (2025). Mesma posição, nome encurtado.
- [CONFIRMADO] A09: "Security Logging and Monitoring Failures" (2021) →
  **"Security Logging and Alerting Failures"** (2025). Mesma posição;
  *Monitoring* virou *Alerting*.
- [CONFIRMADO] Detalhe fácil de errar: A08 mudou de "Software **and** Data
  Integrity Failures" (2021) para "Software **or** Data Integrity Failures"
  (2025). Conjunção diferente, mesma posição.

### Quem subiu e quem desceu

| Categoria | 2021 | 2025 | Movimento |
|---|---|---|---|
| Broken Access Control | A01 | A01 | manteve o topo |
| Security Misconfiguration | A05 | A02 | **subiu 3 posições** |
| Cryptographic Failures | A02 | A04 | desceu 2 |
| Injection | A03 | A05 | desceu 2 |
| Insecure Design | A04 | A06 | desceu 2 |
| Authentication Failures | A07 | A07 | estável (renomeada) |
| Software or Data Integrity Failures | A08 | A08 | estável |
| Security Logging and Alerting Failures | A09 | A09 | estável (renomeada) |
| Vulnerable and Outdated Components | A06 | — | absorvida/expandida em A03:2025 |
| SSRF | A10 | — | consolidada em A01:2025 |

[CONFIRMADO] Todos os movimentos acima constam da introdução oficial de 2025.

### Números da base de dados de 2025

- [CONFIRMADO] 248 CWEs mapeadas nas 10 categorias (de 968 CWEs no dicionário do
  MITRE). Em 2021 eram 218.
- [CONFIRMADO] Mais de 2,8 milhões de aplicações analisadas, de 13 organizações
  nomeadas mais doadores anônimos.
- [CONFIRMADO] Cerca de 175 mil registros de CVE analisados, contra ~125 mil em 2021.

---

## 3. Data de publicação do Top 10:2025

**Não existe data oficial de publicação divulgada nas páginas do OWASP.**

- [CONFIRMADO] Nenhuma das páginas oficiais lidas
  (`www-project-top-ten`, `Top10/2025/`, `Top10/2025/0x00_2025-Introduction/`,
  `github.com/OWASP/Top10`) traz dia/mês de publicação. A única marca temporal na
  introdução é a linha de copyright "© Copyright 2021-2025".
- [CONFIRMADO] O repositório GitHub do OWASP/Top10 **não tem nenhuma release nem
  tag publicada** ("There aren't any releases here"), então não há data por ali.
- [CONFIRMADO] O site suplementar oficial (owasptopten.org, mantido pelo core team
  do projeto) anunciava: a Top 10:2025 "will be announced at the OWASP Global
  AppSec Conf in DC the first week of Nov 2025".
- [CONSOLIDADO] O *release candidate* foi apresentado em **6 de novembro de 2025**,
  na Global AppSec Conference em Washington, DC.
  https://www.fastly.com/blog/new-2025-owasp-top-10-list-what-changed-what-you-need-to-know
- [CONSOLIDADO] A versão **final** teria saído em **janeiro de 2026**. Fontes
  secundárias convergem nisso, mas nenhuma fonte OWASP confirma dia exato.
  https://about.gitlab.com/blog/2025-owasp-top-10-whats-changed-and-why-it-matters/

**Regra de escrita: citar "OWASP Top 10:2025", sem dia.** Se for preciso datar,
usar "release candidate em novembro de 2025, versão final em janeiro de 2026",
marcado como consolidado, nunca como dado oficial.

---

## 4. OWASP Web Security Testing Guide (WSTG)

- [CONFIRMADO] **Versão estável vigente: WSTG v4.2, lançada em 3 de dezembro de 2020.**
  A página do projeto diz: "Version 4.2 introduces new testing scenarios, updates
  existing chapters, and offers an improved writing style and chapter layout."
  https://owasp.org/www-project-web-security-testing-guide/
- [CONFIRMADO] A **v5.0 está em desenvolvimento**, não lançada: "We are currently
  developing release version 5.0." Existe também uma v4.3 não lançada na página de
  releases.
- [CONFIRMADO] A URL `.../www-project-web-security-testing-guide/latest/` serve
  conteúdo de trabalho ("may frequently change"), **não** é uma versão numerada.
  Não citar "latest" como se fosse versão.

**Armadilha de idade:** o WSTG estável é de 2020. É a referência mais antiga deste
conjunto — quase seis anos. Não escrever "guia atualizado" sem qualificar.

---

## 5. OWASP ASVS

- [CONFIRMADO] **Versão vigente: ASVS 5.0.0, lançada em 30 de maio de 2025**, no
  Global AppSec EU Barcelona. A página do projeto anuncia: "ASVS Version 5.0.0 is
  released LIVE at Global AppSec EU Barcelona 2025!"
  https://owasp.org/www-project-application-security-verification-standard/
- [CONFIRMADO] Histórico de releases no GitHub: 5.0.0 (30/05/2025), 4.0.3
  (28/10/2024), 4.0.2 (28/10/2024), 4.0.1 (03/03/2021).
  https://github.com/OWASP/ASVS/releases
- [CONFIRMADO] Existe uma tag `latest` ("Bleeding Edge", recompilada
  automaticamente do master — a última recompilação vista é de 28/07/2026).
  **Não é versão.** O próprio projeto avisa que ela "cannot be relied upon for
  stability" e recomenda a 5.0.0 estável.
- [CONFIRMADO] A 5.0.0 traz mapeamento de/para a 4.0.3, útil para quem migra.

---

## 6. MITRE ATT&CK — versão da matriz Enterprise

- [CONFIRMADO] A versão exibida no site é **ATT&CK v19.2** (rodapé de
  https://attack.mitre.org/tactics/TA0043/).
- [CONFIRMADO] A release base **v19 saiu em 28 de abril de 2026**
  (https://attack.mitre.org/resources/updates/updates-april-2026/ — "Start Date:
  April 28, 2026").
- [CONFIRMADO] A **v19.2 saiu em 6 de agosto de 2026**
  (https://attack.mitre.org/resources/updates/updates-august-2026/). É a primeira
  "Agile release" do ATT&CK: um ciclo de escopo estreito entre as releases
  semestrais, publicando atualizações pontuais de grupos, software e campanhas.
  A v19.2 acrescentou ShinyHunters (G1057), TeamPCP (G1056) e Kali365 (S9044).
- [CONFIRMADO] Versão anterior: **v18.1, vigente de 28/10/2025 a 27/04/2026**
  (https://attack.mitre.org/resources/versions/).
- [CONSOLIDADO] Não localizei página de update própria para uma v19.1. O histórico
  de versões lista a faixa como v19 (28/04/2026 – atual), com a v19.x correndo por
  dentro. **Forma segura de citar: "ATT&CK v19 (28 de abril de 2026), atualizada
  para v19.2 em 6 de agosto de 2026".**

---

## 7. Tática Reconnaissance (TA0043)

[CONFIRMADO] https://attack.mitre.org/tactics/TA0043/

Descrição oficial: *"The adversary is trying to gather information they can use to
plan future operations."* Envolve coleta ativa ou passiva de informação sobre a
organização-alvo, sua infraestrutura e seu pessoal, para apoiar o direcionamento
do ataque.

### As 12 técnicas de TA0043 (v19.2)

| ID | Técnica | Sub-técnicas |
|---|---|---|
| T1595 | Active Scanning | .001 Scanning IP Blocks; .002 Vulnerability Scanning; .003 Wordlist Scanning |
| T1592 | Gather Victim Host Information | .001 Hardware; .002 Software; .003 Firmware; .004 Client Configurations |
| T1589 | Gather Victim Identity Information | .001 Credentials; .002 Email Addresses; .003 Employee Names |
| T1590 | Gather Victim Network Information | .001 Domain Properties; .002 DNS; .003 Network Trust Dependencies; .004 Network Topology; .005 IP Addresses; .006 Network Security Appliances |
| T1591 | Gather Victim Org Information | .001 Determine Physical Locations; .002 Business Relationships; .003 Identify Business Tempo; .004 Identify Roles |
| T1598 | Phishing for Information | .001 Spearphishing Service; .002 Spearphishing Attachment; .003 Spearphishing Link; .004 Spearphishing Voice |
| T1682 | Query Public AI Services | — |
| T1597 | Search Closed Sources | .001 Threat Intel Vendors; .002 Purchase Technical Data |
| T1596 | Search Open Technical Databases | .001 DNS/Passive DNS; .002 WHOIS; .003 Digital Certificates; .004 CDNs; .005 Scan Databases |
| T1593 | Search Open Websites/Domains | .001 Social Media; .002 Search Engines; .003 Code Repositories |
| T1681 | Search Threat Vendor Data | — |
| T1594 | Search Victim-Owned Websites | — |

[CONFIRMADO] São **12 técnicas**, não as 10 de listas antigas. **T1681 (Search
Threat Vendor Data)** e **T1682 (Query Public AI Services)** são adições recentes;
material anterior a 2025 não as menciona.

### O que distingue Reconnaissance (TA0043) de Resource Development (TA0042)

[CONFIRMADO] https://attack.mitre.org/tactics/TA0042/

Descrição oficial de TA0042: *"The adversary is trying to establish resources they
can use to support operations."*

A distinção é **o objeto do verbo**:

- **TA0043 Reconnaissance — coletar informação SOBRE a vítima.** O alvo é
  conhecimento: quem é a organização, que hosts e redes tem, quem trabalha lá.
  Nada é construído; o adversário lê.
- **TA0042 Resource Development — criar, comprar ou comprometer RECURSOS DO PRÓPRIO
  ADVERSÁRIO.** O alvo é capacidade: infraestrutura, contas, ferramentas, malware,
  domínios de staging. Nada é aprendido sobre a vítima; o adversário monta o
  arsenal.

Ambas são **pré-comprometimento** (acontecem antes de tocar no ambiente da vítima
em si), e é aí que a confusão nasce. O teste rápido: *a ação produz informação
sobre a vítima ou produz um ativo controlado pelo atacante?*

Técnicas de TA0042, para contraste [CONFIRMADO]:
T1650 Acquire Access · T1583 Acquire Infrastructure · T1586 Compromise Accounts ·
T1584 Compromise Infrastructure · T1587 Develop Capabilities · T1585 Establish
Accounts · T1683 Generate Content · T1588 Obtain Capabilities · T1608 Stage
Capabilities.

Caso-limite útil: comprar dados técnicos de um broker é **T1597.002 Purchase
Technical Data (Reconnaissance)** — o que se compra é informação sobre a vítima.
Comprar acesso já existente a uma rede é **T1650 Acquire Access (Resource
Development)** — o que se compra é um ativo operacional.

---

## 8. Técnicas pedidas, com ids

### T1595 — Active Scanning

[CONFIRMADO] https://attack.mitre.org/techniques/T1595/

Descrição: *"Adversaries may execute active reconnaissance scans to gather
information that can be used during targeting. Active scans are those where the
adversary probes victim infrastructure via network traffic, as opposed to other
forms of reconnaissance that do not involve direct interaction."*

- Tática: Reconnaissance (TA0043)
- Version da técnica: 1.0 · Created: 02/10/2020 · Last Modified: 24/10/2025

| ID | Sub-técnica |
|---|---|
| T1595.001 | Scanning IP Blocks |
| T1595.002 | Vulnerability Scanning |
| T1595.003 | Wordlist Scanning |

O diferencial de T1595 é **interação direta com a infraestrutura da vítima via
tráfego de rede**. Reconhecimento que não toca no alvo cai em T1596 (Search Open
Technical Databases), T1593 (Search Open Websites/Domains) etc.

### T1592 — Gather Victim Host Information

[CONFIRMADO] https://attack.mitre.org/techniques/T1592/

Descrição: *"Adversaries may gather information about the victim's hosts that can
be used during targeting. Information about hosts may include a variety of
details, including administrative data (ex: name, assigned IP, functionality,
etc.) as well as specifics regarding its configuration (ex: operating system,
language, etc.)."*

| ID | Sub-técnica |
|---|---|
| T1592.001 | Hardware |
| T1592.002 | Software |
| T1592.003 | Firmware |
| T1592.004 | Client Configurations |

### T1590 — Gather Victim Network Information

[CONFIRMADO] https://attack.mitre.org/techniques/T1590/

Descrição: *"Adversaries may gather information about the victim's networks that
can be used during targeting. Information about networks may include a variety of
details, including administrative data (ex: IP ranges, domain names, etc.) as well
as specifics regarding its topology and operations."*

| ID | Sub-técnica |
|---|---|
| T1590.001 | Domain Properties |
| T1590.002 | DNS |
| T1590.003 | Network Trust Dependencies |
| T1590.004 | Network Topology |
| T1590.005 | IP Addresses |
| T1590.006 | Network Security Appliances |

[CONFIRMADO] Ponto importante: **T1592 (Host) e T1590 (Network) são técnicas
distintas com ids distintos.** Não existe uma técnica única chamada "Gather Victim
Host/Network Information". Se um enunciado pedir "a técnica de coleta de informação
de host/rede", a resposta correta são duas técnicas, não uma.

---

## ARMADILHAS

1. **Escrever que o Top 10 de 2021 é o vigente.** É o erro mais provável: material
   de treinamento, blogs e memória de modelo anterior a 2026 ainda dizem 2021.
   Vigente é **OWASP Top 10:2025**, final, confirmado em duas fontes OWASP.
   Sempre escrever a versão colada no nome: "OWASP Top 10:2025".

2. **Chutar data de publicação do Top 10:2025.** Não existe data oficial em
   nenhuma página do OWASP, e o GitHub do projeto não tem release nem tag. As
   datas que circulam (06/11/2025 para o RC, janeiro de 2026 para o final) são
   **consolidadas de fontes secundárias**. Se entrar em questão de prova, usar só
   "2025" ou marcar explicitamente como consolidado.

3. **Dizer que Injection caiu porque virou menos comum.** Injection desceu de A03
   para A05 em posição relativa; o documento não afirma queda de prevalência
   absoluta. Ordem no Top 10 é ranking relativo com metodologia própria, não
   medida de risco absoluto.

4. **Tratar A03:2025 como simples renomeação de A06:2021.** Software Supply Chain
   Failures é categoria **nova e mais ampla**: cobre dependências, sistemas de
   build e infraestrutura de distribuição, não só "componente desatualizado".
   A introdução oficial conta duas categorias novas, e essa é uma delas.

5. **Procurar SSRF como categoria própria em 2025.** Sumiu; foi consolidada em
   A01:2025 Broken Access Control. Questão que peça "a categoria de SSRF no Top 10
   vigente" tem resposta A01, não A10.

6. **Confundir "and" com "or" em A08 e "Monitoring" com "Alerting" em A09.** Os
   nomes mudaram por uma palavra. Copiar o nome de 2021 dentro de um texto sobre
   2025 é erro silencioso e difícil de pegar na revisão.

7. **Assumir que o WSTG acompanhou o Top 10.** O WSTG estável continua na **v4.2
   de dezembro de 2020**. A v5.0 está em desenvolvimento, não lançada. Nunca citar
   "WSTG v5" como existente, nem citar a URL `/latest/` como se fosse versão
   numerada — é conteúdo de trabalho, muda a qualquer momento.

8. **Citar o ASVS "bleeding edge" como versão.** A tag `latest` no GitHub é
   recompilada do master automaticamente e o próprio projeto diz que não serve para
   uso estável. A versão a citar é **ASVS 5.0.0, de 30/05/2025**.

9. **Usar a lista antiga de 10 técnicas em Reconnaissance.** TA0043 tem **12**
   técnicas na v19.2. **T1681 (Search Threat Vendor Data)** e **T1682 (Query Public
   AI Services)** são recentes; qualquer contagem de 10 vem de material velho.

10. **Escrever a versão do ATT&CK sem checar.** Vigente é **v19**, base de
    28/04/2026, com o site exibindo **v19.2** desde 06/08/2026 (primeira "Agile
    release"). A anterior foi v18.1 (28/10/2025 a 27/04/2026). Não localizei página
    de update dedicada a uma v19.1 — não inventar uma.

11. **Colapsar TA0043 e TA0042 em "fase de preparação".** As duas são
    pré-comprometimento, mas o objeto difere: Reconnaissance coleta **informação
    sobre a vítima**; Resource Development monta **recursos do atacante**. Teste
    rápido: a ação gerou conhecimento sobre o alvo ou um ativo controlado pelo
    atacante?

12. **Inventar uma técnica "Gather Victim Host/Network Information".** São duas:
    **T1592** (Host) e **T1590** (Network). Ids diferentes, sub-técnicas diferentes.

13. **Chamar de Active Scanning qualquer reconhecimento.** T1595 exige **interação
    direta com a infraestrutura da vítima via tráfego de rede**. Consulta a
    Shodan/Censys é T1596.005 (Scan Databases), não T1595 — quem escaneou foi outro.
