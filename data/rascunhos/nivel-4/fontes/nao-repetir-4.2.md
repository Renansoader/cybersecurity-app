# O que os módulos publicados já ensinam — não repetir no 4.2

Gerado do conteúdo real em 23/08/2026. A regra 5 do validador compara resposta
certa com resposta certa entre módulos: escrever de novo qualquer uma destas
vira aviso, e vira o oitavo par duplicado do projeto.

## 0.1 — O que é cibersegurança

- **0.1.q13**: Uma empresa contrata um serviço de segurança que cobre firewall, antivírus e monitoramento de r
  - resposta: O contrato cobre o recorte digital; conversa, papel, crachá e comportamento das pessoas continuam sem tratamen
- **0.1.q18**: A diretoria da sua empresa aprovou a compra de um firewall next-generation caro e comunicou int
  - resposta: O firewall reduz um conjunto específico de riscos de rede, mas nada muda para phishing, acesso indevido de que

## 0.2 — Superfície de ataque e ecossistema

- **0.2.q23**: Uma empresa quer limitar o alcance de um invasor que consiga comprometer uma estação de trabalh
  - resposta: Segmentar a rede e restringir quais sistemas podem ser alcançados a partir da faixa das estações

## 0.3 — Quem é o adversário

- **0.3.q31**: Contra um adversário persistente que já demonstrou capacidade de entrar, qual medida reduz mais
  - resposta: Segmentar o ambiente e registrar acessos entre segmentos, de modo que alcançar sistemas críticos exija passos 

## 1.2 — Linha de comando e shell

- **1.2.q3**: Você executa `comando_com_erros | grep "aviso"` e as mensagens de erro continuam aparecendo no 
  - resposta: O pipe liga apenas a saída padrão ao comando seguinte; a saída de erro segue por fora da cadeia

## 1.4 — Redes I — modelo, endereçamento e serviços de base

- **1.4.q2**: Em qual camada do modelo OSI atua um firewall que filtra por endereço IP e por porta?
  - resposta: Camadas 3 e 4: rede e transporte
- **1.4.q7**: Qual afirmação sobre o NAT é correta?
  - resposta: Ele foi criado para lidar com a escassez de endereços IPv4 públicos, e a redução de exposição é um efeito cola
- **1.4.q8**: Uma empresa afirma estar protegida porque todas as estações estão atrás de NAT. Quais riscos pe
  - resposta: Phishing, download de código malicioso, conexões de saída para servidores de controle e ataques entre máquinas
- **1.4.q13**: Um atacante conecta um servidor DHCP não autorizado à rede interna. Qual é o risco principal?
  - resposta: Ele pode entregar às máquinas um roteador padrão e um servidor DNS sob seu controle, colocando-se no meio do t
- **1.4.q24**: Quais problemas de segurança este projeto apresenta?
  - resposta: Rede plana sem segmentação permite movimento lateral livre, NAT não é controle de segurança, e o DNS aberto po
- **1.4.q27**: Uma empresa precisa dividir a rede 192.168.20.0/24 em quatro sub-redes de tamanho igual. Qual p
  - resposta: /26, com 62 hosts utilizáveis por sub-rede
- **1.4.q28**: Uma rede tem servidores e estações na mesma faixa. Qual mudança reduz mais o alcance de uma est
  - resposta: Separar servidores e estações em sub-redes distintas e filtrar explicitamente o tráfego permitido entre elas
- **1.4.q31**: Por que um firewall que filtra apenas por endereço e porta não detecta um ataque contra uma apl
  - resposta: Porque o ataque trafega dentro de requisições legítimas na porta permitida; o problema está no conteúdo, que e
- **1.4.q33**: O que significa dizer que o NAT quebra a comunicação fim a fim?
  - resposta: O endereço visto pelo destino não é o da máquina de origem, o que dificulta conexões iniciadas de fora e algun
