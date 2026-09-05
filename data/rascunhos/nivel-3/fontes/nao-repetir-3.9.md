# Levantamento de não-repetição — engenharia social × redes sem fio

## Método

Contagem de menções por palavra/frase-chave (regex com fronteira de palavra,
acento normalizado), varrendo `teoria` e `questoes` dos 34 módulos
publicados. Toda ocorrência relevante foi lida em contexto, não só contada
— a primeira rodada de busca (substring solta) deu falso positivo grosso
("bec" batendo em "cabeçalho", "rf" batendo em qualquer trecho com essas
duas letras) e foi descartada antes de qualquer conclusão.

---

## Engenharia social — território pesado, com dono forte

| termo | módulos com menção real |
|---|---|
| engenharia social | 0.1(1), 0.2(3), 0.3(1), 0.4(4), 2.4(1), 2.7(3), 3.7(3), 4.7(2) |
| phishing | 0.1(5), 0.2(7), 0.3(6), 1.3(1), 1.4(3), 1.5(16), 2.5(11), 2.7(21) |
| pretexto/pretexting | 0.4(1), 2.7(3) |
| tailgating | 2.7(5) |
| BEC (fraude de e-mail corporativo) | 2.7(10) |
| urgência (gatilho de persuasão) | 1.7(3), 2.7(2), 3.1(1), 4.1(3), 4.7(3) |
| fator humano | 2.7(1) |
| vishing / smishing / whaling / deepfake / clonagem de voz | **zero, em qualquer módulo** |

