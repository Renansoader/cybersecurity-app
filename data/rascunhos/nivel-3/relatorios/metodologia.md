# Metodologia de teste de intrusao — pesquisa com fontes

Data da pesquisa: 2026-08-19.
Convencao de marcacao:
- **[CONFIRMADO]** = li a fonte primaria nesta sessao (URL abaixo da afirmacao) e o texto esta la.
- **[CONSOLIDADO]** = consenso de mercado / conhecimento estabelecido, sem verificacao direta na fonte primaria nesta sessao.

Falhas de carregamento registradas:
- `https://pentest-standard.org` e `https://www.pentest-standard.org` **nao carregam por HTTPS** (conexao recusada na porta 443; `WebFetch` falhou com `ECONNREFUSED 96.126.116.56:443`). O site **responde por HTTP na porta 80** (HTTP 200 em `http://www.pentest-standard.org/index.php/Main_Page`), e foi por ai que confirmei o conteudo. Ou seja: o padrao oficial hoje vive num wiki sem TLS.
- `https://web.archive.org/...` — bloqueado para a ferramenta de fetch (nao consegui usar o Internet Archive).
- `https://app.readthedocs.org/projects/pentest-standard/` — HTTP 403 (nao deu para ver historico de builds).
- `https://www.cisa.gov/...` — 403 via WebFetch; recuperado via `curl` com User-Agent normal (conteudo abaixo confirmado assim).
- O PDF do NIST SP 800-115 nao foi legivel pelo fetch (fluxo binario); foi baixado e convertido localmente com `pdftotext` — todas as citacoes do 800-115 abaixo saem desse texto extraido do PDF oficial do NVL/NIST.

---

## 1. PTES — Penetration Testing Execution Standard

### As sete secoes, na ordem oficial

[CONFIRMADO] O wiki oficial diz: "The penetration testing execution standard consists of seven (7) main sections", e lista, nesta ordem:

1. **Pre-engagement Interactions** — escopo, questionarios, datas de inicio/fim, faixas de IP e dominios, terceiros (cloud/ISP/MSSP), pretextos de engenharia social aceitos, teste de DoS sim/nao, pagamento, metas primarias e secundarias, linhas de comunicacao, contatos de emergencia e as Rules of Engagement (timeline, locais, manuseio de evidencia, reunioes de status, horario do teste, tratamento de shunning/bloqueio, permissao para testar, questoes legais).
2. **Intelligence Gathering** — coleta passiva/ativa, inteligencia corporativa e de pessoal; o wiki tem "niveis" de intensidade aqui.
3. **Threat Modeling** — modelagem de ativos de negocio, processos, agentes de ameaca e suas capacidades.
4. **Vulnerability Analysis** — identificacao das vulnerabilidades **potenciais** e sua classificacao.
5. **Exploitation** — confirmacao pratica: explorar para provar que a vulnerabilidade existe e ganhar o acesso definido.
6. **Post Exploitation** — valor do alvo comprometido, pivoteamento, persistencia, exfiltracao simulada, impacto de negocio.
7. **Reporting** — sumario executivo + relatorio tecnico (detalhe na secao 5 deste documento).
   Fonte: http://www.pentest-standard.org/index.php/Main_Page (so por HTTP) e http://www.pentest-standard.org/index.php/Pre-engagement

[CONFIRMADO] O PTES separa o "padrao" do "como fazer": "As the standard does not provide any technical guidelines as far as how to execute an actual pentest, we have also created a technical guide to accompany the standard itself" (PTES Technical Guidelines e documento separado).
Fonte: http://www.pentest-standard.org/index.php/Main_Page

### Estado do padrao hoje (2026)

[CONFIRMADO] A pagina principal do wiki tem no rodape: **"This page was last edited on 16 August 2014, at 20:14."** A pagina Pre-engagement: **"This page was last edited on 16 August 2014, at 18:13."**
Fontes: http://www.pentest-standard.org/index.php/Main_Page e http://www.pentest-standard.org/index.php/Pre-engagement

[CONFIRMADO] O proprio texto se declara **v1.0** e promete uma v2.0 que nunca saiu: "This version can be considered a v1.0 ... A v2.0 is in the works soon, and will provide more granular work in terms of 'levels'".
Fonte: http://www.pentest-standard.org/index.php/Main_Page

[CONFIRMADO] `Special:RecentChanges` do wiki (consultado em 19/08/2026) retorna **"No changes during the given period match these criteria"** — nenhuma edicao no periodo consultavel.
Fonte: http://www.pentest-standard.org/index.php?title=Special:RecentChanges

[CONFIRMADO] Existe um espelho em Read the Docs com as mesmas sete secoes e o mesmo texto de "v1.0", tambem sem data de revisao.
Fonte: https://pentest-standard.readthedocs.io/en/latest/

**Leitura honesta:** o PTES e **um padrao congelado desde 2014**, util como vocabulario e como checklist de escopo/relatorio, mas nao e um padrao vivo. Nao ha organismo mantenedor publicando revisoes. [CONSOLIDADO — inferencia a partir dos fatos confirmados acima]

---

## 2. NIST SP 800-115 — Technical Guide to Information Security Testing and Assessment

### Identidade e idade do documento

[CONFIRMADO] Titulo completo: *Technical Guide to Information Security Testing and Assessment*; autores Karen Scarfone, Murugiah Souppaya (NIST), Amanda Cody, Angela Orebaugh (BAH); **publicado em setembro de 2008 (status "Final", 30/09/2008)**; superseded o SP 800-42. Nao ha indicacao de revisao em andamento na pagina do CSRC.
Fonte: https://csrc.nist.gov/pubs/sp/800/115/final

