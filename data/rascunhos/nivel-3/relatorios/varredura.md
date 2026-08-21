# Varredura e Enumeração — levantamento em documentação oficial

Data do levantamento: 2026-08-19.
Convenção: **[CONFIRMADO]** = afirmação lida na documentação/fonte primária citada (texto do Nmap Reference Guide, RFC, ou código-fonte da release do tool). **[CONSOLIDADO]** = conclusão derivada de fontes confirmadas, mas que a fonte não enuncia com essas palavras.

Versões usadas como referência: Nmap Reference Guide (Cap. 15 do *Nmap Network Scanning*, edição online), Gobuster **v3.8.2** (release mais recente no repositório oficial), ffuf **v2.2.1** (release mais recente no repositório oficial).

---

## 1. Nmap — o que cada técnica manda na rede

### 1.1 Escolha padrão de técnica e privilégio

- Por padrão o Nmap faz **SYN scan**, mas substitui por **connect scan** se o usuário não tem privilégio para enviar pacotes crus: *"By default, Nmap performs a SYN Scan, though it substitutes a connect scan if the user does not have proper privileges to send raw packets (requires root access on Unix)."* **[CONFIRMADO]** — https://nmap.org/book/man-port-scanning-techniques.html
- Usuários sem privilégio só conseguem rodar **connect** e **FTP bounce**: *"Of the scans listed in this section, unprivileged users can only execute connect and FTP bounce scans."* **[CONFIRMADO]** — https://nmap.org/book/man-port-scanning-techniques.html
- Só uma técnica de porta por vez, exceto que **-sU pode ser combinado com um scan TCP** (e com SCTP `-sY`/`-sZ`): *"Only one method may be used at a time, except that UDP scan (-sU) and any one of the SCTP scan types (-sY, -sZ) may be combined with any one of the TCP scan types."* **[CONFIRMADO]** — https://nmap.org/book/man-port-scanning-techniques.html
- Em IPv6 e sem privilégio de raw packet, connect scan é o padrão: *"a user does not have raw packet privileges or is scanning IPv6 networks."* **[CONFIRMADO]** — https://nmap.org/book/scan-methods-connect-scan.html
- **Por que -sS exige privilégio:** o SYN scan monta e injeta pacotes TCP diretamente ("raw-packet privileges"), em vez de pedir a conexão ao SO pela API de sockets; montar/ler pacotes crus é operação restrita a root (Unix) ou a driver de captura (Npcap no Windows). **[CONFIRMADO]** para "requires raw-packet privileges / root access on Unix" — https://nmap.org/book/synscan.html e https://nmap.org/book/man-port-scanning-techniques.html ; **[CONSOLIDADO]** para a menção específica ao Npcap no Windows (o Reference Guide trata Npcap como requisito de raw packets em https://nmap.org/book/host-discovery-controls.html, ao descrever usuários "Windows users without Npcap").

### 1.2 `-sS` (TCP SYN scan / half-open)

- Envia um **SYN** e espera: **SYN/ACK ⇒ open**; **RST ⇒ closed**; **sem resposta após várias retransmissões ⇒ filtered**; **ICMP unreachable (type 3, code 0, 1, 2, 3, 9, 10 ou 13) ⇒ filtered**. Também marca **open** se receber um SYN sem ACK (caso raro de *simultaneous open / split handshake*). **[CONFIRMADO]** — https://nmap.org/book/man-port-scanning-techniques.html
- Nunca completa a conexão (não manda o ACK final); quem fecha é um RST. *"This technique is often referred to as half-open scanning, because you don't open a full TCP connection."* **[CONFIRMADO]** — https://nmap.org/book/man-port-scanning-techniques.html e https://nmap.org/book/synscan.html
- Diferencia com clareza **open / closed / filtered**, e funciona contra qualquer pilha TCP compatível (não depende de idiossincrasia de plataforma como FIN/NULL/Xmas). **[CONFIRMADO]** — https://nmap.org/book/man-port-scanning-techniques.html
- **O que o alvo registra:** a aplicação em geral não vê nada, porque a conexão nunca chega à camada de aplicação; mas *"widely deployed intrusion detection systems and even personal firewalls are quite capable of detecting default SYN scans"*. **[CONFIRMADO]** — https://nmap.org/book/synscan.html

### 1.3 `-sT` (TCP connect scan)

- Não escreve pacotes crus: pede ao SO a conexão via **chamada de sistema `connect`** (Berkeley Sockets), a mesma usada por navegadores. **[CONFIRMADO]** — https://nmap.org/book/man-port-scanning-techniques.html
- **Completa** a conexão nas portas abertas em vez do half-open: mais lento, mais pacotes para a mesma informação. **[CONFIRMADO]** — https://nmap.org/book/man-port-scanning-techniques.html
- **O que o alvo registra:** *"target machines are more likely to log the connection… Many services on your average Unix system will add a note to syslog, and sometimes a cryptic error message, when Nmap connects and then closes the connection without sending data."* E: *"An administrator who sees a bunch of connection attempts in her logs from a single system should know that she has been connect scanned."* **[CONFIRMADO]** — https://nmap.org/book/man-port-scanning-techniques.html
- Resumo prático da diferença -sS × -sT: mesma informação, camada diferente — -sS é visível ao IDS/firewall (rede), -sT é visível ao IDS **e** ao log do serviço (aplicação). **[CONSOLIDADO]** a partir das duas citações acima.

### 1.4 `-sU` (UDP scan)

