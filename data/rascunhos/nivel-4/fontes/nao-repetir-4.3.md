# O que os módulos publicados já ensinam — não repetir no 4.3

Gerado do conteúdo real em 25/08/2026. A regra 5 do validador compara resposta
certa com resposta certa entre módulos. Defesa em profundidade é o tema de maior
risco de colisão do corpus: camada, segmentação e escolha de controle já aparecem
em nove módulos.

## 0.1 — O que é cibersegurança

- **0.1.q9**: A área de segurança propõe cifrar todos os documentos com uma chave guardada em um cofre físico, acessíve
  - resposta: O ganho de confidencialidade se paga com uma perda severa de disponibilidade, e o controle provavelmente será contornado
- **0.1.q17**: Uma empresa investiu pesado em controles digitais e sofreu um vazamento: um estagiário foi convencido por
  - resposta: O incidente é de segurança da informação com vetor humano, e nenhum controle exclusivamente digital o teria evitado
- **0.1.q18**: A diretoria da sua empresa aprovou a compra de um firewall next-generation caro e comunicou internamente 
  - resposta: O firewall reduz um conjunto específico de riscos de rede, mas nada muda para phishing, acesso indevido de quem já está dentro ou 
- **0.1.q27**: A ação corretiva registrada resolve o incidente, mas deixa um dos três pilares — pessoas, processo e tecn
  - resposta: Processo: atualizar aquele servidor conserta a instância, mas não cria a rotina de inventário e de aplicação de correções que deix
- **0.1.q30**: Funcionários passaram a enviar planilhas de trabalho para o e-mail pessoal porque o compartilhamento inte
  - resposta: O controle é inviável na prática e por isso está sendo contornado
- **0.1.q32**: Um incidente foi possível porque um servidor de teste com dados reais estava exposto na internet, sem sen
  - resposta: Falha combinada: uma de tecnologia e outra de processo

## 0.2 — Superfície de ataque e ecossistema

- **0.2.q8**: Qual afirmação distingue corretamente superfície de ataque de vulnerabilidade?
  - resposta: Superfície é o conjunto de pontos alcançáveis; vulnerabilidade é uma falha explorável em um desses pontos
- **0.2.q11**: Uma empresa descobre que 30 planilhas com dados de clientes estão espalhadas por pastas compartilhadas, c
  - resposta: Dados: a informação está em lugares não previstos e sem controle
- **0.2.q14**: Por que dividir a superfície de ataque em cinco domínios é útil na prática?
  - resposta: Porque cada domínio falha de um modo diferente e é corrigido por um responsável diferente, o que orienta a ação
- **0.2.q23**: Uma empresa quer limitar o alcance de um invasor que consiga comprometer uma estação de trabalho. Qual me
  - resposta: Segmentar a rede e restringir quais sistemas podem ser alcançados a partir da faixa das estações
- **0.2.q28**: Entre as três estratégias de redução de superfície, qual é a mais eficaz quando aplicável?
  - resposta: Desligar o que não é usado, porque elimina o ponto de contato e junto com ele todo o custo futuro de defesa
- **0.2.q35**: Você recebeu a tarefa de mapear a superfície de ataque de uma empresa de 200 pessoas em duas semanas. Qua
  - resposta: Cobrir os cinco domínios em profundidade rasa, e aprofundar depois com base no que o mapa mostrar

## 0.3 — Quem é o adversário

- **0.3.q5**: Por que é útil descrever adversários pelos eixos motivação e capacidade?
  - resposta: Porque a combinação dos dois indica quais controles fazem diferença
- **0.3.q8**: Qual é o erro de priorização nesta análise?
  - resposta: Dimensiona a defesa pelo adversário menos provável e adia os controles que conteriam o adversário mais provável
- **0.3.q11**: Uma empresa de energia e uma loja virtual pedem, cada uma, um plano de segurança. Por que os planos não d
  - resposta: Porque os adversários plausíveis e o impacto de um incidente são diferentes, o que muda a prioridade dos controles
- **0.3.q27**: Por que a defesa contra insider costuma exigir equilíbrio explícito com confiança e privacidade, mais do 
  - resposta: Porque os controles recaem sobre pessoas da própria organização
- **0.3.q31**: Contra um adversário persistente que já demonstrou capacidade de entrar, qual medida reduz mais o dano po
  - resposta: Segmentar o ambiente e registrar os acessos entre segmentos