**Idade: o documento tem ~18 anos em 2026.** Isso importa: ele nao cobre nuvem, contêineres, CI/CD, identidade federada, mobile moderno nem IA. O que envelheceu bem e a parte de **processo** (planejamento, ROE, manuseio de dados, pos-teste); o que envelheceu mal e a parte de **tecnica** (ferramentas, tipos de falha, "Live CDs" no Apendice A). [CONSOLIDADO]

### As quatro fases

[CONFIRMADO] Secao 5.2.1, "Figure 5-1. Four-Stage Penetration Testing Methodology": **Planning → Discovery → Attack → Reporting**, com laco de realimentacao ("Additional Discovery") do Attack de volta para o Discovery.

- **Planning**: "rules are identified, management approval is finalized and documented, and testing goals are set. ... **No actual testing occurs in this phase.**"
- **Discovery**: duas partes — (a) coleta de informacao e varredura (identificacao de portas/servicos, DNS/WHOIS, sniffing em teste interno, enumeracao, banner grabbing, ate dumpster diving); (b) **analise de vulnerabilidade**, comparando servicos/SO com bases de vulnerabilidade (ex.: NVD) e com o conhecimento do testador.
- **Attack**: "the process of verifying previously identified potential vulnerabilities by attempting to exploit them"; exploracao pode levar a escalada de privilegio e a novo Discovery (o laco). O guia lista as categorias classicas: misconfigurations, kernel flaws, buffer overflows, insufficient input validation, symbolic links, file descriptor attacks, race conditions, incorrect file/directory permissions.
- **Reporting**: "occurs simultaneously with the other three phases" — na Planning nasce o plano/ROE; em Discovery e Attack ha logs e relatorios periodicos; ao final, um relatorio que "describe identified vulnerabilities, present a risk rating, and give guidance on how to mitigate".
  Fonte: https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-115.pdf (secao 5.2.1)

[CONFIRMADO] Nota de rodape 18 do proprio NIST: **"This is an example of how the penetration process can be divided into phases. There are many acceptable ways of grouping the actions involved in performing penetration testing."** — ou seja, o proprio NIST diz que quatro fases nao e dogma.
Fonte: mesmo PDF, nota 18.

### Frase que separa varredura de pentest

[CONFIRMADO] "While vulnerability scanners check only for the **possible existence** of a vulnerability, the attack phase of a penetration test **exploits the vulnerability to confirm its existence**."
Fonte: mesmo PDF, secao 5.2.1.

### O que a norma diz sobre Rules of Engagement (ROE)

[CONFIRMADO] O ROE tem um template proprio no **Apendice B**, com esta estrutura:
1. Introducao — 1.1 Proposito (quem e testado, quem testa, por que), 1.2 **Escopo** ("test boundaries in terms of actions and expected outcomes"), 1.3 Premissas e limitacoes, 1.4 **Riscos** ("Inherent risks exist ... particularly in the case of intrusive tests" + mitigacoes), 1.5 Estrutura do documento.
2. Logistica — 2.1 **Pessoal** (nomes de todos os testadores e dos contatos do cliente, incluindo tabela com pontos de contato do time de teste, da gerencia e do **time de resposta a incidentes**; clearances se aplicavel), 2.2 **Cronograma de teste** ("hours during which the testing will take place — for example, it may be prudent to conduct technical testing of an operational site during evening hours rather than during peak business periods"), 2.3 Local do teste (acesso fisico, cracha, escolta, areas proibidas), 2.4 Equipamento e **ferramentas autorizadas**, incluindo como distinguir as maquinas do testador das do cliente (ex.: por MAC).
3. Estrategia de comunicacao — 3.1 Comunicacao geral (frequencia, reunioes), 3.2 **Incident Handling and Response**: "Criteria for **halting** the information security testing should be provided" + curso de acao se o teste degradar a rede **ou se um adversario real atacar durante o teste** + a arvore de chamadas/cadeia de comando do IR em formato de consulta rapida + **processo para retomar o teste**.
4. Sistema/rede alvo — IPs autorizados e **nao** autorizados; "It is also crucial to identify any system not authorized for testing — this is referred to as the **'exclude list'**".
5. Execucao — atividades permitidas e proibidas; 5.1 componentes nao tecnicos (incluindo, para teste fisico, **um formulario assinado e com contatos para o testador mostrar a policia ou a seguranca do predio**); 5.2 componentes tecnicos (se pode instalar/criar/modificar/executar arquivos e o que fazer com eles no fim); 5.3 **Data Handling** (coleta, armazenamento, transmissao e destruicao dos dados de teste, com requisitos "detailed, unambiguous").
6. Reporting — o que cada relatorio traz no minimo e com que frequencia (ex.: status diario), template como anexo.
7. **Signature Page** — "At a minimum, the **test team leader** and the organization's **senior management (CSO, CISO, CIO, etc.)** should sign the ROE stating that they understand the test's scope and boundaries."
   Fonte: https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-115.pdf (Apendice B)

[CONFIRMADO] Criterio de parada tambem aparece no corpo: "penetration testing can be designed to **stop when the tester reaches a point when an additional action will cause damage**"; e no teste coberto: "Covert testing usually has defined boundaries, such as stopping testing when a certain level of access is achieved or a certain type of damage is achievable as a next step in testing. Having such boundaries prevents damage while still showing that the damage could occur."
Fonte: mesmo PDF, secoes 5.2.2 e 2.4.2.

