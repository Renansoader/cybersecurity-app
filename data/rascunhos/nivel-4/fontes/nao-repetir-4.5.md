# O que os módulos publicados já ensinam — não repetir no 4.5

Levantado em 30/08/2026, sobre os 25 módulos publicados (876 questões). O 4.5
(SIEM e monitoramento) é o de maior risco de colisão do corpus depois do 4.3:
log, alerta, correlação e "tempo até detectar" já aparecem, em graus diferentes,
em onze módulos.

## O achado que mais importa: 0.3 já ensina a MÉTRICA, não o MECANISMO

- **0.3.q13**: por que, contra adversário determinado, a métrica importante
  deixa de ser prevenção e passa a ser tempo até detectar
  — resposta: porque adversário com tempo e recurso acaba encontrando um caminho
- **0.3.q30**: presença de sete meses com pouca movimentação é comportamento
  típico de adversário persistente; a lacuna está na detecção, e a métrica a
  melhorar é o tempo até perceber

0.3 já fecha essa porta como **argumento estratégico** (por que detecção importa
mais que prevenção contra um adversário capaz). O 4.5 não pode reabrir essa
mesma porta. O que falta, e é território livre, é o argumento **operacional**:
como uma métrica de tempo até detectar se contrapõe a contar alerta e contar
regra como indicador de saúde do monitoramento — isso nenhum módulo toca.

## 1.1 — Linux essencial

- **1.1.q32**: enviar registros a um destino centralizado, só de adição, para
  que sobrevivam a um servidor comprometido — resposta é sobre **integridade do
  registro**, não sobre custo de coletar. Não repetir "centralizar para
  sobreviver ao comprometimento" como resposta certa.

## 1.2 — Linha de comando e shell

- **1.2.q24**: monitorar mudança em arquivos de cron e timers do systemd para
  detectar tarefa agendada não autorizada
- **1.2.q35**: script que alerta quando um endereço acumula mais de 50 falhas de
  autenticação em um dia — **já é uma regra de correlação por limiar**, do tipo
  mais simples. O 4.5 pode citar esse tipo de regra como dado, mas a lição nova
  é a pergunta que vem antes dela, não o limiar em si.

## 1.3 — Windows e Active Directory

- **1.3.q24**: por que um evento 4625 isolado raramente justifica um alerta —
  resposta: falha de logon isolada é rotina, não ataque. Território adjacente à
  fadiga de alerta, mas a lição aqui é "um evento sozinho não basta", não "a
  regra malfeita é que produz o ruído".
- **1.3.q27**: centralizar eventos dos controladores de domínio fora deles, com
  alerta para mudança, entrega mais valor primeiro
- **1.3.q33**: equipe pequena sem orçamento de ferramenta comercial: centralizar
  autenticação e mudança em conta/grupo privilegiado rende mais

Estas três já ensinam **o que priorizar coletar** num cenário concreto de AD.
O 4.5 não repete "o que centralizar primeiro"; ensina o raciocínio de custo por
trás de decidir o que coletar, em qualquer fonte, não só AD.

## 3.1 — Metodologia de pentest

- **3.1.q9**: sem quem detecte, não há o que um exercício de red team meça
- **3.1.q28**: teste de duas semanas sem gerar um único alerta na defesa vira
  achado próprio: **relacionar as ações executadas com o alerta que cada uma
  deveria ter disparado**

`3.1.q28` é o achado mais próximo do eixo 5 (validar provocando o evento de
propósito). A diferença: lá é um **red team encontrando a lacuna depois do
fato**, de fora para dentro. O 4.5 ensina a **prática recorrente do time de
detecção**, de dentro para fora — provocar o evento de propósito como rotina de
engenharia, não como achado de auditoria externa uma vez a cada dois anos.

## 3.2 — OSINT e reconhecimento

- **3.2.q31/q32**: monitorar logs de transparência de certificado do próprio
  domínio para flagrar emissão indevida
- **3.2.q34**: 400 e-mails coletados exigem finalidade definida, coleta mínima,
  prazo de retenção e descarte pela LGPD

`3.2.q34` já usa a palavra retenção, mas em **moldura jurídica** (LGPD, dado
pessoal). O 4.5 usa retenção em **moldura de orçamento de engenharia** (volume ×
dias × custo de armazenamento). Não é o mesmo argumento; ainda assim, nenhuma
questão do 4.5 deve usar prazo legal de retenção como resposta certa — esse
território já é do 0.4 e do 3.2.

## 3.3 — Varredura e enumeração

- **3.3.q29**: uma origem tocando mil portas em segundos caracteriza varredura;
  horário e endereço sozinhos, não
- **3.3.q30**: o log registrou a varredura inteira, e mesmo assim ela pode não
  ter sido detectada, porque **detecção exige regra que reconheça o padrão e
  alguém que leia o alerta — quase nenhuma linha é lida**
- **3.3.q31**: uma regra de limiar existe; a varredura reduz velocidade para
  ficar abaixo dela, ao custo de levar de horas a dias

