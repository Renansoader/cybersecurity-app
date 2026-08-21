# Módulo OSINT e Reconhecimento — o que precisa acertar e onde ficam os limites

Levantamento fechado em **19/08/2026**. Convenção de marcação:

- **[CONFIRMADO]** — fui à fonte primária/oficial nesta sessão e li a afirmação lá.
- **[CONSOLIDADO]** — consenso técnico ou jurídico estabelecido, com URL de apoio, mas sem verificação em fonte primária nesta sessão (ou a fonte primária estava indisponível).

---

## 1. A fronteira passivo × ativo

### 1.1 Onde exatamente ela está

A fronteira **não** é "usei ferramenta ofensiva ou não". É: **saiu pacote meu (ou por minha ordem) em direção à infraestrutura do alvo?**

- Consultar um terceiro que já publicou o dado (log CT, índice de busca, banco de banners, registro RDAP, repositório público) = **passivo**. Quem tocou o alvo foi o terceiro, antes e por conta própria.
- Resolver um nome, forçar transferência de zona, abrir TCP/443 para ler o certificado, tirar screenshot, testar wordlist de diretório = **ativo**.

Definição de referência, verbatim do MITRE ATT&CK T1595 Active Scanning: *"Active scans are those where the adversary probes victim infrastructure via network traffic, as opposed to other forms of reconnaissance that do not involve direct interaction."*
[CONFIRMADO] https://attack.mitre.org/techniques/T1595/

O contraste na própria taxonomia: T1596.003 (Digital Certificates, ou seja, leitura de logs CT) é classificado como reconhecimento **sem** interação direta, pré-comprometimento, cuja única mitigação listada é M1056 Pre-compromise — "minimizing the amount and sensitivity of data available to external parties".
[CONFIRMADO] https://attack.mitre.org/techniques/T1596/003/

Referência metodológica clássica para o par passivo/ativo em teste técnico: NIST SP 800-115, *Technical Guide to Information Security Testing and Assessment*, set/2008, ainda listado como publicação vigente no CSRC.
[CONFIRMADO] https://csrc.nist.gov/pubs/sp/800/115/final

> Nota de estado: o PTES (pentest-standard.org), citado em quase toda bibliografia de recon, estava **fora do ar** nesta sessão (ECONNREFUSED em 96.126.116.56:443, 19/08/2026). Não use como fonte viva sem checar. [CONFIRMADO]

### 1.2 A zona cinzenta que derruba gente

Existe um terceiro caso que não é nem um nem outro na intuição, mas é **ativo** na prática: **mandar um terceiro tocar o alvo por você**.

- Shodan **on-demand scanning**: a API permite pedir varredura imediata de uma rede, 1 crédito por IP, com bloqueio de 24h para re-scan. Não há verificação de propriedade documentada. O pacote sai da Shodan, mas por ordem sua e com o alvo que você escolheu.
  [CONFIRMADO] https://help.shodan.io/the-basics/on-demand-scanning
- theHarvester classifica módulos exatamente por isso: `pentesttools`, `shodan` e `subdomainfinderc99` são **P1** (não-passivos), `criminalip` é **P2** — enquanto os outros ~54 são P0.
  [CONFIRMADO] https://github.com/laramies/theHarvester

Regra operacional: **classifique por destino do pacote, não por qual aba do programa você clicou.**

### 1.3 Por que a fronteira importa

**Juridicamente (Brasil).** O tipo penal do art. 154-A do CP exige **invadir dispositivo informático de uso alheio** com finalidade específica. Consulta a terceiro não invade nada, não toca dispositivo do alvo, e não preenche o núcleo do tipo. Pacote enviado ao alvo ainda não é invasão — mas é o primeiro degrau de uma escalada que pode chegar lá, e desde 2021 sem a antiga válvula de escape do "mecanismo de segurança violado" (ver §9). [CONSOLIDADO]

**Operacionalmente.** Recon passivo não gera evento no WAF, no IDS nem no log do alvo — logo não queima a operação nem contamina a linha do tempo de um teste. Recon ativo aparece. Também: passivo pode ser feito **antes** do contrato assinado sem risco; ativo, não.

**Contratualmente.** Escopo de teste normalmente autoriza *ativos do cliente*. Recon passivo colhe dados de terceiros (SaaS, CDN, provedor) que **não estão no seu escopo** — o dado é lícito de ler, mas testá-lo ativamente não é autorizado pelo seu contrato com o cliente.

---

## 2. Ferramentas — o que coletam, de onde, se tocam o alvo, e estado atual

Estado verificado via API do GitHub em 19/08/2026.

| Ferramenta | Toca o alvo? | Estado |
|---|---|---|
| theHarvester | Não por padrão (P0); sim com flags P1/P2 | Ativo, release 4.11.1 (jun/2026) |
| Amass | Sim, por design (modo `-active`) | Ativo, v5.1.1 (abr/2026) |
| Shodan | Não ao consultar; **sim** no on-demand scan | Comercial, ativo |
| Censys | Não ao consultar; a Censys varre por conta própria | Comercial, ativo; Legacy Search descontinuada |
| Maltego | Depende do transform | Comercial, ativo; CE limitada |
| SpiderFoot | Depende do módulo | OSS sem release desde 2022; dono é a Intel 471 |
| recon-ng | Depende do módulo | **Dormente** (sem commit desde nov/2024) |

### 2.1 theHarvester — CONFIRMADO, não mudou de casa

**Continua em `github.com/laramies/theHarvester`.** Não migrou para organização nenhuma. Não arquivado, não desabilitado, último push **18/08/2026**, 17.118 stars, branch `master`, sem licença declarada nos metadados da API.
[CONFIRMADO] https://api.github.com/repos/laramies/theHarvester

Última release **4.11.1, publicada em 03/06/2026** (novo módulo Sherlockeye, bumps de aiohttp/fastapi/uvicorn).
[CONFIRMADO] https://api.github.com/repos/laramies/theHarvester/releases/latest

Autor Christian Martorella (@laramies); mantenedores atuais Matt Brown (@NotoriousRebel1) e Jay Townsend (@jay_townsend1). [CONFIRMADO]

**O que coleta e de onde:** e-mails, subdomínios, nomes, hosts, IPs, banners de ASN. 58 fontes de descoberta, entre elas logs CT (`crtsh`, `certspotter`, `crt-name`, `shodanct`), motores de busca (`baidu`, `brave`, `duckduckgo`, `mojeek`, `yahoo`), repositórios de código (`github-code`, `gitlab`, `sourcegraph`), threat intel (`otx`, `virustotal`, `urlscan`, `leakix`), arquivos web (`waybackarchive`, `commoncrawl`, `arquivo`), enriquecimento de pessoa (`hunter`, `rocketreach`, `tomba`, `intelx`) e bases de vazamento (`haveibeenpwned`, `dehashed`, `hudsonrock`).
[CONFIRMADO] https://github.com/laramies/theHarvester