**Achado central: o módulo 2.7 ("Fator humano — por que a segurança falha
nas pessoas") já é, para todos os efeitos, um módulo de engenharia social
completo**, com 35 questões e quatro objetivos declarados:

- obj. 1: "reconhecer e nomear os gatilhos de persuasão e os vieses
  cognitivos que os ataques exploram"
- obj. 2: "analisar phishing, pretexting e fraude de e-mail corporativo:
  sinais reais e defesa que é mecanismo, não vigilância"

Teoria: `2.7.t3` cobre autoridade/conformidade (Asch, Milgram, o trote
telefônico de 1995-2005) e responsabilidade difusa; `2.7.t4` é "o catálogo
de vieses que o golpe usa"; `2.7.t5`, título literal "**Persuasão
profissional, engenharia social e phishing**", cobre as seis técnicas de
Cialdini, os sete princípios de Stajano e Wilson, a definição de
pretexting com caso real (HP 2006), e a definição de BEC; `2.7.t7` cobre
autenticação de e-mail (SPF/DKIM/DMARC) como defesa técnica contra
phishing/BEC.

**Tailgating não é menção de passagem — já tem questão própria**
(`2.7.q26`, verificado no arquivo): cenário de empresa que quer acabar com
"entradas coladas" sem instalar catraca, com explicação de por que
tailgating funciona (educação social, não ingenuidade) e o que faz uma
regra pegar. O vetor físico mais óbvio de engenharia social já está coberto
com mecanismo e defesa, não só citado.

As outras menções de "phishing" (1.5, 2.5) são tangenciais e não competem:
1.5 usa phishing como exemplo do porquê "procure o cadeado" é orientação
morta (a maioria dos sites de phishing tem HTTPS válido) — ponto sobre TLS,
não sobre engenharia social; 2.5 usa phishing como argumento para
autenticação resistente a phishing (FIDO2/passkey vs. MFA por código) —
ponto sobre modelo de autenticação. 0.1–0.4 introduzem o conceito em nível
de alicerce, sem mecanismo. `1.1` e `4.4` (indicados pelo usuário como
possíveis pontos de toque) **não mencionam** engenharia social, phishing,
pretexto nem vetor humano em lugar nenhum do arquivo — busca ampla, zero
ocorrência.

### O que sobra de fato livre

Sobra pouco do "o que é e como reconhecer" — isso é 2.7. O que **não**
existe em nenhum módulo:

1. **A engenharia social como teste autorizado**, não como golpe sofrido: o
   que muda quando o alvo do pentest é uma pessoa, não um sistema —
   consentimento específico para vetor humano (proteger o funcionário
   individual, não só a organização), princípio de "sem culpa" no relato
   (quem clicou não é o achado, o controle que faltou é), e por que
   "taxa de clique" sozinha é métrica ruim de sucesso. **Risco de colisão
   com 3.1** (que já possui objetivo 1 "fechar escopo, janela e regras de
   engajamento" e `3.1.t4`/`t5` de pré-engajamento e regras de
   engajamento) — só se sustenta como eixo próprio se ficar estritamente no
   que é **específico de alvo humano**, não regra de engajamento genérica
   já ensinada.
2. **Reconhecimento aplicado a pretexto**: 3.2 (OSINT) já ensina a
   levantar informação sobre uma organização; nenhum módulo conecta esse
   levantamento à construção de um pretexto crível (organograma, nome de
   fornecedor, jargão interno). Eixo de **aplicação cruzada**, não de
   mecanismo novo — precisa ficar claramente subordinado a 3.2, não
   reensinar OSINT.
3. **Vishing e engenharia social por voz, incluindo o risco de clonagem de
   voz** — zero menção em qualquer módulo. Território livre de verdade, mas
   fino como eixo isolado.
4. **Métricas e desenho de campanha de simulação de phishing** — como
   medir sem punir indivíduo, como fechar o ciclo com treinamento
   direcionado — extensão natural de `2.7.t2` ("erro humano é previsível,
   logo é projetável"), mas do lado de quem desenha o programa, não de
   quem é o alvo.

**Diagnóstico**: sobra território real, mas ele é estreito e concentrado em
"como avaliar/testar", não em "o que é e como funciona" — o mesmo tipo de
aperto que o 3.7 (OWASP Top 10) enfrentou com sete das dez categorias já
possuídas, e que só foi resolvido lá com uma reformulação de eixo forte
("a lista como instrumento", não as categorias em si). Aqui a reformulação
equivalente seria algo como "engenharia social como o que se testa e como
se testa, não como o que engana" — viável, mas mais apertada que a do 3.7:
lá sobravam 2 de 10 categorias inteiras livres; aqui sobra um recorte fino
de processo, não um pedaço de conteúdo inteiro.

---

## Redes sem fio — território quase inteiramente livre

| termo | módulos com menção real |
|---|---|
| Wi-Fi / WPA / WEP / 802.11 / evil twin / deauth / Bluetooth / KRACK / rogue AP / beacon | **zero, em qualquer módulo** |
| SSID | zero como mecanismo (não apareceu no scan limpo — as ocorrências da varredura suja eram todas ruído de outras palavras) |
| "rede sem fio" / "wireless" (menção genérica) | 0.1(2), 1.4(3) |
| "ponto de acesso" (uso genérico, não WiFi) | 0.2(1), 1.5(1) |
| handshake | 1.5(24), 2.2(4) — **falso alvo**: é handshake de TLS/TCP, confirmado lendo o contexto (`1.5.t?` descreve literalmente "o handshake do TLS 1.3"), sem nenhuma relação com WPA/rede sem fio |

Toda menção genuína de "rede sem fio" no corpus é um exemplo de superfície
de ataque citado de passagem, nunca mecanismo: `0.1` usa "rede sem fio da
clínica com senha compartilhada com pacientes" como item de uma lista de
riscos; `1.4` usa "rede sem fio" como uma categoria de sintoma de rede
(ao lado de cabo e porta de switch) e como distrator numa questão sobre
endereço IP vs. endereço físico; `0.2` usa "ponto de acesso" no sentido de
"porta de entrada a dados corporativos", metáfora de negócio, não o
dispositivo de rede. 1.4 e 1.5 (indicados pelo usuário) tocam "rede" no
sentido amplo de camada de transporte/enlace, mas nenhum dos dois ensina
protocolo de rede sem fio, criptografia WPA, autenticação de rede sem fio
ou qualquer mecanismo específico do meio físico sem fio. 4.2 (Segurança de
rede) foi conferido especificamente e não cita nenhum dos termos de rede
sem fio da lista.

**Diagnóstico**: território inteiramente livre — mais livre até que o do
3.8 (quebra de senhas), que teve pelo menos parâmetros numéricos
compartilhados com 2.4/2.5 para navegar ao redor. Aqui não há nem
sobreposição de vocabulário, e sustenta um módulo padrão de 35 questões sem
esforço de reformulação: protocolo e criptografia (WEP→WPA2→WPA3, por que
cada geração quebrou a anterior), o handshake de autenticação real (WPA2
4-way handshake, distinto do handshake de TLS já ensinado em 1.5 — vale
inclusive uma referência cruzada explícita para não confundir os dois),
rede aberta vs. protegida e o que "protegida" garante e não garante, ponto
de acesso não autorizado (rogue AP) e evil twin como problema de confiança
de identidade de rede (eco temático de 3.8: "quebrado" não é o que parece),
ataque de desautenticação como negação de serviço direcionada, e Bluetooth
como superfície adicional de curto alcance.

---

## Recomendação

**Saída (b): dois módulos — 3.9 Engenharia social, 3.10 Redes sem fio —
mas com uma condição explícita para o 3.9.**

Redes sem fio sustenta um módulo padrão sem ressalva: território limpo,
35 questões honestas sem reformulação forçada. Não há debate aqui.

Engenharia social **não** sustenta um módulo com o recorte ingênuo
("o que é, como reconhecer, como phishing/pretexting/BEC funcionam") —
isso é 90% do que 2.7 já é, tailgating incluído com questão própria. Só
sustenta separado se o recorte for deliberadamente estreito e do lado da
**avaliação/teste autorizado**, não do lado de "como a pessoa é enganada":
consentimento e relato específicos de alvo humano (diferenciado de 3.1),
aplicação de OSINT a pretexto (subordinado a 3.2, não repetindo mecanismo),
vishing/voz/deepfake (livre, mas fino sozinho), e desenho/métrica de
campanha de simulação (extensão de 2.7.t2 do lado de quem constrói o
programa). É a mesma manobra que salvou o 3.7 — só que mais apertada, e
sem a garantia de que dá para preencher 35 questões honestas até a fase de
escrita de fato começar.

**Se, ao tentar montar os eixos concretos do 3.9 com esse recorte, o
território não render um número honesto de questões, a saída de fallback é
(c)**: publicar redes sem fio como módulo 3.9 padrão, e engenharia social
como um módulo mais curto que o padrão do projeto (exceção já com
precedente — 2.6 tem 5 objetivos em vez de 4, 2.7 tem 7 blocos de teoria em
vez de 6), documentada explicitamente no PROGRESS.md como decisão de
escopo, não como atalho de conveniência.

Não recomendo a saída (a) — não porque redes sem fio não caiba como bloco
menor dentro de outro módulo (caberia, tecnicamente), mas porque o
território de redes sem fio é bom demais para virar bloco secundário: é
exatamente o tipo de assunto autocontido, com mecanismo técnico próprio
(criptografia, protocolo, RF), que o curso trata como módulo inteiro em
todo o resto do nível 3.

---

## Adendo — decisão final e checagem de eixo contra 1.4/1.5/4.2

**Decisão do usuário**: variante do (c), sem enquadrar como corte. 3.9 é
Redes sem fio, módulo inteiro. Engenharia social não vira módulo — o item
do roadmap já está cumprido pelo 2.7 (ver PROGRESS.md, seção 5, "Decisão
de escopo"). Nível 3 fecha com 9 módulos (não 10).

Recorte proposto para 3.9 — por que o meio compartilhado muda o modelo de
ameaça, não catálogo de sigla de protocolo:

1. O meio é o ar: sem fronteira física, confidencialidade e autenticidade
   precisam ser resolvidas onde cabo resolvia por padrão.
2. Autenticar a rede, não só o cliente — por que ponto de acesso falso
   funciona (confiança unilateral, não senha fraca).
3. O que a evolução dos padrões resolveu, e o que fica fora por
   construção.
4. Corporativa × doméstica — por que o modelo de identidade muda quando
   cada usuário tem credencial própria.
5. Contraponto defensivo, fechando o módulo.

Checagem eixo a eixo contra 1.4 (endereçamento/NAT/DNS/DHCP), 1.5
(transporte/HTTP/TLS) e 4.2 (filtragem/detecção/segmentação/acesso) — os
três lidos por objetivo e título de teoria, não por suposição:

- **Eixos 1, 2, 3, 5**: sem colisão. Nenhum dos três módulos toca meio
  físico de rádio, broadcast sem fronteira, autenticação do lado da rede
  (só do lado do cliente/acesso), ou história de protocolo sem fio.
- **Eixo 4 (corporativa × doméstica, credencial por usuário)**: colisão
  leve e real com **`4.2.t6`** ("VPN, proxy e controle na porta"), que já
  descreve o mecanismo genérico de controle de acesso por porta — "o
  equipamento pede, o comutador intermedeia, o servidor de autenticação
  decide" — que é exatamente 802.1X, a base tanto do NAC cabeado quanto do
  Wi-Fi corporativo (WPA-Enterprise).

  **Troca proposta, para não reensinar**: o eixo 4 não descreve como
  802.1X funciona (isso é 4.2.t6, referenciado como já visto) — descreve
  por que o rádio **exige** esse mecanismo de um jeito que o cabo não
  exige. Posse física de um cabo já é, sozinha, um fator parcial de
  confiança (só quem tem acesso ao ambiente físico pluga); posse de nada
  equivalente existe no ar — qualquer um no alcance participa da mesma
  transmissão. É esse motivo estrutural, não o mecanismo do 802.1X em si,
  que é o conteúdo novo do eixo 4. `4.2.t6` fica como referência cruzada
  explícita ("volta a 4.2.t6"), nunca reescrito.

Nenhum outro ajuste necessário. Os cinco eixos do pedido, com essa única
troca de ênfase no eixo 4, seguem para a escrita.