- Manda um datagrama UDP a cada porta alvo; para portas comuns (ex.: 53, 161) envia **payload específico do protocolo**, mas *"for most ports the packet is empty unless the `--data`, `--data-string`, or `--data-length` options are specified."* **[CONFIRMADO]** — https://nmap.org/book/man-port-scanning-techniques.html
- Interpretação: **ICMP port unreachable (type 3, code 3) ⇒ closed**; **outros ICMP unreachable (type 3, codes 0, 1, 2, 9, 10, 13) ⇒ filtered**; **resposta UDP do serviço ⇒ open**; **nenhuma resposta após retransmissões ⇒ open|filtered**. **[CONFIRMADO]** — https://nmap.org/book/man-port-scanning-techniques.html
- Lentidão é estrutural: portas open e filtered normalmente não respondem (timeout + retransmissão), e portas closed sofrem **rate limit de ICMP** — *"the Linux 2.4.20 kernel limits destination unreachable messages to one per second"*, o que faz *"a 65,536-port scan take more than 18 hours."* **[CONFIRMADO]** — https://nmap.org/book/man-port-scanning-techniques.html e https://nmap.org/book/scan-methods-udp-scan.html
- Mitigações citadas pela própria doc: escanear só portas populares primeiro, mais hosts em paralelo, `--host-timeout`, e `-sV` para separar open de open|filtered. **[CONFIRMADO]** — https://nmap.org/book/man-port-scanning-techniques.html ; exemplo medido de `-F --version-intensity 0` reduzindo 3.691 s para 12,92 s em https://nmap.org/book/scan-methods-udp-scan.html **[CONFIRMADO]**

### 1.5 `-sn` (descoberta de host, sem varredura de portas)

- Privilegiado, por padrão envia **quatro** probes: *"an ICMP echo request, a TCP SYN packet to port 443, a TCP ACK packet to port 80, and an ICMP timestamp request"*. **[CONFIRMADO]** — https://nmap.org/book/host-discovery-controls.html
- Em Ethernet local usa **ARP**, a menos que `--send-ip` seja dado: *"ARP requests are used unless the `--send-ip` option is specified."* **[CONFIRMADO]** — https://nmap.org/book/host-discovery-controls.html
- Sem privilégio (usuário Unix comum, Windows sem Npcap): *"only SYN packets are sent instead"*, e são enviados *"using a TCP `connect` system call to ports 80 and 443"* — ou seja, o -sn não privilegiado **abre conexões reais** em 80/443. **[CONFIRMADO]** — https://nmap.org/book/host-discovery-controls.html
- Consequência de log: -sn privilegiado deixa rastro de rede (ICMP/ARP/SYN); -sn não privilegiado deixa rastro **de aplicação** em quem escuta 80/443. **[CONSOLIDADO]**

### 1.6 `-Pn` (pular descoberta de host)

- Não faz fase de descoberta: *"attempt[s] the requested scanning functions against every target IP address specified."* Um /16 vira 65.536 alvos escaneados por inteiro. **[CONFIRMADO]** — https://nmap.org/book/host-discovery-controls.html
- Uso legítimo: alvos com firewall que descartam probes de descoberta e seriam declarados "down" por engano; custo: muito mais lento (retransmissões e esperas contra IPs inexistentes). **[CONFIRMADO]** — https://nmap.org/book/host-discovery-controls.html
- `-Pn` **não** é opção de furtividade: ele aumenta o volume de pacotes contra hosts que não existem. **[CONSOLIDADO]**

---

## 2. Nmap — identificação, script, portas, tempo, estados

### 2.1 `-sV` (detecção de versão)

- Interroga portas abertas usando a base **`nmap-service-probes`** (probes + expressões de match). **[CONFIRMADO]** — https://nmap.org/book/man-version-detection.html
- Reporta: protocolo do serviço, nome da aplicação, número de versão, hostname, tipo de dispositivo, família de SO, **CPE** e detalhes extras. **[CONFIRMADO]** — https://nmap.org/book/man-version-detection.html
- Intensidade: `--version-intensity <0-9>` (**padrão 7**); `--version-light` = 2; `--version-all` = 9; `--allports` remove as exclusões (ex.: TCP 9100 de impressoras); `--version-trace` para depuração. **[CONFIRMADO]** — https://nmap.org/book/man-version-detection.html
- O mecanismo é "conectar e interrogar": ele diz *o que está realmente rodando*, não apenas quais números de porta estão abertos. **[CONFIRMADO]** — https://nmap.org/book/vscan.html
- `-sV` também converte parte dos `open|filtered` de UDP em `open`, porque força uma resposta do serviço. **[CONFIRMADO]** — https://nmap.org/book/man-port-scanning-techniques.html

### 2.2 `-O` (detecção de SO) e por que erra

- Método: **TCP/IP stack fingerprinting** — *"Nmap sends a series of TCP and UDP packets to the remote host and examines practically every bit in the responses… TCP ISN sampling, TCP options support and ordering, IP ID sampling, and the initial window size check"*, comparando com **`nmap-os-db`**, com *"more than 2,600 known OS fingerprints"*. **[CONFIRMADO]** — https://nmap.org/book/man-os-detection.html
- Depende de condições: *"OS detection is far more effective if at least one open and one closed TCP port are found"* (é isso que `--osscan-limit` exige). **[CONFIRMADO]** — https://nmap.org/book/man-os-detection.html
- Quando não há match perfeito, o Nmap oferece **near-matches**: `--osscan-guess` / `--fuzzy` faz ele chutar mais agressivamente, e *"Nmap will still tell you when an imperfect match is printed and display its confidence level (percentage) for each guess."* **[CONFIRMADO]** — https://nmap.org/book/man-os-detection.html
- Por que erra na prática: o -O infere o SO pelo comportamento da pilha; firewall/NAT/proxy/balanceador no caminho alteram ou bloqueiam as respostas, dispositivos embarcados compartilham pilhas, e falta de porta fechada (ou aberta) degrada a amostra. Daí saídas como "Aggressive OS guesses" e percentuais de confiança, que são **hipóteses, não fato**. **[CONSOLIDADO]** a partir de https://nmap.org/book/man-os-detection.html e https://nmap.org/book/osdetect.html
- Verificação é responsabilidade do operador: o capítulo de OS detection direciona explicitamente para conselhos de acurácia e verificação. **[CONFIRMADO]** — https://nmap.org/book/osdetect.html