- **1.4.q35**: Você vai projetar a rede de um escritório novo com 60 estações, 6 servidores e rede sem fio par
  - resposta: Sub-redes separadas para estações, servidores e visitantes, com filtragem explícita entre elas, DHCP restrito 

## 1.5 — Redes II — transporte, HTTP e TLS

- **1.5.q31**: Em uma varredura de portas, o que costuma diferenciar uma porta filtrada de uma porta fechada?
  - resposta: A porta fechada responde com RST; a filtrada normalmente não responde nada, porque um equipamento descartou o 

## 1.6 — Python para segurança

- **1.6.q2**: Este código tem dois defeitos que não geram mensagem de erro. Quais são?
  - resposta: Não define tempo limite, então portas filtradas travam a execução; e range(inicio, fim) nunca testa a porta 25
- **1.6.q17**: Um script de varredura de portas roda muito devagar em uma faixa de rede filtrada. Qual é a cau
  - resposta: O tempo limite está alto ou ausente: portas filtradas não respondem e cada tentativa espera até o limite; redu
- **1.6.q24**: Por que chamar `s.settimeout(0.5)` antes de `s.connect_ex(...)` em uma varredura?
  - resposta: Para que portas filtradas, que não respondem, não travem a execução até o limite do sistema

## 2.7 — Fator humano — por que a segurança falha nas pessoas

- **2.7.q22**: Um proxy de phishing intercepta o login em tempo real e repassa o segundo fator. O que resiste?
  - resposta: Passkey ou chave FIDO2: a credencial é vinculada à origem e a chave privada não sai do autenticador

## 3.2 — OSINT e reconhecimento — mapear a pegada sem tocar no alvo

- **3.2.q11**: Por que um host interno chamado vpn-teste aparece em log de transparência de certificado?
  - resposta: Porque o certificado publicamente confiável dele precisa estar em log público para ser aceito
- **3.2.q29**: Como reduzir o que uma vaga de emprego entrega, sem prejudicar a contratação?
  - resposta: Descrever competência em vez de inventário: firewall de próxima geração, e não produto e versão

## 3.3 — Varredura e enumeração — o que a rede responde e o que isso deixa no log

- **3.3.q4**: Numa varredura autorizada, a porta 22 saiu fechada e a 8080 saiu filtrada. O que cada uma dessa
  - resposta: Que o host respondeu e não tem serviço em 22; sobre a 8080, apenas que existe filtragem entre o ponto de teste
- **3.3.q8**: Como a detecção de sistema operacional (-O) chega ao palpite, e por que ela erra?
  - resposta: Compara a impressão digital da pilha TCP/IP com uma base; firewall, NAT e balanceador alteram a amostra
- **3.3.q10**: Na varredura UDP (`nmap -sU 192.168.10.20`), uma porta não responde a nenhuma retransmissão. Co
  - resposta: Como aberta ou filtrada, porque o silêncio não separa serviço calado de sonda bloqueada
- **3.3.q32**: Os quatro itens têm defeito. Qual deles promete ao cliente um resultado que o testador não tem 
  - resposta: O item 3, que promete que o cliente não vai perceber o teste, embora IDS e firewall pessoal reconheçam a varre
- **3.3.q34**: Depois da segmentação, a mesma varredura externa passou a relatar portas filtradas. O que mudou
  - resposta: As sondas deixaram de alcançar as portas, então o alcance de quem varre diminuiu, e não apenas a informação

## 4.1 — Hardening — linha de base, superfície mínima e correção por risco

- **4.1.q10**: O item de auditoria "firewall de host ativo: sim ou não" foi marcado como conforme em todas as 
  - resposta: "Ação padrão de entrada definida por política e igual a bloquear, nos três perfis", que nomeia o valor esperad
- **4.1.q13**: Numa conferência de linha de base no Windows, qual leitura devolve, por perfil de firewall, o e
  - resposta: `Get-NetFirewallProfile`, que traz uma linha por perfil com os dois campos lado a lado