**Toca o alvo?** Classificação explícita do README, verbatim: *"Passive sources are P0. DNS resolution, brute force, recursive DNS, and reverse lookup are P1. HTTP, TLS, screenshot, takeover, virtual-host, port, and endpoint actions are P2."* E: *"Run it only against targets you own or have explicit permission to test."*
[CONFIRMADO] https://github.com/laramies/theHarvester

Ou seja: `theharvester -d alvo.com -b crtsh` é passivo puro. Adicione `-r` (resolve), `-c` (brute force DNS), `--screenshot` ou varredura de porta e você atravessou a linha.

### 2.2 Amass — CONFIRMADO, **mudou de casa**

**Endereço antigo `github.com/OWASP/Amass` redireciona: a API do GitHub responde com `full_name: "owasp-amass/amass"`.** O projeto saiu do repositório monolítico da OWASP para uma **organização própria, `owasp-amass`**, que hospeda também `amass-docs`, `asset-db`, `open-asset-model` e imagens Docker.
[CONFIRMADO] https://api.github.com/repos/OWASP/Amass e https://github.com/owasp-amass

Estado: não arquivado, último push **19/07/2026**, branch `main`, ~14.993 stars, 237 issues abertas, **Apache License 2.0** (a API reporta "NOASSERTION" por metadado, mas o arquivo LICENSE é Apache-2.0 padrão, sem cláusula de restrição comercial).
[CONFIRMADO] https://api.github.com/repos/owasp-amass/amass e https://raw.githubusercontent.com/owasp-amass/amass/main/LICENSE

Última release **v5.1.1, 07/04/2026** — novo Asset Database com mudança de schema, Go 1.26, engine REST API reescrita, dispatcher com backlog durável.
[CONFIRMADO] https://api.github.com/repos/owasp-amass/amass/releases/latest

Suporte migrou do issue tracker para o Discord do projeto. [CONFIRMADO]

**O que coleta:** mapeamento de superfície de ataque e descoberta de ativos externos — subdomínios, ASNs, blocos de IP, relações entre organizações, dados de certificado, no modelo Open Asset Model.

**Toca o alvo?** **Sim, e assume isso no README, verbatim:** *"The OWASP Amass Project performs network mapping of attack surfaces and external asset discovery using open source information gathering and **active reconnaissance** techniques."*
[CONFIRMADO] https://raw.githubusercontent.com/owasp-amass/amass/main/README.md

A documentação oficial usa `-active` no exemplo canônico (`docker compose run --rm enum -active -d example.org`).
[CONFIRMADO] https://owasp-amass.github.io/docs/

Na prática, `-active` liga tentativa de transferência de zona, coleta de nomes em certificados TLS abrindo conexão nos IPs descobertos, e o modo de brute force resolve nomes de verdade. Sem root domain definido, Amass tenta alcançar **todo IP da infraestrutura identificada** para pegar nomes de certificado — comportamento barulhento.
[CONSOLIDADO] https://pkg.go.dev/github.com/aokimio/Amass/v3/enum

**Consequência prática: Amass não é ferramenta de OSINT passivo.** Tratá-lo como tal é o erro mais comum do módulo.

### 2.3 Shodan

**O que coleta e de onde:** banners de serviços de dispositivos diretamente conectados à internet — tipo e versão de software, mensagens de boas-vindas, opções suportadas, certificados, telas. Fonte: **varredura própria da Shodan**, não de terceiros.
Verbatim: *"Shodan gathers information about all devices directly connected to the Internet. If a device is directly hooked up to the Internet then Shodan queries it for various publicly-available information."*
[CONFIRMADO] https://book.shodan.io/getting-started/overview/

**Frequência:** *"Shodan crawls the entire Internet at least once a week."*
[CONFIRMADO] https://help.shodan.io/the-basics/on-demand-scanning

**Toca o alvo?** Consultar o índice: **não**. Usar on-demand scan: **sim** — você paga 1 crédito por IP e a Shodan dispara a varredura naquele instante, com cooldown de 24h (contornável no Enterprise com `force`). Isso é reconhecimento ativo por procuração.
[CONFIRMADO] https://help.shodan.io/the-basics/on-demand-scanning

**Estado:** produto comercial ativo, com Shodan Monitor para monitoramento de superfície própria. [CONFIRMADO] https://monitor.shodan.io/

### 2.4 Censys

**O que coleta e de onde:** varredura própria da internet — hosts, serviços, certificados, DNS, WHOIS, web screenshots (nos tiers pagos), CVEs associados. Verbatim da documentação: *"Censys scans help the scientific community accurately study the Internet."*
[CONFIRMADO] https://docs.censys.com/docs/opt-out-of-data-collection

**Infraestrutura de varredura publicada** (é um vendor que se identifica): sub-redes IPv4 como `162.142.125.0/24` e `66.132.159.0/24`, faixas IPv6 como `2602:80d:1000:b0cc:e::/80`, ASNs **AS398722, AS398705, AS398324**, e User-Agent `Mozilla/5.0 (compatible; CensysInspect/1.1; +https://about.censys.io/)`.
[CONFIRMADO] https://docs.censys.com/docs/opt-out-of-data-collection

**Toca o alvo?** Consultar: não. A Censys, sim, continuamente, por conta própria.

**Estado — mudou bastante:** a **Legacy Search foi descontinuada para usuários Free após 31/03/2025**; usuários Free migraram para a **Censys Platform**, e as APIs Search v1/v2 estão em rota de aposentadoria (meta declarada: fim de 2025), com nova base URL e Personal Access Token. Tiers atuais: Free (41 protocolos, 1 página / 100 resultados), Starter (por créditos), Search e Core (enterprise, histórico de host 31+ dias, todos os campos de certificado pesquisáveis).
[CONFIRMADO tiers] https://docs.censys.com/docs/data-access-tiers-entitlements
[CONSOLIDADO datas de descontinuação] https://community.censys.com/censys-platform-q-a-58

### 2.5 Maltego

**O que coleta:** não coleta nada por si — é plataforma de **grafo de link analysis**. Coleta vem dos *Transforms* (conectores para APIs de terceiros: DNS, WHOIS/RDAP, redes sociais, VirusTotal, Shodan, bases comerciais).