### 2.3 `--script` / NSE e `-A`

- `-sC` é equivalente a `--script=default`, e a doc avisa: *"Some of the scripts in this category are considered intrusive and should not be run against a target network without permission."* **[CONFIRMADO]** — https://nmap.org/book/man-nse.html
- `--script` aceita lista separada por vírgula de **nomes de arquivo, categorias, diretórios ou expressões booleanas** (`and`, `or`, `not`, curingas). Também: `--script-args`, `--script-args-file`, `--script-help`, `--script-trace`, `--script-updatedb`. **[CONFIRMADO]** — https://nmap.org/book/man-nse.html
- Categorias documentadas: `auth`, `broadcast`, `default`, `discovery`, `dos`, `exploit`, `external`, `fuzzer`, `intrusive`, `malware`, `safe`, `version`, `vuln`. **[CONFIRMADO]** — https://nmap.org/book/man-nse.html
- Aviso de segurança do próprio manual: *"Scripts are not run in a sandbox and thus could accidentally or maliciously damage your system or invade your privacy. Never run scripts from third parties unless you trust the authors or have carefully audited the scripts yourself."* **[CONFIRMADO]** — https://nmap.org/book/man-nse.html
- `-A` habilita hoje: *"OS detection (-O), version scanning (-sV), script scanning (-sC) and traceroute (--traceroute)."* **[CONFIRMADO]** — https://nmap.org/book/man-misc-options.html

### 2.4 Portas: padrão, `-p-`, `-F`, `--top-ports`

- Padrão: *"the most common 1,000 ports for each protocol"* (ranking do arquivo `nmap-services`) — **não** são as portas 1-1000. **[CONFIRMADO]** — https://nmap.org/book/man-port-specification.html
- `-p-`: portas **1 a 65535**. A **porta 0** só entra se for pedida explicitamente: *"Scanning port zero is allowed if you specify it explicitly."* **[CONFIRMADO]** — https://nmap.org/book/man-port-specification.html
- `-F` (fast): **100** portas. `--top-ports <n>`: as n portas de maior razão em `nmap-services`. Sintaxe de `-p` aceita faixas, qualificadores de protocolo (`T:`, `U:`, `S:`, `P:`) e nomes de serviço com curinga. **[CONFIRMADO]** — https://nmap.org/book/man-port-specification.html

### 2.5 `-T0` a `-T5` — barulho e duração

Nomes: T0 paranoid, T1 sneaky, T2 polite, T3 normal (padrão), T4 aggressive, T5 insane. **[CONFIRMADO]** — https://nmap.org/book/performance-timing-templates.html

| Template | Comportamento documentado |
|---|---|
| **T0** | Serializa a varredura (uma porta por vez) e **espera 5 minutos entre cada probe** — *"serializing the scan so only one port is scanned at a time, and waiting five minutes between sending each probe"*. **[CONFIRMADO]** https://nmap.org/book/man-performance.html |
| **T1** | Delay de **15 s** entre probes; também serial. **[CONFIRMADO]** https://nmap.org/book/man-performance.html |
| **T2** | Delay de **0,4 s** (400 ms); pode levar **~10× mais tempo** que a varredura padrão. **[CONFIRMADO]** https://nmap.org/book/performance-timing-templates.html |
| **T3** | Padrão, com paralelização dinâmica. **[CONFIRMADO]** https://nmap.org/book/man-performance.html |
| **T4** | `--max-rtt-timeout 1250ms --min-rtt-timeout 100ms --initial-rtt-timeout 500ms --max-retries 6` + teto de scan delay TCP/SCTP de **10 ms**. **[CONFIRMADO]** https://nmap.org/book/man-performance.html |
| **T5** | `--max-rtt-timeout 300ms --min-rtt-timeout 50ms --initial-rtt-timeout 250ms --max-retries 2 --host-timeout 15m --script-timeout 10m` + teto de scan delay de **5 ms**. **[CONFIRMADO]** https://nmap.org/book/man-performance.html |

- T0-T2 usam `max-parallelism 1` (probes em série); T3+ usam paralelismo dinâmico. **[CONFIRMADO]** — https://nmap.org/book/performance-timing-templates.html
- T0 e T1 existem para **evasão de IDS**; T5 *"assumes you are on an extraordinarily fast network or are willing to sacrifice some accuracy for speed."* **[CONFIRMADO]** — https://nmap.org/book/performance-timing-templates.html
- Efeito real no barulho: o que muda é **taxa de pacotes por segundo e concorrência**, não o conteúdo dos pacotes. T0/T1 reduzem chance de disparar limiar de detecção por volume, ao custo de horas ou dias; T4/T5 aumentam risco de **falsos "filtered"** por timeout e perda. **[CONSOLIDADO]** a partir das tabelas de timeouts/retries acima.

### 2.6 Os seis estados de porta (definições literais)

- **open**: *"An application is actively accepting TCP connections, UDP datagrams or SCTP associations on this port."*
- **closed**: *"A closed port is accessible (it receives and responds to Nmap probe packets), but there is no application listening on it."*
- **filtered**: *"Nmap cannot determine whether the port is open because packet filtering prevents its probes from reaching the port."*
- **unfiltered**: *"The unfiltered state means that a port is accessible, but Nmap is unable to determine whether it is open or closed."*
- **open|filtered**: *"Nmap places ports in this state when it is unable to determine whether a port is open or filtered."*
- **closed|filtered**: *"This state is used when Nmap is unable to determine whether a port is closed or filtered."*

Todas **[CONFIRMADO]** — https://nmap.org/book/man-port-scanning-basics.html

Leitura operacional: `closed` prova que o host respondeu (host vivo, sem serviço ali); `filtered` prova que **algo no caminho** interferiu — não prova ausência de serviço. **[CONSOLIDADO]**

---

## 3. A saída do Nmap — o que cada coluna prova