[CONFIRMADO] Dado sensivel e manuseio (secao 7.4): "Because this data is sensitive, it is important to handle it appropriately"; os assessors devem manter **log passo a passo das proprias acoes** — "This provides an audit trail, and allows the organization to **distinguish between the actions of assessors and true adversaries**" — com, no minimo, data/hora, nome do assessor, IP/MAC da maquina de teste, IP/MAC do alvo, ferramenta, comando executado e comentarios. Armazenamento seguro e responsabilidade do assessor: "Inappropriate release of this information can damage the organization's reputation and increase the likelihood of exploitation". O guia trata explicitamente de coleta, armazenamento, transmissao e **destruicao** dos dados (7.4.1–7.4.4).
Fonte: mesmo PDF, secao 7.4.

[CONFIRMADO] Ha secao propria de **Legal Considerations** (6.6) e de planejamento (6. Security Assessment Planning: politica, priorizacao, selecao de tecnicas, logistica, plano, questoes legais) e de execucao (7. Coordination / Assessing / Analysis / Data Handling) e pos-teste (8. Mitigation Recommendations / Reporting / Remediation).
Fonte: sumario do mesmo PDF.

---

## 3. OSSTMM e OWASP WSTG

### OSSTMM (ISECOM)

[CONFIRMADO] Versao vigente: **OSSTMM 3.02**. O proprio manual diz: "The current version of the Open Source Security Testing Methodology Manual (OSSTMM) is **3.02**. ... The original version was published on Monday, December 18, 2000. This current version is published on **Tuesday, December 14, 2010**."
Fonte: https://www.isecom.org/OSSTMM.3.pdf (secao "Version Information")

[CONFIRMADO] A pagina de pesquisa do ISECOM lista apenas o OSSTMM 3 como versao publicada, descrito como "a complete methodology for penetration and security testing, security analysis and the measurement of operational security". Nao ha OSSTMM 4 publicado la.
Fonte: https://www.isecom.org/research.html

[CONFIRMADO] O OSSTMM 3 unificou o teste em **cinco canais** — Human, Physical, Wireless, Telecommunications, Data Networks — e trocou a metrica antiga por **rav** (attack surface metric): "there is now a single security testing methodology for all channels"; "The new rav provides a factual attack surface metric".
Fonte: https://www.isecom.org/OSSTMM.3.pdf

[CONSOLIDADO] OSSTMM 4 aparece ha anos como rascunho/acesso para assinantes, sem lancamento publico. Trate o OSSTMM como **metodologia de auditoria operacional e de metrica (rav)**, nao como manual passo a passo de exploracao. Onde se encaixa: escopo amplo (fisico, humano, telecom, sem fio, redes), medicao repetivel e linguagem de "controles operacionais" — bom para auditoria e para comparar postura ao longo do tempo; fraco como guia tecnico de ataque moderno.

### OWASP Web Security Testing Guide (WSTG)

[CONFIRMADO] Versao estavel vigente: **v4.2**, publicada em **03/12/2020** (tag `v4.2`, `published_at: 2020-12-03T15:23:44Z`, `prerelease: false` na API do GitHub). A anterior, v4.1, e de 21/04/2020. Ha um `20230928-Prerelease` (28/09/2023) marcado como pre-release, feito para distribuir PDF/ePub entre a 4.2 e a 4.3.
Fontes: https://api.github.com/repos/OWASP/wstg/releases e https://github.com/OWASP/wstg/releases

[CONFIRMADO] A pagina do projeto confirma a v4.2 como estavel e a **v5.0 em desenvolvimento**, com conteudo "bleeding edge" no repositorio GitHub; o guia se define como "a comprehensive guide to testing the security of web applications and web services".
Fonte: https://owasp.org/www-project-web-security-testing-guide/

**Onde cada um se encaixa** [CONSOLIDADO]:
- **PTES** = espinha dorsal do **processo comercial** de um pentest (pre-engagement → relatorio). Bom para escopo, ROE e estrutura de relatorio.
- **NIST SP 800-115** = **processo de avaliacao** com peso normativo/regulatorio (governo dos EUA), forte em planejamento, ROE, manuseio de dados e pos-teste.
- **OSSTMM** = **metodologia de auditoria operacional multi-canal** com metrica (rav). Escopo alem de TI.
- **WSTG** = **catalogo tecnico de testes de aplicacao web** (o "o que testar e como", caso a caso, com IDs de teste WSTG-xxxx). Nao e um processo de engajamento — e a caixa de ferramentas dentro da fase de analise/exploracao.
- Combinacao comum na pratica: processo do PTES ou 800-115 + testes do WSTG (web) / OSSTMM (infra e nao tecnico) + pontuacao CVSS. [CONSOLIDADO]

---

## 4. Tipos de teste

### Caixa preta, cinza e branca

[CONFIRMADO] O NIST SP 800-115 define os termos no contexto de aplicacao (Apendice C): tecnicas **white box** "involve direct analysis of the application's source code"; **black box** operam sem esse conhecimento; "a combination of white box and black box techniques — this combination is known as **gray box testing**". O guia observa ainda: "Most assessments of custom applications are performed with white box techniques" e "White box techniques still tend to be more efficient and cost-effective for finding security defects in custom applications than black box techniques"; black box serve para ver o comportamento em execucao e a interacao com usuarios, outros sistemas e o ambiente.
Fonte: https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-115.pdf (Apendice C)

Traducao pratica [CONSOLIDADO]:
- **Preta**: sem credenciais nem documentacao. Mede o que um estranho alcanca. Gasta tempo em descoberta que o cliente poderia ter entregue.
- **Cinza**: credenciais de usuario comum e/ou documentacao parcial. Melhor custo-beneficio na maioria dos casos.
- **Branca**: codigo, arquitetura, configuracao e credenciais administrativas. Maior cobertura por hora paga.
- Caixa preta **nao e mais rigorosa** — e apenas mais cega. Rigor vem do escopo e do tempo, nao da ignorancia do testador.

### Externo x interno