- **0.3.q35**: Você precisa apresentar à diretoria de uma indústria de médio porte quais adversários importam e o que fa
  - resposta: Priorizar crime organizado e ataque oportunista, e tratar insider por controles estruturais

## 0.4 — Ética, escopo e lei

- **0.4.q4**: Durante um teste autorizado, você descobre que um servidor fora do escopo tem uma falha grave e facilment
  - resposta: Parar, registrar a observação e comunicar ao contato do cliente, sem explorar a falha
- **0.4.q12**: O que caracteriza a divulgação responsável de uma vulnerabilidade?
  - resposta: Comunicar a falha ao responsável e conceder prazo para correção antes de qualquer divulgação pública
- **0.4.q34**: Quais problemas esta política apresenta?
  - resposta: Retenção sem prazo, acesso irrestrito sem controle de finalidade e coleta de conteúdo

## 1.1 — Linux essencial

- **1.1.q8**: Durante uma verificação, você encontra um script próprio da empresa com o bit SUID e dono root. Por que i
  - resposta: Qualquer falha no script passa a rodar com privilégio de root
- **1.1.q12**: Qual é a leitura mais preocupante deste trecho de /var/log/auth.log?
  - resposta: Uma sequência de falhas de autenticação do mesmo endereço termina em login bem-sucedido e leitura de /etc/shadow com sudo
- **1.1.q22**: Os itens 2, 3 e 4 têm um problema em comum. Qual é?
  - resposta: Todos concedem mais privilégio do que a aplicação precisa, ampliando o estrago de qualquer falha nela

## 1.2 — Linha de comando e shell

- **1.2.q27**: O que esta saída indica, e qual é o próximo passo mais útil?
  - resposta: Um endereço concentra três das quatro falhas; o próximo passo é verificar se houve login bem-sucedido a partir dele

## 1.3 — Windows e Active Directory

- **1.3.q5**: Por que a revisão de segurança em ambientes Windows precisa olhar os privilégios especiais, e não só a pe
  - resposta: Porque alguns privilégios equivalem na prática a controle total da máquina
- **1.3.q15**: Por que o Active Directory costuma ser o objetivo do movimento lateral, e não o ponto de entrada?
  - resposta: Porque o controlador raramente é acessível de fora, mas concentra o controle da rede
- **1.3.q24**: Por que um evento 4625 isolado raramente justifica um alerta?
  - resposta: Porque falhas de logon ocorrem rotineiramente, sem ataque nenhum

## 1.4 — Redes I

- **1.4.q2**: Em qual camada do modelo OSI atua um firewall que filtra por endereço IP e por porta?
  - resposta: Camadas 3 e 4
- **1.4.q13**: Um atacante conecta um servidor DHCP não autorizado à rede interna. Qual é o risco principal?
  - resposta: Ele pode entregar roteador padrão e servidor de DNS sob o controle dele
- **1.4.q24**: Quais problemas de segurança este projeto apresenta?
  - resposta: A rede plana, o NAT tratado como controle e o resolvedor de DNS aberto
- **1.4.q26**: Qual é a diferença entre endereço IP e endereço físico de rede (MAC)?
  - resposta: O endereço IP é lógico e roteável entre redes; o endereço físico identifica a interface dentro do segmento local

## 1.5 — Redes II

- **1.5.q8**: Um usuário recebe um link, abre a página, vê o cadeado no navegador e conclui que o site é confiável para
  - resposta: O cadeado indica conexão cifrada e controle do domínio, não legitimidade

## 2.3 — Criptografia III

- **2.3.q3**: O que acontece quando o mesmo nonce é usado duas vezes com a mesma chave em AES-GCM?
  - resposta: Falha catastrófica: o sigilo cai e dá para forjar mensagens válidas
- **2.3.q19**: Por que testes automatizados raramente detectam falhas criptográficas de uso?
  - resposta: Porque eles verificam que cifrar e decifrar funcionam, e a falha está no que vaza

## 2.5 — Autenticação e identidade

- **2.5.q13**: O que HttpOnly, Secure e SameSite fazem no cookie de sessão?
  - resposta: Bloqueiam leitura por JavaScript, envio fora de HTTPS e envio a partir de outro site

## 2.6 — Controle de acesso

- **2.6.q16**: A área financeira tem apenas duas pessoas, e não é possível separar cadastro de fornecedor de aprovação d
  - resposta: Controle compensatório: aprovação por gestor de fora da área, alçada por valor e revisão do log