**Toca o alvo?** **Depende do transform.** Transform de "DNS from domain" resolve — ativo. Transform que consulta VirusTotal — passivo. Não existe resposta única; é preciso auditar transform a transform. Essa é a armadilha estrutural do Maltego num módulo de ensino.

**Estado:** produto comercial (Maltego Technologies), ativo. A **Community Edition** exige conta Maltego ID e é limitada a **24 resultados por Transform**, grafo de até **10.000 entidades**, e mínimo de **200 créditos/mês** de Maltego Data.
[CONFIRMADO] https://docs.maltego.com/en/support/solutions/articles/15000018947-what-is-maltego-graph-community-edition-ce-

### 2.6 SpiderFoot

**O que coleta:** automação de OSINT com 200+ módulos — domínios, IPs, e-mails, nomes, hashes de vazamento, dados de threat intel, correlacionados num alvo.

**Toca o alvo?** Depende do módulo; a interface separa varreduras "passive" das que fazem resolução/HTTP. Configuração padrão **não** é totalmente passiva.

**Estado — o ponto sensível:** repositório `smicallef/spiderfoot`, MIT, 21.193 stars, **não arquivado**, último push **13/04/2026**. Mas a **última release marcada é v4.0, de 07/04/2022** — quatro anos sem versão.
[CONFIRMADO] https://api.github.com/repos/smicallef/spiderfoot e https://api.github.com/repos/smicallef/spiderfoot/releases/latest

Motivo: a **Intel 471 adquiriu a SpiderFoot em 02/11/2022**, e o fundador Steve Micallef entrou na Intel 471 como VP of Attack Surface Technology. O produto comercial (SpiderFoot HX) foi absorvido na plataforma da Intel 471; o OSS ficou disponível, mas com desenvolvimento sob prioridade comercial.
[CONFIRMADO] https://www.intel471.com/blog/intel-471-acquires-spiderfoot

Classificação honesta para o módulo: **disponível, não morto, mas sem release há 4 anos e com o dono focado no produto pago.**

### 2.7 recon-ng

**O que coleta:** framework modular estilo Metasploit para OSINT — módulos de recon (hosts, contatos, credenciais, portas, perfis), reporting e marketplace de módulos.

**Toca o alvo?** Depende do módulo carregado; há módulos puramente de API e módulos que resolvem/varrem.

**Estado — dormente.** `lanmaster53/recon-ng` (Tim Tomes), GPL-3.0, 5.860 stars, **não arquivado**, mas o **último push é de 01/11/2024** — quase dois anos parado em 19/08/2026. **Não há releases publicadas no GitHub** (endpoint `/releases/latest` responde 404); a última tag é **v5.1.2**.
[CONFIRMADO] https://api.github.com/repos/lanmaster53/recon-ng e https://api.github.com/repos/lanmaster53/recon-ng/tags

Ensinar recon-ng hoje é ensinar arqueologia útil (o padrão de workspace + módulo + keystore é bom), não ferramenta de linha de frente.

### 2.8 Complementar — metagoofil

`laramies/metagoofil`, colhe documentos públicos de um domínio e extrai metadados. **Não arquivado, último push 21/03/2024**, 1.310 stars.
[CONFIRMADO] https://api.github.com/repos/laramies/metagoofil

---

## 3. Operadores de busca (dorks) — o que ainda vale hoje

**Aviso de método:** Google documenta oficialmente muito pouco. A página de ajuda ao usuário lista apenas `""`, `site:`, `-`, `before:`, `after:` e `filetype:`.
[CONFIRMADO] https://support.google.com/websearch/answer/2466433

E no Search Central, o único operador com página dedicada é `site:`.
[CONFIRMADO] https://developers.google.com/search/docs/monitor-debug/search-operators/all-search-site

Tudo que estiver fora dessas duas listas funciona **de fato**, mas **sem garantia contratual** — pode sumir sem aviso, como já aconteceu.

### 3.1 Mortos — confirmados, não presumidos

| Operador | Situação | Fonte |
|---|---|---|
| `cache:` | **Morto.** Link "Em cache" removido dos snippets em jan/2024; Danny Sullivan: *"You're going to see cache: go away in the near future, too."* O changelog de documentação do Google registrou depois: *"The cache: search operator no longer works in Google Search."* | [CONFIRMADO] https://searchengineland.com/google-search-officially-retires-cache-link-437122 e https://www.searchenginejournal.com/google-removes-cache-search-operator-documentation/528022/ |
| `related:` | **Morto.** Confirmado por Danny Sullivan em **19/07/2023**: *"It hasn't really worked that well for some time, as in some cases, the information was dated."* | [CONFIRMADO] https://searchengineland.com/google-confirms-related-search-operator-is-going-away-429575 |
| `link:` | Descontinuado em 2017; ainda retorna algo, mas é amostra filtrada e inútil para recon. | [CONSOLIDADO] https://ahrefs.com/blog/google-advanced-search-operators/ |
| `info:` | Descontinuado em 2017; virou alias lento para digitar a URL. | [CONSOLIDADO] https://ahrefs.com/blog/google-advanced-search-operators/ |
| `+` (força exata) | Removido em 2011. | [CONSOLIDADO] https://support.google.com/websearch/answer/2466433 |
| `~` (sinônimos) | Removido em 2013. | [CONSOLIDADO] |

**Substituto de `cache:` para OSINT:** Wayback Machine (`web.archive.org`), Common Crawl, e o cache do Bing quando existir. Não há equivalente 1:1.

### 3.2 Vivos e úteis (funcionam, mas só os dois primeiros são documentados)

`site:` · `filetype:` (e `ext:`) · `intitle:` / `allintitle:` · `inurl:` / `allinurl:` · `intext:` / `allintext:` · `""` · `-` · `OR` / `|` · `*` · `before:` / `after:` · `AROUND(X)` (irregular) · `define:` · `source:` (Google News) · `imagesize:` · `src:`

O OWASP WSTG (WSTG-INFO-01) continua recomendando exatamente `site:`, `inurl:`, `intitle:`, `intext:`/`inbody:` e `filetype:` — e insiste: *"Do not limit testing to just one search engine provider, as different search engines may generate different results."* Motores sugeridos: Google, Bing, Baidu, DuckDuckGo, Wayback Machine, Shodan, Censys, Common Crawl.
[CONFIRMADO] https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/01-Information_Gathering/01-Conduct_Search_Engine_Discovery_Reconnaissance_for_Information_Leakage

### 3.3 GHDB