[CONFIRMADO] "Since a penetration test scenario can be designed to simulate an inside attack, an outside attack, or both, external and internal security testing methods are considered. **If both internal and external testing is to be performed, the external testing usually occurs first.**"
[CONFIRMADO] **Outsider**: "testers are provided with no real information about the target environment other than targeted IP addresses or address ranges" + OSINT + varredura; como o trafego passa por firewall, "the amount of information obtained from scanning is far less than if the test were undertaken from an insider perspective".
[CONFIRMADO] **Insider**: "the testers are on the internal network (i.e., behind the firewall) and have been granted some level of access"; a partir dai tentam escalada de privilegio, recebendo "network information that someone with their level of access would normally have".
[CONFIRMADO] Cautela de escopo: "If given a list of authorized IP addresses to use as targets, assessors should verify that all public addresses ... are under the organization's purview before testing begins" (WHOIS).
Fonte: https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-115.pdf (secao 5.2.2)

### Overt x covert (o eixo que o iniciante esquece)

[CONFIRMADO] **Overt** ("white hat testing") = com conhecimento e consentimento da equipe de TI; permite avaliacao ampla e vira treinamento para a equipe. **Covert** ("black hat testing") = sem conhecimento da equipe de TI, **mas com pleno conhecimento e permissao da alta gerencia**; muitas vezes com um terceiro de confianca mediando para evitar resposta a incidente desnecessaria. "The purpose of covert testing is to examine the damage or impact an adversary can cause — it **does not focus on identifying vulnerabilities**. This type of testing does not test every security control, identify each vulnerability, or assess all systems". Custa mais e demora mais por causa da furtividade; overt "is less expensive, carries less risk ... and is more frequently used".
Fonte: mesmo PDF, secao 2.4.2 (e glossario: "Covert Testing: Testing performed using covert methods and without the knowledge of the organization's IT staff, but with full knowledge and permission of upper management"; "Overt Testing: Security testing performed with the knowledge and consent of the organization's IT staff").

### Red team x pentest x varredura de vulnerabilidade

| | Varredura de vulnerabilidade | Pentest | Red team |
|---|---|---|---|
| Pergunta | "O que aparenta estar vulneravel?" | "O que consigo de fato explorar e ate onde chego?" | "A organizacao detecta e responde a um adversario determinado?" |
| Confirmacao | Nao explora | Explora para confirmar | Explora o minimo necessario para atingir objetivos |
| Cobertura | Ampla, automatizada, rasa | Ampla-media, manual, profunda no escopo | Estreita e orientada a objetivo |
| Alvo da avaliacao | Sistemas | Sistemas e configuracao | Pessoas, processos e tecnologia de defesa |
| Frequencia tipica | Continua/semanal | Periodica | Anual ou menos |

[CONFIRMADO — varredura x pentest] "While vulnerability scanners check only for the possible existence of a vulnerability, the attack phase of a penetration test exploits the vulnerability to confirm its existence" e "A well-designed program of regularly scheduled network and vulnerability scanning, **interspersed with periodic penetration testing**, can help prevent many types of attacks" (o NIST trata os dois como complementares, com cadencias diferentes; sugere que pentest anual pode bastar pelo custo e impacto).
Fonte: https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-115.pdf (secao 5.2)

[CONFIRMADO — red team] Ficha oficial da CISA (fev/2022): "CISA's Red Team Assessment (RTA) is a comprehensive evaluation of an information technology (IT) environment. **Simulation of advanced persistent threats (APTs)** ... testing the effectiveness of **response capabilities** ... CISA crafts the RTAs to specifically test the **people, processes, and technologies defending a network**". Componentes: *Threat Simulation* (TTPs e intencao de APT, buscando demonstrar risco de negocio) e *Measurable Events* — "This series of events is **specifically intended to provoke a security response**. CISA measures the effectiveness of the people, processes, and technologies defending the customer's network using **observable, response-driven metrics**". Fases: Pre-Planning (pedido, briefing, **assinatura de formularios**), Planning (agenda, escopo, **pontos de contato de confianca**), Execution (OSINT, simulacao de APT, ativacao dos eventos mensuraveis), Post-Execution (out brief e treinamento).
Fonte: https://www.cisa.gov/sites/default/files/publications/VM_Assessments_Fact_Sheet_RTA_508C.pdf (recuperado via curl; WebFetch retornou 403)

[CONSOLIDADO] Confusoes comuns a desfazer: (a) rodar um scanner e entregar o PDF dele **nao** e pentest; (b) red team **nao** e "pentest mais caro" — muda a metrica (deteccao e resposta, nao cobertura de vulnerabilidades); (c) um red team costuma **deixar vulnerabilidades sem reportar** porque nao eram necessarias ao objetivo; (d) sem um blue team monitorando e sem um "white cell"/contato de confianca, um red team vira so um pentest furtivo caro.

---

## 5. O relatorio como produto final

[CONFIRMADO] PTES: "The report is broken down into **two (2) major sections**" — **Executive Summary** e **Technical Report**.
Fonte: http://www.pentest-standard.org/index.php/Reporting

**Sumario executivo** (publico: quem responde pelo programa de seguranca e pelos riscos) — secoes que o PTES manda ter [CONFIRMADO, mesma URL]:
- **Background**: proposito do teste, ligacao com o que foi acordado no pre-engagement; se os objetivos mudaram durante o teste, "all changes must be listed in this section" e a carta de aditamento vai no anexo.
- **Overall Posture**: narrativa da eficacia do teste e distincao entre problema **sistemico** e **sintomatico** (exemplo do proprio PTES: "Systemic issue = Lacking Effective Patch Management Process vs. Symptomatic = Found MS08-067 missing on xyz box").
- **Risk Ranking/Profile**: a nota geral e **o mecanismo de pontuacao definido no pre-engagement** (o PTES cita FAIR, DREAD e escalas proprias).
- **General Findings**: sintese estatistica/grafica, causa-raiz, e metricas de eficacia das contramedidas ("we ran x attacks and IPS blocked y").
- **Recommendation Summary**: esforco necessario e criterio de priorizacao.
- **Strategic Roadmap**: plano priorizado, pesado contra objetivos de negocio, ligado ao threat modeling.