`3.3.q30` já contém, em uma frase, quase o resumo do eixo 4 (fadiga de alerta).
A diferença que o 4.5 precisa sustentar: `3.3.q30` descreve o **sintoma**
("quase ninguém lê"); o 4.5 ensina o **diagnóstico** ("se o analista ignora o
alerta, o defeito é do alerta, não da disciplina dele") e a **consequência de
engenharia** disso — não é uma constatação nova, é uma count de vetor causal
oposto ao senso comum ("treinar mais o analista" não resolve alerta ruim).
`3.3.q31` já mostra evasão de uma regra de correlação existente; o 4.5 não
ensina evasão, ensina a origem da regra — a pergunta que a motivou.

## 4.1 — Hardening

- **4.1.q31**: item que faz o histórico ser sobrescrito rápido piora a
  investigação depois do incidente — sobre retenção mínima para forense, não
  sobre custo de coletar mais.

## 4.2 — Segurança de rede

- **4.2.q12**: assinatura malfeita marca tráfego legítimo de folha de pagamento
  como ataque; na posição de cópia isso **consome o tempo do analista**
- **4.2.q15**: tráfego cifrado esvazia a fila de alertas do sensor; a defesa
  muda o ponto de observação
- **4.2.q17**: duas linhas de log às 03h15 permitem afirmar um padrão reconhecido
  saindo de uma máquina interna; não permitem afirmar se houve resposta nem se
  havia autorização
- **4.2.q18**: espelhar tráfego antes ou depois do filtro de borda muda o que o
  sensor vê e o tamanho da fila

`4.2.q12` é o achado mais próximo do eixo 4: já mostra que uma assinatura ruim
custa tempo do analista. É um **caso**, não a **regra geral**. O 4.5 generaliza:
fadiga de alerta é *defeito de engenharia da regra*, não da pessoa — e isso vale
para qualquer fonte, não só assinatura de rede. `4.2.q17` já mostra o limite de
uma linha de log isolada, o que é prima-irmã da normalização (eixo 2), mas o
caso ali é sobre **suficiência de evidência**, não sobre **campo comum entre
fontes diferentes**.

## 4.3 — Defesa em profundidade

- **4.3.q15**: falha silenciosa é o controle que para de funcionar e continua
  reportando saúde — o distrator errado cita "fadiga de alerta" só para
  descartá-la como conceito diferente
- **4.3.q16**: uma regra de detecção sem disparo há seis meses — a leitura mais
  defensável é tratar o silêncio como **hipótese a testar**, não como prova de
  ausência de ataque
- **4.3.q17**: adversário com acesso administrativo prefere desligar a coleta,
  sem mexer no resto
- **4.3.q19**: agente parado de reportar em 40 estações há três dias, painel
  ainda mostra "protegido" — camada ausente que ninguém contabilizou como perda

`4.3.q16` é o achado mais próximo do eixo 5: já ensina que **silêncio de regra
não prova nada por si**. É exatamente onde o 4.5 precisa entrar sem repetir:
`4.3.q16` para na dúvida ("é hipótese a testar"); o 4.5 completa com o **método
que resolve a dúvida** — provocar o evento de propósito e confirmar (ou não) o
disparo, e nomear a equivalência: regra nunca testada é regra que não existe,
do mesmo jeito que alerta que ninguém lê. `4.3.q19` é sobre monitorar o próprio
controle (tema do 4.3), não sobre volume, correlação ou fadiga — sem colisão.

---

## Território livre do 4.5, resumido

1. **Custo de coletar como decisão de orçamento** (volume × retenção × fonte) —
   nenhum módulo toca. Mais próximo: 1.1.q32 (integridade) e 3.2.q34/0.4.q30
   (retenção legal), nenhum sobre custo de engenharia.
2. **Normalização — campo comum entre formatos diferentes** — nenhum módulo
   toca diretamente. Mais próximo: 4.2.q17 (limite de uma linha isolada), que é
   sobre suficiência de evidência, não sobre esquema comum entre fontes.
3. **Correlação como pergunta antes da regra** — 1.2.q35, 1.3.q24 e 3.3.q31 já
   mostram regras de limiar em uso ou em evasão; nenhuma ensina que escrever a
   regra antes de formular a pergunta é a fonte do ruído.
4. **Fadiga de alerta como defeito de engenharia, não de disciplina** —
   3.3.q30 e 4.2.q12 mostram sintomas concretos (ninguém lê, analista perde
   tempo); nenhum nomeia o princípio geral nem inverte a atribuição de culpa.
5. **Regra nunca testada = alerta que ninguém lê; validar provocando o evento**
   — 4.3.q16 chega mais perto (silêncio é hipótese a testar) e 3.1.q28 mostra o
   caso de auditoria externa; nenhum ensina a prática recorrente de validação
   proposital como rotina do time de detecção.
6. **Tempo até detectar como métrica contra contagem de alerta/regra** —
   0.3.q13/q30 já usam tempo até detectar como argumento estratégico; o 4.5
   usa o mesmo termo com finalidade diferente — indicador operacional de saúde
   do monitoramento, não motivo para investir em detecção.

A regra 5 do validador (resposta-certa × resposta-certa entre módulos) é quem
audita este documento depois de o módulo escrito — este levantamento é a
prevenção, não a garantia.