A **Google Hacking Database** é *"a categorized index of Internet search engine queries designed to uncover interesting, and usually sensitive, information made publicly available on the Internet"*. Criada por Johnny Long em 2000, **transferida para a OffSec em novembro de 2010** e mantida por ela desde então, hoje incluindo consultas para Bing e GitHub.
[CONFIRMADO] https://www.exploit-db.com/google-hacking-database

**Ponto de ensino:** dork não é portável. `filetype:` do Google é `filetype:` no Bing mas `mime:` em alguns; DuckDuckGo e Yandex têm sintaxes próprias. Cada entrada de GHDB precisa ser retestada, e uma fração significativa não retorna mais nada — não por a exposição ter sumido, mas por o operador ter mudado.

---

## 4. Certificate Transparency como fonte de subdomínio

### 4.1 A norma

**RFC 6962 — "Certificate Transparency"**, status **Experimental**, junho de 2013. Define log público, append-only e não confiável (untrusted) de certificados TLS, com propriedade de append-only garantida por **Merkle Tree**, para que qualquer um possa auditar a atividade de CAs.
[CONFIRMADO] https://www.rfc-editor.org/rfc/rfc6962

**RFC 6962 está formalmente obsoletado pela RFC 9162 — "Certificate Transparency Version 2.0"**, também **Experimental**, dezembro de 2021.
[CONFIRMADO] https://www.rfc-editor.org/rfc/rfc9162.html

Verbatim da 9162 sobre append-only: *"The append-only property of each log is achieved using Merkle Trees, which can be used to efficiently prove that any particular instance of the log is a superset of any particular previous instance."* E sobre acesso: *"Log operators SHOULD NOT impose any conditions on retrieving or sharing data from the log."*
[CONFIRMADO] https://www.rfc-editor.org/rfc/rfc9162.html

**Precisão importante:** apesar de a 9162 obsoletar formalmente a 6962, o ecossistema em produção rodou v1 (RFC 6962) por quase toda a década. Dizer "CT é a RFC 6962" está desatualizado; dizer "todo mundo implementa a 9162" está errado. [CONSOLIDADO]

### 4.2 Por que os dados existem — a obrigação do navegador

Não é opcional. Política de CT do Chrome, verbatim: *"In CT-enforcing versions of Chrome, all publicly-trusted TLS certificates are required to be CT Compliant to successfully validate."* Certificado precisa de SCTs de logs qualificados de operadores distintos.
[CONFIRMADO] https://googlechrome.github.io/CertificateTransparency/ct_policy.html

**Consequência para o atacante:** todo certificado público válido do alvo — inclusive de `jenkins-interno.alvo.com.br`, `vpn-teste.alvo.com.br`, `sap-hml.alvo.com.br` — está num log público, permanentemente, e é indexado por buscadores de CT.

### 4.3 crt.sh

Buscador público de logs CT. Permite consulta por domínio (com `%` como curinga), por Issuer, por hash SHA-256, e expõe a base via interface web e JSON. O schema é aberto: `github.com/crtsh/certwatch_db`, licença **GPL-3.0**.
[CONFIRMADO] https://github.com/crtsh/certwatch_db

Operado pela Sectigo. [CONSOLIDADO]

> Estado do serviço: **`https://crt.sh/` respondeu HTTP 502 nesta sessão (19/08/2026)**. crt.sh é notoriamente instável sob carga — um módulo que depende só dele quebra. Alternativas: `certspotter` (SSLMate), `censys` (campo de certificado), `shodanct`, e leitura direta dos logs. [CONFIRMADO]

### 4.4 O que mudou na infraestrutura de CT — e por que o módulo precisa saber

Está em curso a migração dos logs RFC 6962 (servidor dinâmico) para a **Static CT API** ("tiled logs"): o log publica todos os dados como hierarquia de arquivos estáticos servidos de object storage/CDN, sem computação no caminho de leitura. A implementação de referência é o **Sunlight**, de Filippo Valsorda com a Let's Encrypt.
[CONFIRMADO] https://letsencrypt.org/2025/06/11/reflections-on-a-year-of-sunlight

**Ponto crítico para quem constrói coletor:** a API **não é retrocompatível** — a própria Let's Encrypt avisa que quem monitora CT *"need to update your data pipeline"*.
[CONFIRMADO] https://letsencrypt.org/2025/06/11/reflections-on-a-year-of-sunlight

Chrome, em fase de validação, aceita SCTs de logs tiled desde que ao menos um SCT venha de log RFC 6962, e sinalizou aceitar novos logs RFC 6962 pelo menos até 2026. Logs RFC 6962 da Let's Encrypt entraram em read-only em 30/11/2025 e foram desligados em 28/02/2026.
[CONSOLIDADO] https://groups.google.com/a/chromium.org/g/ct-policy/c/HBFZHG0TCsY/m/HAaVRK6MAAAJ

**Não existe redação de nomes DNS em CT.** Busquei no texto da RFC 9162: nenhum mecanismo de redação, nenhum label `?`, nenhuma substituição por privacidade. A ideia de "redigir nomes no precertificado" ficou nos rascunhos do 6962-bis e **não sobreviveu**.
[CONFIRMADO] https://www.rfc-editor.org/rfc/rfc9162.html

---

## 5. Metadados de documento como vazamento

### 5.1 O que vaza

De um único PDF ou DOCX publicado no site institucional: **nome do autor** (frequentemente o login de rede), **caminho completo do arquivo** (revela nome de servidor, share SMB, estrutura de departamento), **versão do software** que gerou (Word 2016? LibreOffice? Acrobat 9?), datas de criação/modificação, impressora, histórico de revisão, comentários não removidos, e em imagens embutidas o EXIF completo com GPS.

Ancoragem MITRE, T1592.002 (Software), verbatim: *"Information about the installed software may also be exposed to adversaries via online or other accessible data sets (ex: job postings, network maps, assessment reports, resumes, or purchase invoices)."* E a mesma técnica cita explicitamente análise de metadados de arquivos da vítima para extrair versões e configurações que indiquem software desatualizado ou vulnerável.
[CONFIRMADO] https://attack.mitre.org/techniques/T1592/002/

### 5.2 Ferramentas de leitura

- **ExifTool** (Phil Harvey), biblioteca Perl + CLI, **v13.59 de 27/05/2026**, 300+ formatos, lê e escreve EXIF, GPS, IPTC, XMP, JFIF, GeoTIFF, ICC Profile, Photoshop IRB, ID3 e maker notes de fabricante.
  [CONFIRMADO] https://exiftool.org/