**Relatorio tecnico** [CONFIRMADO, mesma URL]: "will describe in detail the scope, information, attack path, impact and remediation suggestions of the test", com:
- **Introduction**: pessoas envolvidas dos dois lados, contatos, ativos, objetivos, escopo, "strength of test", abordagem, estrutura de classificacao de ameaca.
- **Information Gathering**: inteligencia passiva, ativa, corporativa e de pessoal.
- **Vulnerability Assessment**: "the act of identifying the POTENTIAL vulnerabilities"; niveis de classificacao, vulnerabilidades tecnicas (achadas por scanner x manualmente) e logicas, exposicao, sumario de resultados.
- **Exploitation / Vulnerability Confirmation**: "the act of triggering the vulnerabilities identified in the previous sections to gain a specified level of access"; linha do tempo da exploracao, alvos selecionados, e **em detalhe todos os passos** usados para confirmar.
- Depois: post-exploitation, impacto de negocio e remediacao.

[CONFIRMADO] NIST 800-115 sobre relatorio (secao 8): recomendacoes de mitigacao devem sair "for each finding", incluindo o resultado da **analise de causa-raiz**, com recomendacoes tecnicas (ex.: aplicar patch) **e nao tecnicas** (ex.: corrigir o processo de gestao de patches). "Because a report may have multiple audiences, **multiple report formats may be required**". Relatorios internos "should include test methodology, test results, analysis, and POA&M" (plano de acao com marcos), garantindo que cada vulnerabilidade tenha acao "specific, measurable, attainable, realistic, and tangible". O relatorio serve como referencia para acao corretiva, benchmark de progresso, insumo de analise custo/beneficio e cumprimento de obrigacoes de reporte.
Fonte: https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-115.pdf (secoes 8.1–8.3)

### Anatomia de um achado bem escrito [CONSOLIDADO]

Um achado que presta responde, nesta ordem, sem obrigar o leitor a adivinhar:
1. **Titulo factual** — o que e, onde, qual efeito. "Injecao de SQL em /api/v1/orders (parametro `sort`) permite leitura de toda a tabela de clientes" — nao "Falha critica de banco de dados".
2. **Alvo exato** — host/URL/endpoint, parametro, versao, ambiente (prod/homologacao), data e hora do teste.
3. **Passos de reproducao** — numerados, do zero, com requisicao completa (metodo, cabecalhos, corpo), usuario usado e resultado esperado a cada passo. Criterio: alguem de fora reproduz sem falar com voce.
4. **Evidencia** — resposta bruta, captura de tela com timestamp, hash do arquivo obtido. **Evidencia minima suficiente**: prova o acesso sem despejar dado pessoal real no relatorio (mascare; cite volume e tipo em vez de colar os registros).
5. **Impacto** — o que um atacante consegue **neste ambiente**, ligado ao negocio (dados de N clientes, fraude financeira, parada de servico), nao a adjetivos.
6. **Pre-requisitos e dificuldade** — precisa de credencial? de rede interna? de interacao de usuario? Isso e o que separa "critico" de "teorico".
7. **Correcao** — recomendacao especifica e verificavel (consulta parametrizada nesse endpoint), mais a correcao sistemica (revisar todos os endpoints do mesmo padrao) e mitigacao temporaria se houver.
8. **Classificacao de risco** — nota + vetor + a justificativa em uma frase.
9. **Referencias** — CWE, WSTG-ID, CVE quando aplicavel.

### Classificacao de risco [CONSOLIDADO]

- Use **uma** escala declarada no pre-engagement e explique-a no relatorio (o PTES exige exatamente isso: o mecanismo de pontuacao e acordado antes).
- Risco util = severidade tecnica **x** exposicao real **x** valor do ativo. Um CVSS 9.8 num servico interno desligado atras de duas VPNs pode ficar abaixo de um 6.5 exposto na internet com exploracao ativa.
- Nao empilhe cinquenta achados "medios" de scanner: agrupe por causa-raiz (o NIST fala em causa-raiz e em recomendacao de processo).
- Diga sempre **quando** o achado foi observado; o ambiente muda.

---

## 6. CVSS

### Versao vigente em 2026 — confirmado na fonte

[CONFIRMADO] A pagina oficial do SIG na FIRST apresenta **CVSS v4.0 como versao atual**, com nota de que "The CVSS SIG continues to work on gathering feedback and updating CVSS v4.0"; a v3.1 aparece na secao de **arquivo** (calculadora, especificacao, user guide, exemplos), continua acessivel e em uso. **Nao ha v4.1 nem v5.0** anunciadas na pagina (consulta em 19/08/2026).
Fonte: https://www.first.org/cvss/

[CONFIRMADO] O documento de especificacao da v4.0 esta em **Document Version 1.2**.
Fonte: https://www.first.org/cvss/v4.0/specification-document

[CONFIRMADO] Existem exemplos oficiais da v4.0 datados de **2026-07-02, versao 1.8** — ou seja, a v4.0 continua recebendo manutencao editorial em 2026.
Fonte: https://www.first.org/cvss/v4-0/cvss-v40-examples.pdf (data e versao visiveis no titulo do documento retornado pela busca)

