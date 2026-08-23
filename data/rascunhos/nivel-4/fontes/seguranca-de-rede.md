# Fontes do módulo 4.2 — Segurança de rede

Levantamento do fio principal em 23/08/2026, direto na fonte. **[CONFIRMADO]** =
lido na fonte primária nesta rodada; **[CONSOLIDADO]** = conhecimento corrente,
não reaberto aqui.

---

## Normas de referência

**NIST SP 800-41 Rev. 1 — Guidelines on Firewalls and Firewall Policy** [CONFIRMADO]
Setembro de 2009, listada como final e corrente, sem nota de retirada. Supersede
a SP 800-41 original, de janeiro de 2002. Citar **sempre com a data**: o princípio
vale, o exemplo tecnológico é de 2009.
<https://csrc.nist.gov/pubs/sp/800/41/r1/final>

**NIST SP 800-94 — Guide to Intrusion Detection and Prevention Systems** [CONFIRMADO]
Fevereiro de 2007, final e ativa. **Atenção, armadilha:** existiu um rascunho de
Revisão 1 em 2012 que **nunca virou publicação final e foi retirado** — o NIST
registra que os comentários deixaram de ser aplicáveis às tecnologias e aos
modelos de ameaça atuais. Não existe "SP 800-94 Rev. 1" para citar.
<https://csrc.nist.gov/pubs/sp/800/94/final>

**NIST SP 800-207 — Zero Trust Architecture** [CONFIRMADO em rodada anterior]
Já usada no módulo 2.6. Aqui entra só pelo ângulo de rede: o perímetro deixa de
ser o limite de confiança, e a decisão passa a ser por sessão.

---

## O que a máquina mostrou — laboratório somente leitura

**Regras de firewall habilitadas: 476, e todas de permissão** [VERIFICADO EM EXECUÇÃO]
285 de entrada e 191 de saída, todas com ação `Allow`. Zero regras de bloqueio
habilitadas. Combinado com `DefaultInboundAction = NotConfigured` nos três
perfis, isso ensina o ponto central: **a proteção de entrada não vem das regras,
vem da ação padrão**; as regras são as exceções que abrem buracos nela. E a saída,
sem política e sem regra de bloqueio, é permissiva na prática.

**Tabela de rotas** [VERIFICADO EM EXECUÇÃO]
Rota padrão `0.0.0.0/0` pelo `192.168.100.1`, rede local `192.168.100.0/24`.
Endereços RFC 1918, dentro da regra de alvo do projeto.

**Proxy do sistema: acesso direto, nenhum servidor proxy** [VERIFICADO EM EXECUÇÃO]
Útil para separar proxy de sistema, proxy de navegador e proxy transparente.

**`estado_vs_estatico.py`** [VERIFICADO EM EXECUÇÃO]
Compara filtro sem estado e filtro com estado contra a mesma sequência de uma
conexão HTTPS de saída. Resultado: os quatro pacotes da conexão legítima passam
nos dois; o quinto pacote — não solicitado, vindo de outro endereço com porta de
origem 443 — **passa no filtro sem estado e é descartado pelo com estado**. É a
demonstração de por que o filtro sem estado precisa de uma regra de entrada larga
para o tráfego de volta, e de que essa regra é o flanco.

---

## Conhecimento consolidado — declarar como tal na fonte da questão

- **Firewall de próxima geração (NGFW)**: acrescenta identificação de aplicação
  independente de porta, identidade de usuário e inspeção de conteúdo. Não é
  norma; é categoria de mercado.
- **IDS x IPS**: o primeiro observa uma cópia do tráfego e alerta; o segundo fica
  em linha e pode descartar. A diferença que importa é a consequência do erro:
  falso positivo em IDS gera ruído, em IPS derruba tráfego legítimo.
- **Detecção por assinatura x por anomalia**: a primeira só encontra o que já foi
  descrito; a segunda precisa de linha de base e paga em falso positivo.
- **VPN**: cria canal autenticado e cifrado sobre rede não confiável. Não torna o
  cliente confiável — e é por isso que acesso remoto por VPN ampla convive mal
  com Zero Trust.
- **NAC e 802.1X**: autenticação na porta antes de entregar acesso à rede;
  suplicante, autenticador e servidor de autenticação. Postura do dispositivo
  como condição de entrada.
- **DMZ**: rede intermediária onde ficam serviços publicados, para que o
  comprometimento de um deles não dê acesso direto à rede interna.
- **VLAN e segmentação**: VLAN separa domínios de difusão em nível de enlace;
  segmentação de verdade exige filtragem entre os segmentos. VLAN sem filtro
  entre elas separa broadcast, não separa acesso.
- **VLAN hopping**: por switch spoofing (porta que aceita negociar tronco) ou por
  dupla marcação; a defesa é desabilitar negociação automática e não usar a VLAN
  nativa para dados.

---

## ARMADILHAS: o que NÃO escrever

1. **"NIST SP 800-94 Rev. 1"** — não existe: o rascunho de 2012 foi retirado.
2. **Citar a SP 800-41 sem a data** — é de 2009.
3. **"IPS é um IDS melhor"** — são posições diferentes na rede, com custos de erro
   diferentes; um não substitui o outro por ser mais novo.
4. **"VLAN é segmentação de segurança"** — sem filtro entre as VLANs, não é.
5. **"VPN protege a rede interna"** — ela protege o transporte; o dispositivo do
   outro lado continua sendo o que é.
6. **"Firewall de próxima geração dispensa segmentação"** — categoria de produto
   não substitui arquitetura.
7. **Repetir o que 1.4, 1.5, 3.3 e 4.1 já ensinam** — ver
   `nao-repetir-4.2.md`, gerado do conteúdo publicado.