- **metagoofil** — colhe os documentos do domínio e extrai metadados em lote. Repo com push em mar/2024. [CONFIRMADO] https://github.com/laramies/metagoofil
- **FOCA** — extrai metadados de rede (impressoras, caminhos, SSIDs, usuários) de documentos e monta o mapa organizacional. [CONSOLIDADO] https://github.com/ElevenPaths/FOCA

### 5.3 Ferramentas de limpeza — e onde elas falham

- **mat2** — **mudou de casa.** O repositório histórico em `0xacab.org/jvoisin/mat2` está **ARQUIVADO e read-only**. O projeto vivo é `github.com/jvoisin/mat2`, **LGPL-3.0**, último push **18/08/2026**.
  [CONFIRMADO] https://0xacab.org/jvoisin/mat2 e https://api.github.com/repos/jvoisin/mat2
- **ExifTool** — **não garante remoção completa.** A própria documentação: em JPEG a remoção é razoavelmente completa; em TIFF, PNG e outros pode restar metadado residual.
  [CONFIRMADO] https://exiftool.org/

**A armadilha do PDF, verbatim da documentação do ExifTool:** *"All metadata edits are reversible. While this would normally be considered an advantage, it is a potential security problem because old information is never actually deleted from the file."* O ExifTool edita PDF por *incremental update* — o metadado antigo continua no arquivo e é recuperável. O remédio é passar depois: `qpdf --linearize in.pdf out.pdf`.
[CONFIRMADO] https://exiftool.sourceforge.net/TagNames/PDF.html

Ou seja: `exiftool -all= relatorio.pdf` **não limpa o PDF**. Quem ensina isso como limpeza está ensinando errado.

---

## 6. Pegada digital de pessoa

### 6.1 Vaga de emprego

A vaga é o documento de arquitetura que a empresa publica de graça. "Experiência com Fortigate 7.2, Citrix NetScaler, SAP ECC 6.0, Oracle 12c on-prem, VPN Pulse Secure" descreve o parque inteiro, com versão. Também revela tamanho de time, ferramentas de CI, provedor de nuvem e — no anúncio interno de sucessão — quem saiu.

Ancoragem: MITRE T1592.002 lista `job postings` e `resumes` como fonte, e T1591.004 (Identify Roles) trata de mapear papéis e responsabilidades de pessoas-chave.
[CONFIRMADO] https://attack.mitre.org/techniques/T1592/002/ e https://attack.mitre.org/techniques/T1591/

### 6.2 Repositório público

MITRE T1593.003 (Code Repositories), verbatim: *"Public code repositories can often be a source of various general information about victims, such as commonly used programming languages and libraries as well as the names of employees. Adversaries may also identify more sensitive data, including accidentally leaked credentials or API keys."*
[CONFIRMADO] https://attack.mitre.org/techniques/T1593/003/

Vetores além do óbvio: e-mail corporativo nos commits (`git log --format='%ae'` de um repositório pessoal), padrão de nome de usuário, `.env` commitado e depois removido (mas vivo no histórico), Terraform state, `.tfvars`, `docker-compose.yml` com senha padrão, comentário com IP interno.

### 6.3 Foto com geolocalização

EXIF GPS em foto de crachá, de mesa de trabalho, de confraternização. A tag `GPSLatitude`/`GPSLongitude` dá coordenada; `DateTimeOriginal` dá rotina; o modelo de câmera/celular dá o dispositivo; o que está **no fundo da foto** (crachá, monitor com aplicação aberta, quadro branco, etiqueta de patrimônio) costuma valer mais que o EXIF.

Plataformas grandes (Instagram, Facebook, X, LinkedIn, TikTok, Reddit) removem EXIF do arquivo que o público baixa — mas isso é **uma proteção do arquivo público, não uma política de dados**: a plataforma leu e guardou o original. E a limpeza **não** vale para o que importa em OSINT corporativo: site institucional, blog da empresa, PDF de relatório anual, bucket S3 público, wiki interna exposta, anexo de e-mail vazado.
[CONSOLIDADO] https://exifdata.org/blog/do-social-media-sites-strip-exif-data-2025-test

---

## 7. LADO DEFENSIVO — redução de pegada

Enquadramento de partida, do próprio MITRE: reconhecimento *"cannot be easily mitigated with preventive controls since it is based on behaviors performed outside of the scope of enterprise defenses and controls"*; o que resta é **"minimizing the amount and sensitivity of data available to external parties"** (M1056 Pre-compromise).
[CONFIRMADO] https://attack.mitre.org/techniques/T1596/003/

Ou seja: **defesa contra OSINT é higiene de publicação, não bloqueio.** Quem tenta bloquear perde.

### 7.1 O que uma organização REMOVE

- Documentos públicos com metadado sujo — republicar limpos, remover os antigos do site **e** pedir remoção do índice (não só `robots.txt`, ver 7.5).
- Segredos em repositório: **rotacionar primeiro, remover depois.** GitHub, verbatim: *"if the sensitive data you need to remove is a secret (e.g. password/token/credential), as is often the case, then as a first step you need to revoke and/or rotate that secret."*
  [CONFIRMADO] https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository
- Páginas de status, painéis de monitoramento, Swagger/OpenAPI de API interna e `/.git/` expostos.
- Listas telefônicas internas e organogramas em PDF público.

### 7.2 O que SEGREGA

- **Nomes internos fora de certificado público.** Como não existe redação de nomes em CT (§4.4), o único controle real é **não colocar o hostname no SAN**: usar **certificado wildcard** (`*.corp.alvo.com.br`) para o que é interno, ou CA interna própria para o que nunca sai da rede. [CONSOLIDADO, ancorado no fato CONFIRMADO de que a RFC 9162 não tem redação]
- **Split-horizon DNS**: zona interna que não resolve de fora e nunca aparece em resolvers públicos.
- Ambientes de homologação em domínio separado, sem padrão previsível (`hml-`, `dev-`, `-teste` é convite a brute force de subdomínio).
- Contas corporativas separadas de contas pessoais em GitHub/GitLab, para o e-mail corporativo não sair no `git log` de projeto pessoal.

### 7.3 O que LIMPA