[CONFIRMADO] **v3.1 e v4.0 coexistem na pratica**: o NVD "supports Common Vulnerability Scoring System (CVSS) v2.0, v3.x and v4.0 standards"; para CVEs novos o NVD parou de gerar v2.0 (aposentadoria anunciada; desde 13/07/2022 nao gera vetor/severidade v2.0 para registros novos) e "All new and additional CVE assessments will be done using the **CVSS v3.1 guidance**" (nao oferece v3.0 e v3.1 para o mesmo CVE).
Fonte: https://nvd.nist.gov/vuln-metrics/cvss

[CONSOLIDADO] Datas de referencia: CVSS v4.0 publicado em **1 de novembro de 2023**; CVSS v3.1 de **junho de 2019**. Consequencia pratica em 2026: **fornecedores e bases publicam ora v3.1, ora v4.0, ora ambos** — o relatorio precisa dizer qual versao usou e colar o **vetor**, nao so o numero.

### O que muda da v3.1 para a v4.0

[CONFIRMADO] Estrutura em **quatro grupos**: Base, Threat, Environmental e o novo **Supplemental** (Safety, Automatable, Provider Urgency, Recovery, Value Density, Vulnerability Response Effort — contexto que **nao** altera a nota).
[CONFIRMADO] Nomenclatura nova para deixar explicito o que foi pontuado: **CVSS-B, CVSS-BT, CVSS-BE, CVSS-BTE**.
[CONFIRMADO] Base: nova metrica **Attack Requirements (AT)**; **User Interaction (UI)** ganha tres valores (None / Passive / Active); o **Scope** da v3.x sai e no lugar entram impactos separados no **sistema vulneravel (VC/VI/VA)** e nos **sistemas subsequentes (SC/SI/SA)**.
[CONFIRMADO] Threat: **Exploit Maturity (E)** substitui o "Exploit Code Maturity", com valores Attacked / POC / Unreported / Not Defined.
[CONFIRMADO] **Safety** entra como metrica (Supplemental e Environmental), com alinhamento a IEC 61508 — relevante para OT/ICS e dispositivos medicos.
Fonte: https://www.first.org/cvss/v4.0/specification-document

[CONSOLIDADO] Motivacao declarada da v4.0: granularidade fina demais concentrava tudo em "High/Critical" na v3.1, e o grupo Threat/Environmental era pouco usado. A v4.0 nao conserta isso sozinha — ela **da estrutura para o consumidor enriquecer a nota**.

### Por que a nota sozinha nao define prioridade

[CONFIRMADO] A propria especificacao: consumidores "should enrich the Base metrics with Threat and Environmental metric values specific to their use of the vulnerable system"; e "Consumers may use CVSS information as input to an organizational vulnerability management process **that also considers factors that are not part of CVSS** in order to rank the threats ... Such factors may include, but are not limited to: **regulatory requirements, number of customers impacted, monetary losses due to a breach, life or property threatened, or reputational impacts**. These factors are **outside the scope of CVSS**."
Fonte: https://www.first.org/cvss/v4.0/specification-document

[CONFIRMADO] E por isso que existem metodos de decisao por cima do CVSS. A CISA usa **SSVC** (criado pelo SEI/CMU com a CISA em 2019; arvore propria da CISA desde 2020), que classifica em **Track / Track\* / Attend / Act** com base em cinco valores: **exploitation status, technical impact, automatable, mission prevalence, public well-being impact**. "Implementing SSVC has allowed CISA to better prioritize its vulnerability response".
Fonte: https://www.cisa.gov/stakeholder-specific-vulnerability-categorization-ssvc (recuperado via curl; WebFetch retornou 403)

[CONSOLIDADO] Complementos usuais na priorizacao: **KEV** da CISA (esta sendo explorado no mundo real), **EPSS** da FIRST (probabilidade de exploracao nos proximos 30 dias) e o contexto do ativo (exposicao, criticidade, compensating controls). Regra pratica para o relatorio: **CVSS ordena severidade; a prioridade sai de severidade + exploracao ativa + exposicao + valor do ativo.**

---

## 7. Regras de engajamento e autorizacao

### O que precisa estar por escrito e assinado

[CONFIRMADO] **Autorizacao formal antes de qualquer pacote**: PTES — "One of the most important documents which need to be obtained for a penetration test is the **Permission to Test** document. This document states the scope and contains a signature which acknowledges awareness of the activities of the testers. Further, it should clearly state that testing can lead to system instability and all due care will be given by the tester to not crash systems in the process. ... **It is critical that testing does not begin until this document is signed by the customer.**" O mesmo trecho lembra que provedores terceiros podem exigir autorizacao propria previa.
Fonte: http://www.pentest-standard.org/index.php/Pre-engagement

[CONFIRMADO] **Quem assina**: NIST 800-115 — no minimo o lider do time de teste e a alta gerencia da organizacao (CSO/CISO/CIO), declarando que entenderam escopo e limites.
Fonte: https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-115.pdf (Apendice B.7)

Checklist do que tem que estar no papel (uniao PTES + NIST, itens todos [CONFIRMADO] nas fontes acima):
- Proposito, partes e **escopo** com fronteiras de acao e resultado esperado.
- **Alvos autorizados** (IPs, dominios, aplicacoes) **e a exclude list** de sistemas proibidos.
- Terceiros envolvidos (cloud, ISP, MSSP, pais onde os servidores estao) e suas autorizacoes proprias.
- Tecnicas permitidas e proibidas: DoS sim/nao, engenharia social e **pretextos aceitos**, teste fisico, se pode instalar/criar/modificar/executar arquivos e o que acontece com eles depois.
- Ferramentas autorizadas e como distinguir as maquinas do testador (IP/MAC) das do cliente.
- Premissas, limitacoes e **riscos inerentes** com mitigacoes; declaracao de que o teste pode causar instabilidade.
- Cronograma e **janela de teste**.
- Contatos, comunicacao, criptografia obrigatoria, frequencia de status.
- **Criterio de parada** e procedimento de incidente.
- **Data handling** (coleta, guarda, transmissao, destruicao).
- Entregaveis e formato de relatorio.
- **Pagina de assinaturas.**