- Colunas: **PORT** (número/protocolo), **STATE** (um dos seis estados), **SERVICE**, e, com detecção de versão, **VERSION** — *"A new VERSION column provides the application name and version details for the listening service. This comes from service detection, one of the features enabled by the -A option."* **[CONFIRMADO]** — https://nmap.org/book/port-scanning-tutorial.html
- O ponto central sobre a coluna SERVICE, literal: *"Another feature of service detection is that all of the service protocols in the SERVICE column have actually been verified. In the previous scan, they were based on the relatively flimsy heuristic of an nmap-services port number lookup. That table lookup happened to be correct this time, but it won't always be."* **[CONFIRMADO]** — https://nmap.org/book/port-scanning-tutorial.html
- Ou seja: **sem `-sV`, a linha de serviço não prova nada sobre o software** — é tradução do número da porta pela tabela `nmap-services` (base de mais de 2.200 serviços conhecidos). **[CONFIRMADO]** — https://nmap.org/book/vscan.html
- Linhas de resumo do tipo `Not shown: 994 filtered ports` / `Not shown: 65530 filtered ports` indicam portas omitidas por estarem todas no mesmo estado ignorado. **[CONFIRMADO]** (ocorrências no texto) — https://nmap.org/book/port-scanning-tutorial.html
- Formatos de saída: interativo, normal `-oN`, XML `-oX`, grepable `-oG` (campos Host, Status, Ports, Protocols, Ignored State, OS, Seq Index, IP ID Seq), script kiddie `-oS`. **[CONFIRMADO]** — https://nmap.org/book/output.html
- Com `-sV`, o que a linha prova é: **um serviço respondeu a um probe de forma compatível com a assinatura X**. Banner e assinatura podem ser alterados pelo administrador; o que a versão detectada dá é hipótese forte, não inventário autoritativo. **[CONSOLIDADO]** (base: mecanismo de match por probe/resposta descrito em https://nmap.org/book/man-version-detection.html)

---

## 4. Gobuster e ffuf

### 4.1 Gobuster — modos

Modos do binário oficial: **dir** (diretórios/arquivos em servidor web), **dns** (enumeração de subdomínio por resolução), **vhost** (virtual hosts), **fuzz** (fuzzing genérico com keyword), **s3**, **gcs**, **tftp**. **[CONFIRMADO]** — https://github.com/OJ/gobuster (README) e árvore `cli/` em https://github.com/OJ/gobuster/tree/v3.8.2/cli

### 4.2 Gobuster — flags que importam (v3.8.2, texto do código-fonte)

Globais (`cli/options.go`): **[CONFIRMADO]** — https://github.com/OJ/gobuster/blob/v3.8.2/cli/options.go
- `--wordlist, -w` — *"Path to the wordlist. Set to - to use STDIN."* (**obrigatória**)
- `--threads, -t` — padrão **10**
- `--delay, -d` — *"Time each thread waits between requests (e.g. 1500ms)"* ⚠️ nesta versão `-d` é **delay**, não domínio
- `--no-tls-validation, -k`, `--proxy`, `--timeout/-to` (10 s HTTP), `--output/-o`, `--quiet/-q`, `--pattern/-p`
- HTTP comuns: `--url/-u` (obrigatória), `--cookies/-c`, `--username/-U`, `--password/-P`, `--follow-redirect/-r`, `--headers/-H`, `--method/-m` (padrão GET)

Modo `dir` (`cli/dir/dir.go`): **[CONFIRMADO]** — https://github.com/OJ/gobuster/blob/v3.8.2/cli/dir/dir.go
- `--status-codes, -s` — *"Positive status codes (will be overwritten with status-codes-blacklist if set)"* — **vazio por padrão**
- `--status-codes-blacklist, -b` — **padrão `"404"`** — *"Negative status codes (will override status-codes if set)"*
- Só um dos dois pode estar setado; se ambos, erro explícito: *"status-codes (%q) and status-codes-blacklist (%q) are both set - please set only one. status-codes-blacklist is set by default so you might want to disable it by supplying an empty string"*
- `--extensions/-x`, `--extensions-file/-X`, `--expanded/-e`, `--no-status/-n`, `--hide-length/-hl`, `--add-slash/-f`, `--discover-backup/-db`, `--exclude-length/-xl`, `--force`
- **Consequência do modelo:** o padrão do gobuster dir é *mostrar tudo que não seja 404* — ele **não** é uma allowlist de 200. **[CONFIRMADO]** pelo valor default acima.

Modo `dns` (`cli/dns/dns.go`, v3.8.2): **[CONFIRMADO]** — https://github.com/OJ/gobuster/blob/v3.8.2/cli/dns/dns.go
- `--domain, -do` (**obrigatória**) — atenção: alias curto é `do`
- `--check-cname, -c`, `--timeout/-to` (1 s), `--wildcard/-wc` (*"Force continued operation when wildcard found"*), `--no-fqdn/-nf`, `--resolver`, `--protocol` (udp/tcp no resolver custom)
- Em versões **≤ v3.6** o mesmo modo usava `-d/--domain`, `-i/--show-ips`, `-c/--show-cname`, `-r/--resolver`. **[CONFIRMADO]** — https://github.com/OJ/gobuster/blob/v3.6.0/cli/cmd/dns.go

Modo `vhost` (`cli/vhost/vhost.go`, v3.8.2): **[CONFIRMADO]** — https://github.com/OJ/gobuster/blob/v3.8.2/cli/vhost/vhost.go
- `--append-domain, -ad` — *"Append main domain from URL to words from wordlist. Otherwise the fully qualified domains need to be specified in the wordlist."*
- `--exclude-length, -xl`, `--exclude-status, -xs`, `--exclude-hostname-length, -xh` (*"Automatically adjust exclude-length based on dynamic hostname length in responses"*, exige `--exclude-length`), `--domain/-do`
- Mecânica: o vhost varia o cabeçalho **Host** contra o mesmo IP; como o servidor responde 200 para quase tudo, a separação de achado vem de **tamanho/estado da resposta**, não do código. **[CONSOLIDADO]** a partir das flags de exclusão acima.

### 4.3 ffuf — conceito e defaults (v2.2.1, código-fonte)

- Palavra-chave **FUZZ**: *"To define the test case for ffuf, use the keyword `FUZZ` anywhere in the URL (-u), headers (-H), or POST data (-d)."* **[CONFIRMADO]** — https://github.com/ffuf/ffuf#usage
- Casos canônicos do README: diretório `-w list -u https://target/FUZZ`; **vhost** `-u https://target -H "Host: FUZZ" -fs 4242`; parâmetro GET `-u "https://target/script.php?FUZZ=test_value" -fs 4242`. **[CONFIRMADO]** — https://github.com/ffuf/ffuf#usage
- **Matcher padrão de status: `200-299,301,302,307,401,403,405,500`** (`c.Matcher.Status`). **[CONFIRMADO]** — https://github.com/ffuf/ffuf/blob/v2.2.1/pkg/ffuf/optionsparser.go
- Outros defaults confirmados no mesmo arquivo: `Threads = 40`, `HTTP.Timeout = 10` s, `Rate = 0` (sem limite), `Recursion = false`, `RecursionDepth = 0`, `InputMode = "clusterbomb"`, `Filter.Mode = "or"`, `Matcher.Mode = "or"`, `AutoCalibration = false` com keyword `FUZZ`. **[CONFIRMADO]**
- Matchers: `-mc` (status ou `all`), `-ms` (size), `-ml` (lines), `-mw` (words), `-mr` (regex), `-mt` (tempo até o primeiro byte, `>100`/`<100`). Filtros espelhados: `-fc -fs -fl -fw -fr -ft`. **[CONFIRMADO]** — https://github.com/ffuf/ffuf/blob/v2.2.1/main.go
- Outros: `-ac` (autocalibração de filtros), `-recursion`, `-recursion-depth`, `-rate`, `-t`, `-maxtime`, `-se` (para em erros espúrios), `-sf` (*"Stop when > 95% of responses return 403 Forbidden"*), múltiplas wordlists com `-w arquivo:KEYWORD` e `-mode clusterbomb|pitchfork|sniper`. **[CONFIRMADO]** — https://github.com/ffuf/ffuf/blob/v2.2.1/main.go e README
- **Regra de precedência não óbvia (lida no código):** em `SetupFilters`, se você define **qualquer** matcher que não seja `-mc` (`-ms`, `-ml`, `-mr`, `-mt`, `-mw`) e **não** define `-mc`, o matcher de status padrão **é desligado** — comentário literal do código: *"If any other matcher is set, ignore -mc default value"*, e a condição `if statusSet || !matcherSet`. **[CONFIRMADO]** — https://github.com/ffuf/ffuf/blob/v2.2.1/main.go

### 4.4 Papel da wordlist

- Ambos os tools são **adivinhação por lista**: o universo de achados é exatamente o conteúdo da wordlist (mais transformações como extensões `-x` no gobuster ou keywords no ffuf). Nenhum dos dois descobre nome que não esteja na lista. **[CONFIRMADO]** pelo fato de `-w` ser obrigatória e a mecânica de substituição de keyword — https://github.com/OJ/gobuster/blob/v3.8.2/cli/options.go e https://github.com/ffuf/ffuf#usage
- Portanto "não achou" significa "não estava na lista **ou** não passou no filtro configurado", nunca "não existe". **[CONSOLIDADO]**

### 4.5 Por que filtrar só 200 perde achado — e o que 401/403 revelam

- Os defaults dos dois tools já contradizem o hábito de olhar só 200: gobuster dir mostra tudo menos 404 (`-b "404"`) e ffuf casa `200-299,301,302,307,401,403,405,500`. **[CONFIRMADO]** (fontes em 4.2 e 4.3)
- Semântica HTTP (RFC 9110): **[CONFIRMADO]** — https://www.rfc-editor.org/rfc/rfc9110#section-15.5
  - **401 Unauthorized**: *"the request lacks valid authentication credentials for the target resource"*, e a resposta *"MUST send a WWW-Authenticate header field containing at least one challenge applicable to the target resource."*
  - **403 Forbidden**: *"The server understood the request but refuses to fulfill it."* E o ponto decisivo: *"If the server does not wish to make the refusal reason public, the server can instead respond with a 404 status code."*
  - **404 Not Found**: *"The origin server did not find a current representation for the target resource or is unwilling to disclose that one exists."*
- Leitura: **401 e 403 confirmam que o caminho existe e está protegido** — um recurso autenticado ou negado é um achado, muitas vezes mais valioso que um 200 de página pública. Um 301/302 revela diretório real (redirecionamento para versão com `/`), e 405 revela endpoint que existe mas rejeita o método. Um 500 revela caminho que chega a código e quebra. Filtrar só 200 apaga toda essa camada. **[CONSOLIDADO]** com base nas definições da RFC 9110 e nos defaults dos tools
- O inverso também vale: como a RFC permite responder **404 no lugar de 403**, a ausência de 403 **não** prova ausência de recurso. **[CONFIRMADO]** (mesma citação de 15.5.4)
- Por isso os tools oferecem filtro por **tamanho/linhas/palavras** (`-fs/-fl/-fw`, `--exclude-length`) e autocalibração `-ac`: em alvos que devolvem 200 para tudo (soft-404, SPA, wildcard), o código de status é inútil como discriminador. **[CONFIRMADO]** (flags citadas acima)

---

## 5. Enumeração de DNS

### 5.1 Tipos de registro (definições normativas)

RFC 1035 §3.2.2, texto literal dos tipos: **[CONFIRMADO]** — https://www.rfc-editor.org/rfc/rfc1035#section-3.2.2
- **A** (1) — *"a host address"*
- **NS** (2) — *"an authoritative name server"*
- **CNAME** (5) — *"the canonical name for an alias"*
- **SOA** (6) — *"marks the start of a zone of authority"*
- **PTR** (12) — *"a domain name pointer"*
- **MX** (15) — *"mail exchange"*
- **TXT** (16) — *"text strings"*

**AAAA** (28): *"The IANA assigned value of the type is 28 (decimal)"*, e *"A 128 bit IPv6 address is encoded in the data portion of an AAAA resource record in network byte order."* **[CONFIRMADO]** — https://www.rfc-editor.org/rfc/rfc3596

Valor de reconhecimento de cada um, em uma linha: A/AAAA dão o endereço (superfície de rede); NS dá quem é autoritativo (alvos e possível provedor); MX expõe o provedor de e-mail; TXT costuma carregar SPF/DKIM/verificações de serviços SaaS (revela fornecedores usados); CNAME revela hospedagem terceirizada e é o vetor clássico de subdomínio órfão; SOA dá o servidor primário e os parâmetros da zona. **[CONSOLIDADO]** sobre as definições acima.

### 5.2 Transferência de zona (AXFR) e por que quase sempre falha hoje

RFC 5936: **[CONFIRMADO]** — https://www.rfc-editor.org/rfc/rfc5936
- AXFR transfere a **zona inteira** e roda sobre **TCP** (citando RFC 1034 §4.3.5: *"Because accuracy is essential, TCP or some other reliable protocol must be used for AXFR requests."*).
- Formato: *"the first message MUST begin with the SOA resource record of the zone, and the last message MUST conclude with the same SOA resource record."*
- Autorização: *"A zone administrator has the option to restrict AXFR access to a zone."* Implementações devem suportar controle por **TSIG** e/ou **SIG(0)**, e *"SHOULD allow access to be granted to Internet Protocol addresses and ranges."*
- E o ponto que explica o fracasso quase universal do AXFR anônimo hoje: implementações *"SHOULD NOT have a default policy for AXFR requests to be 'open to all'."* **[CONFIRMADO]**
- Consequência: um AXFR recusado é **o comportamento esperado e correto**, não um erro do operador. Quando ele funciona contra um servidor público, isso é o achado (má configuração), porque entrega a zona toda de uma vez, sem adivinhação. **[CONSOLIDADO]**

### 5.3 Força bruta de subdomínio × transparência de certificado (CT)

- **Força bruta** (gobuster dns, ffuf com `Host:`/FUZZ no nome): consulta o resolvedor para cada palavra da lista; acha **apenas** o que está na lista; gera volume de consultas DNS; é enganada por **wildcard DNS**. **[CONFIRMADO]** para a mecânica e para a existência de detecção de wildcard — https://github.com/OJ/gobuster/blob/v3.8.2/cli/dns/dns.go
- **Wildcard**, definição normativa: *"Wildcard RRs can be thought of as instructions for synthesizing RRs. When the appropriate conditions are met, the name server creates RRs with an owner name equal to the query name and contents taken from the wildcard RRs."* **[CONFIRMADO]** — https://www.rfc-editor.org/rfc/rfc4592 — ou seja, com `*.exemplo.com` **qualquer** palavra da wordlist "resolve", e a lista de achados vira lixo se a detecção de wildcard for ignorada.
- **Certificate Transparency** (RFC 6962): logs **públicos e append-only** de certificados emitidos; *"those who are concerned about misissue can monitor the logs, asking them regularly for all new entries, and can thus check whether domains they are responsible for have had certificates issued"*, e *"Log operators MUST NOT impose any conditions on retrieving or sharing data from the log."* **[CONFIRMADO]** — https://www.rfc-editor.org/rfc/rfc6962
- Diferença operacional: CT é consulta a um **registro público de terceiros** — nenhum pacote é enviado ao alvo, e retorna nomes reais (inclusive históricos e hosts internos que receberam certificado por engano). Força bruta toca o DNS do alvo/resolvedor e só acha o que foi imaginado. **[CONSOLIDADO]** a partir da RFC 6962
- Limites do CT: só aparece o que **recebeu certificado publicamente confiável**; host sem TLS, com certificado interno próprio, ou coberto por um curinga `*.exemplo.com` **não** aparece nominalmente. Por isso os dois métodos são complementares, não substitutos. **[CONSOLIDADO]**
- Interfaces práticas de consulta a CT (ex.: https://crt.sh) são serviços de terceiros sobre esses logs, não parte da RFC. **[CONSOLIDADO]**

---

## 6. Lado defensivo: o que a varredura deixa, o que o IDS vê, o que realmente reduz superfície

### 6.1 O que fica em log

- Logs de host capturam conexões TCP completas quando a aplicação as registra; *"the default Nmap SYN scan sneaks through"* esses logs, porque não completa conexões. **[CONFIRMADO]** — https://nmap.org/book/nmap-defenses-detection.html
- Connect scan (`-sT`) é o oposto: *"Many services on your average Unix system will add a note to syslog… when Nmap connects and then closes the connection without sending data."* **[CONFIRMADO]** — https://nmap.org/book/man-port-scanning-techniques.html
- Realidade operacional citada pela própria doc: *"the vast majority of log messages go forever unread"* — gerar log não é o mesmo que ser detectado. **[CONFIRMADO]** — https://nmap.org/book/nmap-defenses-detection.html

### 6.2 Como um IDS reconhece a varredura

- Detectores dedicados de port scan (PortSentry, Scanlogd) são mais eficazes do que só log; Scanlogd *"has been around since 1998 and was carefully designed for security."* **[CONFIRMADO]** — https://nmap.org/book/nmap-defenses-detection.html
- Snort traz *"more than two thousand rules for detecting all sorts of suspicious activity, including port scans"*, mas *"a skilled attacker can defeat most IDS rules, so do not let your guard down."* **[CONFIRMADO]** — https://nmap.org/book/nmap-defenses-detection.html
- Todos os IDS grandes trazem regras feitas para pegar varreduras do Nmap. **[CONFIRMADO]** — https://nmap.org/book/firewalls.html (Cap. 10)
- Mesmo o SYN scan "furtivo" é detectável: *"widely deployed intrusion detection systems and even personal firewalls are quite capable of detecting default SYN scans."* **[CONFIRMADO]** — https://nmap.org/book/synscan.html
- O sinal que um IDS usa é **padrão de volume e dispersão** (muitos destinos/portas a partir de uma origem em pouco tempo); é exatamente esse limiar que `-T0`/`-T1` e `--scan-delay` tentam ficar abaixo — pagando com horas ou dias de duração. **[CONSOLIDADO]** a partir de https://nmap.org/book/performance-timing-templates.html (T0 = 5 min por probe, T1 = 15 s) e https://nmap.org/book/nmap-defenses-detection.html

### 6.3 O que reduz superfície de verdade × o que só esconde

- Desligar o serviço vence filtrar: *"A closed port is a much smaller risk than an open one"*, e *"unnecessary services should be disabled"*; serviços que o público não precisa alcançar devem ser bloqueados no firewall. **[CONFIRMADO]** — https://nmap.org/book/nmap-defenses-proactive-scanning.html
- Corrigir vence esconder: *"Fixing a hole is far more effective than trying to hide it. That approach is also less stressful than constantly worrying that attackers may find the vulnerabilities."* **[CONFIRMADO]** — https://nmap.org/book/nmap-defenses-proactive-scanning.html
- Auditoria é rotina, não evento: *"Proactive network scanning and auditing should become a routine rather than a one-off audit."* **[CONFIRMADO]** — https://nmap.org/book/nmap-defenses-proactive-scanning.html
- Sobre obscuridade, o próprio capítulo de defesas avisa: *"Obfuscating your network to the extent that attackers cannot understand what is going on is not a net win if your administrators no longer understand it either"*, e ferramentas defensivas não compensam se abrirem vulnerabilidade pior. **[CONFIRMADO]** — https://nmap.org/book/defenses.html
- **Mudar a porta padrão não reduz superfície**: o serviço continua alcançável, e `-p-` (1-65535) mais `-sV` identificam o serviço pelo comportamento da resposta, não pelo número da porta. Muda apenas o custo/tempo do atacante — e, na parte defensiva, o custo do inventário próprio. **[CONSOLIDADO]** a partir de https://nmap.org/book/man-port-specification.html e https://nmap.org/book/man-version-detection.html
- Escala de eficácia real, do mais forte ao mais fraco: **remover/desligar o serviço** > **filtrar no firewall / segmentar a rede** (o alvo passa a `filtered`, as probes nem chegam) > **exigir autenticação** > **mudar a porta padrão** (só obscuridade). **[CONSOLIDADO]**, apoiado nas definições de `filtered` (https://nmap.org/book/man-port-scanning-basics.html) e nas recomendações de https://nmap.org/book/nmap-defenses-proactive-scanning.html

---

## ARMADILHAS

Erros que aparecem com frequência em material sobre varredura, e a correção conforme a documentação acima.

1. **"-sS é invisível / não deixa rastro."** Falso. Ele evita o log **da aplicação**, não a detecção: *"intrusion detection systems and even personal firewalls are quite capable of detecting default SYN scans"* (https://nmap.org/book/synscan.html). Diga "não completa a conexão, então em geral não entra no log do serviço", nunca "é indetectável".
2. **"-sT é o scan furtivo."** Invertido. `-sT` completa a conexão e é o que mais gera log em syslog (https://nmap.org/book/man-port-scanning-techniques.html).
3. **"-sS precisa de root porque é mais rápido."** Não. Precisa porque monta e lê **pacotes crus**; sem esse privilégio o Nmap cai para connect scan automaticamente (mesma fonte). No Windows isso significa driver de captura (Npcap).
4. **"UDP fechado = sem resposta."** Invertido. **Sem resposta ⇒ `open|filtered`**; **ICMP type 3 code 3 ⇒ `closed`**. E `filtered` em UDP são os *outros* códigos do type 3 (0,1,2,9,10,13) (https://nmap.org/book/man-port-scanning-techniques.html).
5. **"UDP é lento porque UDP é ruim."** A causa documentada é **rate limit de ICMP port unreachable** no alvo (Linux: 1/s), o que faz 65.536 portas passarem de 18 horas (mesma fonte). Sem essa explicação, o número vira folclore.
6. **"O Nmap escaneia as portas 1-1000 por padrão."** Não: são as **1.000 portas mais comuns** por protocolo, segundo o ranking de `nmap-services` — conjunto que inclui portas altas (https://nmap.org/book/man-port-specification.html). E `-p-` é 1-65535: **a porta 0 só entra se pedida explicitamente**.
7. **"-Pn deixa o scan mais discreto."** Não. Ele **pula a descoberta** e escaneia todo IP indicado, inclusive os inexistentes — mais pacotes, mais tempo (https://nmap.org/book/host-discovery-controls.html). Ele serve contra alvos que ignoram probes de descoberta.
8. **"-sn só manda ping ICMP."** Privilegiado manda quatro probes (ICMP echo + SYN 443 + ACK 80 + ICMP timestamp), e ARP em rede local; **não privilegiado abre conexões TCP reais em 80 e 443** via `connect()` (mesma fonte). Bloquear ICMP não esconde o host.
9. **"A coluna SERVICE diz o que está rodando."** Só com `-sV`. Sem ele é *"the relatively flimsy heuristic of an nmap-services port number lookup"* — e a doc completa: *"it won't always be"* correto (https://nmap.org/book/port-scanning-tutorial.html).
10. **"-O identifica o SO."** Ele **compara assinaturas de pilha TCP/IP** e imprime nível de confiança em percentual quando não há match exato (`--osscan-guess`), e funciona muito melhor com **uma porta aberta e uma fechada** (https://nmap.org/book/man-os-detection.html). Trate como hipótese, nunca como fato de inventário.
11. **"filtered = porta fechada."** Não. `closed` é resposta ativa do host sem serviço escutando; `filtered` é "as probes não chegaram / não voltaram, algo filtra no caminho" (https://nmap.org/book/man-port-scanning-basics.html). Só existem seis estados — `open|filtered` e `closed|filtered` são estados legítimos, não erro de leitura.
12. **"-T5 é sempre melhor quando tenho pressa."** T5 corta `--max-retries` para 2 e `--max-rtt-timeout` para 300 ms, e a doc diz que assume rede extraordinariamente rápida *"or are willing to sacrifice some accuracy"* (https://nmap.org/book/man-performance.html): o preço é **falso `filtered`** por timeout.
13. **"-T0 é só 'mais devagar'."** T0 é serial com **5 minutos entre cada probe** (T1 = 15 s). Uma varredura de mil portas em T0 é medida em dias, não minutos (mesma fonte). Nunca sugira `-T0` sem dizer a duração.
14. **"-sC/--script é seguro por padrão."** A categoria `default` inclui scripts considerados intrusivos, e o manual afirma que scripts *"are not run in a sandbox"* (https://nmap.org/book/man-nse.html). `-A` liga `-sC` junto com `-O`, `-sV` e `--traceroute` — quem usa `-A` está rodando scripts sem perceber.
15. **"gobuster dir só mostra 200 por padrão."** Falso: o padrão é **blacklist `404`** (`-b "404"`), com `-s` vazio; setar os dois é erro fatal do tool (https://github.com/OJ/gobuster/blob/v3.8.2/cli/dir/dir.go).
16. **"gobuster dns -d dominio.com".** Depende da versão: em **v3.7+/v3.8.2** é `--domain` com alias **`-do`**, e **`-d` virou `--delay`** — o comando antigo falha ou faz outra coisa. `-i/--show-ips` não existe mais nessa linha; o de CNAME virou `--check-cname/-c` (https://github.com/OJ/gobuster/blob/v3.8.2/cli/dns/dns.go × https://github.com/OJ/gobuster/blob/v3.6.0/cli/cmd/dns.go). Sempre diga a versão junto da flag.
17. **"ffuf mostra tudo se eu passar `-ms`, `-ml` ou `-mw`."** Ao contrário: definir qualquer matcher que não seja `-mc` **desliga o matcher de status padrão** (*"If any other matcher is set, ignore -mc default value"*, https://github.com/ffuf/ffuf/blob/v2.2.1/main.go). Combine com `-mc all` quando quiser os dois critérios.
18. **"403 significa que não tem nada ali."** A RFC 9110 diz o contrário: 403 é *"understood the request but refuses to fulfill it"*, e o servidor que **não quer** revelar pode responder 404 no lugar (https://www.rfc-editor.org/rfc/rfc9110#section-15.5). 401 vem com `WWW-Authenticate` e prova recurso protegido. Filtrar só 200 descarta 301/302/401/403/405/500 — a parte mais informativa.
19. **"Alvo que responde 200 para tudo quebra o brute force."** Quebra o filtro **por status**; a saída é filtrar por tamanho/linhas/palavras (`-fs/-fl/-fw`, `--exclude-length`) ou usar `-ac` (autocalibração) — recursos que existem exatamente para isso (fontes em 4.2/4.3).
20. **"Nenhum achado = não existe."** Achado é limitado pela **wordlist** e pelos filtros; `-w` é obrigatória nos dois tools. Reporte sempre "não encontrado com esta lista e estes filtros".
21. **"AXFR falhou, errei o comando."** Recusar AXFR anônimo é o comportamento **recomendado pela norma**: implementações *"SHOULD NOT have a default policy for AXFR requests to be 'open to all'"*, com controle por TSIG/SIG(0) e ACL de IP (https://www.rfc-editor.org/rfc/rfc5936). Sucesso do AXFR é que é o achado.
22. **"Wildcard DNS não atrapalha."** Com `*.exemplo.com` o servidor **sintetiza** resposta para qualquer nome consultado (https://www.rfc-editor.org/rfc/rfc4592) — toda a wordlist "resolve". Por isso o gobuster tem detecção de wildcard e exige `--wildcard/-wc` para continuar.
23. **"CT substitui a força bruta."** CT só lista o que **recebeu certificado publicamente confiável**; host sem TLS público ou coberto por curinga não aparece nominalmente. E, ao contrário do brute force, consultar CT **não envia pacote ao alvo** (https://www.rfc-editor.org/rfc/rfc6962). São complementares.
24. **"Mudar a porta do SSH resolve."** Não reduz superfície: `-p-` mais `-sV` identificam o serviço pela resposta, não pelo número. O capítulo de defesas do Nmap coloca a obscuridade abaixo de fechar, filtrar e corrigir — *"A closed port is a much smaller risk than an open one"* e *"Fixing a hole is far more effective than trying to hide it"* (https://nmap.org/book/nmap-defenses-proactive-scanning.html).
25. **"Se aparece no log, foi detectado."** *"the vast majority of log messages go forever unread"* (https://nmap.org/book/nmap-defenses-detection.html). Detecção exige detector dedicado ou IDS com regra e alguém lendo o alerta.
26. **Escopo e autorização.** Todo comando neste material atinge sistemas de terceiros. O próprio manual condiciona o uso de scripts default a permissão do alvo (https://nmap.org/book/man-nse.html). Qualquer exemplo publicado deve usar alvo próprio ou laboratório explicitamente autorizado.
27. **Nada aqui foi executado.** O Nmap não está instalado na máquina do usuário: sintaxe, defaults e comportamentos deste documento vêm da documentação e do código-fonte das versões citadas (Nmap Reference Guide, Gobuster v3.8.2, ffuf v2.2.1). Ao publicar, fixe a versão junto da flag — foi exatamente aí que gobuster e ffuf mudaram.