Pipeline obrigatório antes de publicar qualquer arquivo:
1. `mat2 arquivo` (https://github.com/jvoisin/mat2) — ou `exiftool -all=` para imagem.
2. **Para PDF, obrigatoriamente**: `exiftool -all= in.pdf` **seguido de** `qpdf --linearize in.pdf out.pdf`, senão o metadado continua recuperável. [CONFIRMADO] https://exiftool.sourceforge.net/TagNames/PDF.html
3. Conferir com `exiftool -a -u -g1 arquivo` que não sobrou nada.

Em vaga de emprego: descrever **competência**, não inventário. "Experiência com firewall de próxima geração" em vez de "Fortigate 7.2.4". Não perde candidato e não entrega o parque.

### 7.4 O que MONITORA

- **Logs CT do próprio domínio** — alerta em certificado emitido para nome seu que você não pediu (detecta tanto shadow IT quanto emissão fraudulenta). crt.sh, Cert Spotter, Censys.
- **Repositórios públicos** — MITRE M1047, verbatim: *"scan public code repositories for exposed credentials or other sensitive information before making commits"* e garantir que *"leaked credentials are removed from the commit history, not just the current latest version of the code."*
  [CONFIRMADO] https://attack.mitre.org/techniques/T1593/003/
- **Dorks contra o próprio domínio, periodicamente.** WSTG: *"Periodically review the sensitivity of existing design and configuration information that is posted online."*
  [CONFIRMADO] https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/01-Information_Gathering/01-Conduct_Search_Engine_Discovery_Reconnaissance_for_Information_Leakage
- **A própria superfície em Shodan/Censys** — Shodan Monitor existe para isso. https://monitor.shodan.io/

### 7.5 O que NÃO adianta — a parte que quase todo material omite

| Medida | Por que não resolve | Fonte |
|---|---|---|
| **Esconder WHOIS / privacidade de domínio** | Não remove nenhum hostname do log CT, que é append-only e público por norma. Além disso, o WHOIS de gTLD já era: **a obrigação contratual de oferecer WHOIS acabou em 28/01/2025** e o RDAP (com dados de registrante em grande parte redigidos) passou a ser a fonte definitiva. Você está "escondendo" um dado que já estava redigido, e não tocou no que realmente vaza. | [CONFIRMADO] https://www.icann.org/en/announcements/details/icann-update-launching-rdap-sunsetting-whois-27-01-2025-en + https://www.rfc-editor.org/rfc/rfc9162.html |
| **`robots.txt` para esconder página** | Google, verbatim: *"it is not a mechanism for keeping a web page out of Google."* Pior: o `robots.txt` vira **mapa** do que você quis esconder. Use `noindex` ou senha. | [CONFIRMADO] https://developers.google.com/search/docs/crawling-indexing/robots/intro |
| **Bloquear as sub-redes da Censys/Shodan no firewall** | Censys, verbatim: *"Blocking connections from Censys' subnets prevents our scanners from indexing your services. However, this does not remove historical data from Censys datasets."* E existem dezenas de outros scanners. | [CONFIRMADO] https://docs.censys.com/docs/opt-out-of-data-collection |
| **Tirar a página do ar** | O Internet Archive **parou de usar `robots.txt`** para decidir exibição de arquivo; remoção é por pedido a `info@archive.org`. Common Crawl e caches de terceiros são outra história. | [CONFIRMADO] https://blog.archive.org/2017/04/17/robots-txt-meant-for-search-engines-dont-work-well-for-web-archives/ |
| **Reescrever o histórico do git sem rotacionar o segredo** | GitHub: o dado continua *"in any clones or forks of your repository"*, *"directly via their SHA-1 hashes in cached views on GitHub"* e *"through any pull requests that reference them"*. Fork de terceiro não some. | [CONFIRMADO] https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository |
| **`exiftool -all=` em PDF** | Edição por incremental update é reversível; o metadado velho continua lá. Sem `qpdf --linearize`, você não limpou nada. | [CONFIRMADO] https://exiftool.sourceforge.net/TagNames/PDF.html |
| **Revogar/trocar o certificado que expôs o hostname** | O certificado antigo continua no log CT para sempre. Revogação não desfaz publicação. | [CONFIRMADO — append-only] https://www.rfc-editor.org/rfc/rfc9162.html |
| **Pedir para o funcionário apagar o post** | O post pode já estar em arquivo, print e agregador. Trate como "vazou = vazou" e ajuste o que ainda dá (rotação, segregação). | [CONSOLIDADO] |

---

## 8. Limites legais no Brasil

> Não é aconselhamento jurídico. É o mapa do terreno, com o cuidado de **não exagerar** — que é o erro mais comum do material de treinamento brasileiro.

### 8.1 LGPD — Lei 13.709/2018

**Dado público continua sendo dado pessoal.** A definição do art. 5º, I não tem exceção para dado publicado: *"informação relacionada a pessoa natural identificada ou identificável"*. Se o e-mail corporativo `joao.silva@alvo.com.br` está no site, ele é dado pessoal — coletá-lo é **tratamento** (art. 5º, X, que inclui expressamente "coleta").
[CONFIRMADO] https://lgpd-brasil.info/capitulo_01/artigo_05

**O art. 7º, §4º é mal citado o tempo todo.** Ele diz, verbatim: *"É dispensada a exigência do consentimento previsto no caput deste artigo para os dados tornados manifestamente públicos pelo titular, resguardados os direitos do titular e os princípios previstos nesta Lei."*
[CONFIRMADO] https://lgpd-brasil.info/capitulo_02/artigo_07

O que ele dispensa: **o consentimento.** O que ele **não** dispensa: nada mais. E o §6º diz isso explicitamente — a dispensa de consentimento não afasta as demais obrigações da lei.
[CONFIRMADO] https://lgpd-brasil.info/capitulo_02/artigo_07

E o **§3º** impõe um teste finalístico que quase todo mundo ignora: o tratamento de dados de acesso público *"deve considerar a finalidade, a boa-fé e o interesse público que justificaram sua disponibilização"*. Traduzindo para recon: a pessoa publicou o e-mail para ser contatada profissionalmente, **não** para virar alvo de campanha de phishing simulado sem base própria.
[CONFIRMADO] https://lgpd-brasil.info/capitulo_02/artigo_07

**Os princípios do art. 6º continuam valendo integralmente** — finalidade, adequação, **necessidade** (limitar ao mínimo, "dados pertinentes, proporcionais e não excessivos"), qualidade, segurança, prevenção, não discriminação, responsabilização.
[CONFIRMADO] https://lgpd-brasil.info/capitulo_01/artigo_06

**Você não está fora da LGPD.** O art. 4º lista as hipóteses de não aplicação: pessoa natural para fins **exclusivamente particulares e não econômicos**; fins exclusivamente jornalísticos, artísticos ou acadêmicos; segurança pública/defesa/investigação criminal (com lei específica e sob ente público). **Um teste contratado é atividade econômica e não cai em nenhuma delas.**
[CONFIRMADO] https://lgpd-brasil.info/capitulo_01/artigo_04

**Base legal prática para recon contratado:** art. 7º, IX (legítimo interesse do controlador/terceiro) ou II (cumprimento de obrigação legal/regulatória), com LIA documentada, minimização de coleta, prazo de retenção definido e descarte ao fim do engajamento. O contratante costuma ser controlador e o testador operador — o contrato precisa dizer isso (arts. 5º, VI e VII, e 39). [CONSOLIDADO]

**Sanções (art. 52):** advertência com prazo; **multa simples de até 2% do faturamento do grupo no Brasil no último exercício, excluídos tributos, limitada a R$ 50.000.000,00 por infração**; multa diária; publicização da infração; bloqueio e eliminação dos dados; suspensão do banco de dados ou da atividade de tratamento por até 6 meses (prorrogável); proibição parcial ou total da atividade. Aplicadas pela **ANPD** — esfera **administrativa**, não penal.
[CONFIRMADO] https://lgpd-brasil.info/capitulo_08/artigo_52

### 8.2 Lei 12.737/2012 — o que ela DE FATO tipifica

Ementa: dispõe sobre a **tipificação criminal de delitos informáticos**, altera o Decreto-Lei 2.848/1940 (Código Penal). Publicada em 30/11/2012 (DOU 03/12/2012), em vigor desde **02/04/2013**. Conhecida como "Lei Carolina Dieckmann", origem no PL 2793/2011.
[CONFIRMADO] https://www.lexml.gov.br/urn/urn:lex:br:federal:lei:2012-11-30;12737

**O que ela inseriu/alterou:** arts. **154-A** e **154-B** no CP, e alterações nos arts. **266** (interrupção de serviço telemático ou de informação de utilidade pública) e **298** (falsificação de cartão). [CONSOLIDADO]

**Texto original do art. 154-A (2012):** *"Invadir dispositivo informático alheio, conectado ou não à rede de computadores, **mediante violação indevida de mecanismo de segurança** e com o fim de obter, adulterar ou destruir dados ou informações sem autorização expressa ou tácita do titular do dispositivo ou instalar vulnerabilidades para obter vantagem ilícita: Pena – detenção, de 3 (três) meses a 1 (um) ano, e multa."* [CONSOLIDADO]

**Redação atual, após a Lei 14.155/2021:** *"Invadir dispositivo informático de uso alheio, conectado ou não à rede de computadores, com o fim de obter, adulterar ou destruir dados ou informações sem autorização expressa ou tácita do usuário do dispositivo ou de instalar vulnerabilidades para obter vantagem ilícita: Pena – reclusão, de 1 (um) a 4 (quatro) anos, e multa."*
[CONFIRMADO — descrição e penas na página do TJDFT] https://www.tjdft.jus.br/institucional/imprensa/campanhas-e-produtos/direito-facil/edicao-semanal/violar-segredo-e-crime

**As quatro mudanças de 2021 que importam para recon:**
1. **Caiu a exigência de "violação indevida de mecanismo de segurança".** Este é o ponto que mais muda a conta de risco: antes, acessar algo que estava aberto tinha argumento forte de atipicidade; hoje, não tem mais esse degrau. [CONSOLIDADO] https://www.conjur.com.br/2021-mai-28/opiniao-lei-1415521-incrementa-punicao-crimes-eletronicos-informaticos/
2. "Dispositivo informático **alheio**" virou "**de uso alheio**" — alcança dispositivo que a pessoa usa sem ser dona (notebook da empresa, por exemplo).
3. "Titular do dispositivo" virou "**usuário** do dispositivo" — muda quem pode autorizar.
4. Pena subiu de detenção 3 meses–1 ano para **reclusão 1–4 anos**: deixou de ser infração de menor potencial ofensivo, saiu do JECrim.

**§3º:** se da invasão resulta obtenção de conteúdo de comunicações eletrônicas privadas, segredos comerciais ou industriais, informações sigilosas assim definidas em lei, ou controle remoto não autorizado do dispositivo — **reclusão de 2 a 5 anos e multa**. [CONFIRMADO — TJDFT]

**Art. 154-B — ação penal:** procede-se mediante **representação**, salvo se o crime é cometido contra a administração pública direta ou indireta de qualquer dos Poderes da União, Estados, DF ou Municípios, ou contra empresas concessionárias de serviços públicos — nesses casos, **ação penal pública incondicionada**.
[CONFIRMADO] https://www.tjdft.jus.br/institucional/imprensa/campanhas-e-produtos/direito-facil/edicao-semanal/violar-segredo-e-crime

### 8.3 O que a Lei 12.737/2012 NÃO tipifica — precisão importa

Aqui é onde o material de treinamento brasileiro costuma exagerar. Não faça isso.

- **Não tipifica varredura de portas.** Não há no Brasil crime de "port scan". Enviar SYN para uma porta não é invadir dispositivo.
- **Não tipifica consulta DNS, leitura de banner, resolução de nome ou transferência de zona bem-sucedida contra servidor mal configurado.** Nada disso é invasão.
- **Não tipifica dork, leitura de log CT, consulta a Shodan/Censys, coleta de metadado de documento publicado ou leitura de repositório público.** Isso é ler o que terceiros publicaram.
- **Não cria um tipo genérico de "acesso não autorizado a sistema".** O núcleo é **invadir dispositivo**, com dolo específico (obter/adulterar/destruir dados, ou instalar vulnerabilidade para vantagem ilícita). Sem essa finalidade, não fecha o tipo.
- **Não é a LGPD.** Sanção da ANPD é administrativa e independe de crime; crime do 154-A independe de haver dado pessoal envolvido. São trilhos separados que podem correr juntos.

**O que pode entrar se o "recon ativo" degradar serviço ou tocar o setor público:** CP art. 266, §1º (interromper ou perturbar serviço telemático ou de informação de utilidade pública) — alterado pela própria 12.737/2012; contra sistemas da administração pública, arts. 313-A e 313-B; e responsabilidade civil por dano, independentemente de tipo penal. [CONSOLIDADO]

### 8.4 O papel da autorização por escrito

**Precisão:** **não existe** dispositivo legal brasileiro que exija forma escrita para autorizar teste de segurança, nem que crie um "porto seguro" para pesquisador. Quem diz que "a lei exige contrato" está errado. O escrito serve para outra coisa — e serve muito.

1. **Afasta a tipicidade, não a ilicitude.** A ausência de autorização é **elemento do tipo** do art. 154-A ("sem autorização expressa ou tácita do usuário do dispositivo"). Com autorização, o fato é **atípico** — não é caso de excludente de ilicitude. A distinção é técnica e importa em defesa. [CONSOLIDADO]
2. **É prova.** Autorização verbal é válida ("expressa ou tácita" abrange verbal), mas é indefensável seis meses depois, quando quem autorizou saiu da empresa.
3. **Delimita escopo e janela.** Faixas de IP, domínios, horários, técnicas proibidas, contato de emergência, procedimento de parada. Fora do escopo escrito, você não tem autorização — tem improviso.
4. **Define papéis sob LGPD.** Quem é controlador, quem é operador, o que pode ser coletado, por quanto tempo fica retido, como é descartado, o que acontece se o teste esbarrar em dado pessoal de terceiro não relacionado ao alvo (arts. 5º, VI/VII, 39 e 42-45). [CONFIRMADO — estrutura da LGPD]
5. **Não estende a terceiros.** Autorização do cliente **não autoriza** tocar infraestrutura de provedor SaaS, cloud, CDN ou hospedagem. Cada um desses tem política própria de teste, e quem autoriza é o dono do dispositivo — que ali não é o seu cliente. Este é o furo mais comum em contratos reais.
6. **Quem assina precisa poder assinar.** Autorização vinda de quem não tem poder de representação vale pouco.

---

## ARMADILHAS

Erros que este módulo tem que evitar cometer — e ensinar a evitar.

1. **Chamar Amass de ferramenta passiva.** O README diz "active reconnaissance techniques". Rodar `amass enum -active` contra terceiro sem contrato é reconhecimento ativo com nome de OSINT.

2. **Achar que "não instalei nada ofensivo" = passivo.** O on-demand scan da Shodan (1 crédito/IP, sem verificação de propriedade) dispara pacote no alvo por sua ordem. theHarvester marca `shodan`, `pentesttools`, `subdomainfinderc99` como **P1** exatamente por isso. Classifique por **destino do pacote**, não por interface.

3. **Ensinar `cache:` e `related:`.** Ambos estão mortos — `related:` desde jul/2023, `cache:` desde 2024. Metade das folhas de dorks que circulam foi escrita antes disso e nunca foi retestada. Substituto de `cache:` é Wayback Machine, e não é equivalente.

4. **Presumir que os operadores são estáveis.** O Google documenta oficialmente **seis** operadores na ajuda e **um** (`site:`) no Search Central. `intitle:`, `inurl:`, `intext:` funcionam mas não têm garantia. Reteste antes de publicar qualquer lista.

5. **Dizer "CT é a RFC 6962" sem ressalva.** A 6962 foi **obsoletada pela RFC 9162** (dez/2021), e o ecossistema real está migrando para a **Static CT API** (tiled logs / Sunlight), que **não é retrocompatível**. Coletor de CT escrito para a API antiga vai quebrar.

6. **Depender só do crt.sh.** Ele respondeu **502 nesta sessão**. Um módulo com pipeline monofonte quebra na aula. Tenha certspotter/censys/shodanct como fallback.

7. **Vender "certificado wildcard esconde subdomínio" como redação de CT.** Não existe redação de nomes DNS na RFC 9162 — verifiquei o texto. Wildcard funciona porque o nome interno simplesmente **não é colocado** no SAN, não porque o log permita ocultar. Se o nome entrou, entrou para sempre.

8. **Ensinar `exiftool -all=` como limpeza de PDF.** Não é. A edição é incremental e reversível; o metadado antigo continua recuperável. Sem `qpdf --linearize` depois, o documento continua vazando.

9. **Confiar que `mat2` está onde estava.** O repositório do 0xacab está **arquivado/read-only**. O projeto vivo é `github.com/jvoisin/mat2`. Ensinar o link velho é ensinar software congelado.

10. **Tratar recon-ng e SpiderFoot como estado da arte.** recon-ng está sem commit desde **nov/2024** e sem release nenhuma publicada no GitHub. SpiderFoot está sem release marcada desde **v4.0 (abr/2022)** e pertence à Intel 471 desde nov/2022. Continuam funcionando; não são linha de frente. Diga isso.

11. **Ensinar `robots.txt` como medida de privacidade.** Google: *"it is not a mechanism for keeping a web page out of Google."* Pior: `robots.txt` é o índice do que você tentou esconder — é um alvo de dork, não uma defesa.

12. **Achar que bloquear scanner apaga o passado.** Censys: bloquear as sub-redes impede indexação futura, *"however, this does not remove historical data from Censys datasets"*.

13. **Reescrever histórico de git achando que resolveu.** Sem rotacionar o segredo, não resolveu nada — o dado sobrevive em forks, clones, views cacheadas por SHA-1 e PRs. Regra: **vazou = comprometido**.

14. **Citar o art. 7º, §4º da LGPD como se fosse passe livre para dado público.** Ele dispensa **só o consentimento**. O §3º ainda exige considerar finalidade, boa-fé e interesse público da disponibilização; o §6º mantém todas as demais obrigações; o art. 6º mantém todos os princípios; e o art. 4º **não** exclui atividade econômica.

15. **Exagerar a Lei 12.737/2012.** Ela **não** criminaliza port scan, consulta DNS, banner grabbing, dork, leitura de CT, nem coleta de metadado publicado. O tipo é **invadir dispositivo** com finalidade específica. Inflar o alcance da lei desmoraliza o material inteiro na primeira pergunta de aluno bem informado.

16. **Ignorar que a Lei 14.155/2021 retirou a exigência de "violação indevida de mecanismo de segurança".** Muito material ainda ensina a redação de 2012. Com isso caiu o argumento "estava aberto", e a pena virou reclusão de 1 a 4 anos — não é mais menor potencial ofensivo.

17. **Tratar a autorização como excludente de ilicitude.** É **atipicidade**: a falta de autorização é elemento do tipo do 154-A. E não há lei brasileira que exija forma escrita — o escrito é prova e delimitação de escopo, não requisito legal. Dizer o contrário é imprecisão jurídica.

18. **Assumir que a autorização do cliente cobre a nuvem dele.** Não cobre. Provedor SaaS/cloud/CDN é dispositivo de terceiro, com política própria. Escopo por domínio sem checar quem hospeda cada nome é como se derruba um teste.

19. **Confundir sanção da ANPD com crime.** LGPD é administrativa/civil (multa de até 2% do faturamento, teto R$ 50 mi por infração). Vazar dado colhido em recon pode gerar sanção **sem** existir crime nenhum.

20. **Não mencionar RDAP.** WHOIS de gTLD perdeu a obrigação contratual em **28/01/2025**; RDAP é a fonte definitiva e boa parte dos dados de registrante já vem redigida. Ensinar `whois` como fonte primária de recon em 2026 é ensinar uma ferramenta que muitos registries já desligaram.