### Janela de teste

[CONFIRMADO] NIST: o cronograma deve dizer as horas em que o teste ocorre — "it may be prudent to conduct technical testing of an operational site during evening hours rather than during peak business periods". PTES coloca "Timeline" e "Time of the Day to Test" dentro da secao Rules of Engagement, alem de "Specify Start and End Dates".
Fontes: https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-115.pdf (B.2.2); http://www.pentest-standard.org/index.php/Pre-engagement

[CONSOLIDADO] Registre tambem: fuso horario, congelamentos (fechamento de mes, Black Friday, folha de pagamento), e o que fazer se a janela estourar (aditamento por escrito — o PTES exige listar mudancas de objetivo no relatorio e anexar a carta de aditamento).

### Contatos de emergencia

[CONFIRMADO] PTES: lista de contatos de emergencia compartilhada com todos os envolvidos, com, para cada contato: nome completo, cargo e responsabilidade operacional, **autorizacao para discutir detalhes do teste**, **duas formas de contato imediato 24/7** e uma forma de transferencia segura de dados em massa (SFTP ou e-mail cifrado). A lista deve incluir todos os testadores, o gerente do time, **dois contatos tecnicos na organizacao alvo, dois no cliente e um contato executivo/de negocio**, com um responsavel unico por parte. Um numero de help desk/NOC so substitui um contato se for 24/7. Lembrete importante do PTES: **"the target organization may not be the customer"**.
Fonte: http://www.pentest-standard.org/index.php/Pre-engagement

[CONFIRMADO] NIST: o ROE traz a tabela de pontos de contato do time, da gerencia e do **time de resposta a incidentes**, e a arvore de chamadas do IR em formato de consulta rapida.
Fonte: NIST SP 800-115, Apendice B.2.1 e B.3.2.

[CONFIRMADO] PTES tambem trata a interacao com o IR: alguem no alvo precisa saber quando o teste ocorre "so the incident response team does not start to call every member of upper management in the middle of the night because they thought they were under attack"; e usa a definicao de incidente do NIST SP 800-61 ("a violation or imminent threat of violation of computer security policies, acceptable use policies, or standard security practices").
Fonte: http://www.pentest-standard.org/index.php/Pre-engagement

### Criterio de parada

[CONFIRMADO] NIST, no ROE: "**Criteria for halting** the information security testing should be provided", junto com o curso de acao se um procedimento degradar a rede **ou se um adversario real atacar durante o teste**, e com "A process for **reinstating** the test team and resuming testing".
[CONFIRMADO] NIST, no corpo: o teste pode ser desenhado para parar quando a proxima acao causaria dano; teste coberto costuma ter fronteiras do tipo "parar ao atingir certo nivel de acesso" — "Having such boundaries prevents damage while still showing that the damage could occur".
Fontes: NIST SP 800-115, Apendices B.3.2 e secoes 5.2.2 / 2.4.2.

Gatilhos tipicos de parada imediata [CONSOLIDADO]: indisponibilidade de servico causada pelo teste; corrupcao de dado; descoberta de comprometimento pre-existente por atacante real; acesso a dado fora do escopo (pessoal, medico, financeiro, de terceiro); alcance do objetivo acordado ("flag" capturada); saida do escopo autorizado (IP de terceiro, ambiente de producao nao previsto). Em todos: **parar, preservar log, avisar o contato acordado, so retomar por escrito**.

### Dado sensivel encontrado durante o teste

[CONFIRMADO] O ROE do NIST exige "guidelines for gathering, storing, transmitting, and destroying test data" com requisitos "detailed, unambiguous", e adverte: "data results from any type of information security test will identify vulnerabilities that an adversary can exploit, and **should be considered sensitive**". A secao 7.4 detalha coleta com log de atividade (audit trail que distingue testador de adversario real), armazenamento seguro sob responsabilidade do assessor, transmissao e destruicao.
Fonte: NIST SP 800-115, Apendices B.5.3 e secao 7.4.

[CONFIRMADO] PTES: "Encryption is not optional" — a comunicacao com o cliente, especialmente o relatorio final, deve ser cifrada (PGP/GPG, com o lembrete de que o assunto do e-mail viaja em claro; ou caixa segura). O ROE do PTES tem item proprio de **Evidence Handling**.
Fonte: http://www.pentest-standard.org/index.php/Pre-engagement

[CONSOLIDADO] Regra pratica ao topar com dado pessoal/regulado (PII, saude, cartao, segredo de terceiro): pare de coletar assim que o acesso estiver provado; **prove com metadado** (contagem de registros, nomes de coluna, um trecho mascarado), nao com o conteudo; nao exfiltre para fora da infra acordada; registre o horario e avise o contato; se o ROE nao previu o caso, isso vira decisao conjunta por escrito, nao decisao do testador. Se houver indicio de comprometimento previo ou de crime, o teste para e vira acionamento do IR/juridico do cliente.

[CONFIRMADO] E lembre da secao de legalidade: PTES adverte que "some activities common in penetration tests may violate local laws" (o exemplo dado e captura de VoIP tratada como escuta ilegal em algumas jurisdicoes); NIST tem secao propria de Legal Considerations (6.6).
Fontes: http://www.pentest-standard.org/index.php/Pre-engagement ; NIST SP 800-115 secao 6.6.

---

## ARMADILHAS: o que NAO escrever