- **2.6.q22**: O que esta saída informa sobre a origem e o alcance das permissões deste arquivo?
  - resposta: As três entradas vieram herdadas do diretório pai, e as três concedem controle total
- **2.6.q35**: Uma equipe herdou um sistema com IDOR nos endpoints, sem revisão de acesso e com permissão por usuário. P
  - resposta: Pela verificação de propriedade no servidor, porque a falha é explorável hoje por qualquer conta

## 2.7 — Fator humano

- **2.7.q17**: No cadastro interno de fornecedores da Contoso, a Aurora Suprimentos Ltda consta com o domínio aurorasupr
  - resposta: O domínio do remetente é sósia do que consta no cadastro: o DMARC só prova controle daquele domínio
- **2.7.q26**: Quais itens desta política contrariam a orientação atual sobre senha?
  - resposta: Os itens 1, 2, 3 e 4; o item 5 é justamente um controle que a norma vigente exige

## 3.1 — Metodologia de pentest

- **3.1.q7**: Qual é a diferença entre uma varredura de vulnerabilidade e um teste de intrusão?
  - resposta: A varredura verifica a possível existência da falha; o teste explora a falha para confirmar que ela existe
- **3.1.q8**: O que um exercício de red team mede que um teste de intrusão não mede?
  - resposta: A capacidade de detecção e de resposta das pessoas, dos processos e da tecnologia de defesa
- **3.1.q22**: Por que a janela de teste registra horários, e não apenas as datas de início e fim?
  - resposta: Porque o horário decide quanto impacto uma falha de teste causa, e o pico de operação é o pior momento
- **3.1.q30**: O script `--script vuln` do nmap aponta falha conhecida no serviço da porta 8080 do alvo autorizado. Como
  - resposta: Como achado potencial, até que a tentativa de confirmação diga se a falha existe naquele alvo
- **3.1.q34**: Qual é a diferença entre um problema sistêmico e um problema sintomático no relatório?
  - resposta: O sintomático é a falha observada em um ponto; o sistêmico é o processo que a produz e a repete

## 3.2 — OSINT e reconhecimento

- **3.2.q32**: O monitoramento apontou um domínio parecido com o da empresa, recém-registrado e já com certificado emiti
  - resposta: Registrar o achado, acionar quem responde pela marca e preparar bloqueio de correio e comunicação

## 3.3 — Varredura e enumeração

- **3.3.q15**: O que esses cabeçalhos entregam, e o que remover Server e X-Powered-By resolve?
  - resposta: Entregam nome e versão do software; removê-los apaga um atalho de identificação, não a falha da versão
- **3.3.q22**: Por que a transferência de zona (AXFR) anônima quase sempre falha hoje?
  - resposta: Porque a norma recomenda que a política padrão não seja aberta a todos, com controle por TSIG ou por endereço

## 4.1 — Hardening

- **4.1.q21**: Os quatro itens têm problema. Qual deles já era ruim em 2021 e continua ruim hoje, independentemente de q
  - resposta: O item 3, porque descartar pela pontuação isolada apaga a falha média que está exposta e sendo usada
- **4.1.q22**: Como o NIST SP 800-40 Rev. 4, de abril de 2022, enquadra a atividade de aplicar correções?
  - resposta: Como manutenção preventiva e custo corrente de operar, planejada em estratégia da organização inteira
- **4.1.q26**: Um item do benchmark bloqueia o funcionamento de um sistema legado que a operação ainda depende. Qual é o
  - resposta: Registrar um desvio autorizado, com responsável, motivo, data de nova revisão e medida compensatória enquanto durar

## 4.2 — Segurança de rede

- **4.2.q15**: A maior parte do tráfego da rede passou a ser cifrada e a fila de alertas do sensor esvaziou. Como o adve
  - resposta: O ataque viaja dentro do túnel e o sensor passa a ver só metadados; a defesa muda o ponto de observação para onde o dado já está c
- **4.2.q16**: Três itens deste rascunho têm defeito e um descreve prática defensável. Qual dos defeituosos age sobre os
  - resposta: O item 1, porque ligar tudo de uma vez em modo de bloqueio derruba conexão legítima antes de qualquer ajuste fino
- **4.2.q25**: A rede já está dividida em três segmentos com filtragem entre eles, e mesmo assim um comprometimento se e
  - resposta: Levar a decisão para dentro do segmento, com política por carga de trabalho, de modo que duas máquinas vizinhas deixem de se enxer