1. **Nao escreva que o PTES e "o padrao atual da industria" sem data.** Ele parou em 16/08/2014, se declara v1.0 e prometeu uma v2.0 que nunca veio; o site nem HTTPS tem. Escreva "referencia estavel e amplamente citada, sem manutencao desde 2014".
2. **Nao apresente as sete fases do PTES como se fossem obrigatorias e sequenciais.** Elas se sobrepoem — e o proprio NIST diz que dividir em fases e apenas "an example ... There are many acceptable ways".
3. **Nao trate o NIST SP 800-115 como guia tecnico atual.** E de setembro de 2008. Cite-o para processo, ROE e manuseio de dados; nao para ferramenta, nuvem, contêiner ou tecnica moderna. E nao escreva que "esta sendo revisado" — a pagina do CSRC nao indica revisao.
4. **Nao diga que reporting e a ultima fase.** No 800-115 o reporting "occurs simultaneously with the other three phases".
5. **Nao chame OSSTMM de "versao 4".** A versao publicada e a **3.02, de 14/12/2010**; a v4 nunca saiu publicamente. E nao apresente OSSTMM como guia de exploracao web — ele e auditoria operacional multi-canal com metrica rav.
6. **Nao diga que o WSTG e um "framework de pentest".** E catalogo de testes de aplicacao web (v4.2, 03/12/2020; v5.0 em desenvolvimento, ainda nao lancada). Nao invente numero de versao nova: verifique na pagina do projeto/releases antes.
7. **Nao escreva "o WSTG e de 2023".** A pre-release de 28/09/2023 e so distribuicao de PDF/ePub; a estavel e de 2020. Foi um erro que apareceu numa das leituras automaticas desta pesquisa e so caiu ao conferir a API do GitHub.
8. **Nao equipare caixa preta a "teste mais realista/rigoroso".** Caixa preta so tira informacao do testador; rigor vem de escopo, tempo e acesso. O NIST inclusive diz que white box tende a ser mais eficiente e barato para achar defeito em aplicacao propria.
9. **Nao confunda o eixo caixa (preta/cinza/branca) com o eixo visibilidade (overt/covert) nem com o eixo posicao (externo/interno).** Sao tres eixos independentes.
10. **Nao venda red team como "pentest premium".** Red team mede deteccao e resposta de pessoas, processos e tecnologia (CISA: "measurable events ... intended to provoke a security response"); ele **nao** faz cobertura de vulnerabilidades. Cliente sem monitoramento nenhum nao precisa de red team.
11. **Nao chame relatorio de scanner de pentest.** Scanner indica existencia possivel; pentest explora para confirmar (NIST 5.2.1). Achado sem tentativa de confirmacao e "potencial", e deve ser rotulado assim.
12. **Nao escreva achado sem passos de reproducao ou sem evidencia.** "Sistema vulneravel a XSS" sem requisicao, sem parametro e sem prova nao e achado, e opiniao.
13. **Nao cole dado pessoal real como evidencia.** Prove com metadado e amostra mascarada; o dado do teste ja e sensivel por natureza (NIST 7.4) e o vazamento do relatorio vira o incidente.
14. **Nao entregue um sumario executivo cheio de jargao nem um relatorio tecnico com "risco alto" sem vetor.** Sao dois publicos; o NIST diz explicitamente que multiplos formatos podem ser necessarios.
15. **Nao escreva "CVSS 9.8, portanto prioridade 1".** A propria especificacao coloca requisitos regulatorios, numero de clientes, perda financeira, risco a vida e reputacao **fora do escopo do CVSS**. Priorize com contexto (SSVC, KEV, EPSS, exposicao).
16. **Nao diga que a v3.1 "foi aposentada".** Em 2026 v3.1 e v4.0 coexistem: o NVD suporta v2.0, v3.x e v4.0 e ainda avalia CVEs novos com a orientacao v3.1. Sempre registre versao **e vetor**.
17. **Nao afirme que existe CVSS v5 ou v4.1.** Na pagina da FIRST consultada em 19/08/2026 nao ha nada alem da v4.0 (que segue recebendo atualizacoes editoriais — exemplos oficiais versao 1.8, de 02/07/2026).
18. **Nao escreva que o CVSS mede risco.** Ele comunica "characteristics and severity"; risco e a organizacao que calcula.
19. **Nao comece teste sem documento assinado.** PTES: "It is critical that testing does not begin until this document is signed by the customer". E autorizacao do cliente nao substitui autorizacao do provedor de nuvem/ISP quando o ativo e deles.
20. **Nao omita a exclude list.** Escopo que so diz o que pode ser testado esta pela metade; o NIST chama de "crucial" identificar o que **nao** pode.
21. **Nao deixe o criterio de parada implicito** ("o bom senso do testador"). ROE precisa de gatilho de parada, arvore de acionamento e processo escrito de retomada.
22. **Nao trate contato de emergencia como uma linha de e-mail.** Duas formas de contato 24/7 por pessoa, responsavel unico por parte, canal cifrado para dado em massa — e cuidado com a suposicao de que alvo e cliente sao a mesma organizacao.
23. **Nao prometa "zero impacto".** O proprio NIST diz que sistemas podem ficar inoperantes e que o risco "can never be fully eliminated"; escreva isso no ROE em vez de esconder.
24. **Nao chame nada disso de "certificacao" nem de conformidade automatica.** Um pentest e uma foto datada de um escopo definido, nao um selo.
25. **Nao cite URL sem checar se carrega.** Nesta pesquisa: `https://pentest-standard.org` recusa conexao (so HTTP funciona), `web.archive.org` estava indisponivel para a ferramenta, e paginas da CISA devolveram 403 ao fetch automatico (precisaram de curl). Se a fonte nao abriu, diga que nao abriu — nao preencha com memoria.
