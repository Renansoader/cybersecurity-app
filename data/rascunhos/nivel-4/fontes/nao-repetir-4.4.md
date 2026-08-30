# O que os módulos publicados já ensinam — não repetir no 4.4

Gerado do conteúdo real em 25/08/2026. Compara resposta certa com resposta certa,
que é o critério da regra 5 do validador.

## 0.1 — O que é cibersegurança

- **0.1.q7**: Um ransomware cifra os arquivos do servidor de arquivos e exige pagamento. Qual controle preserva a 
  - resposta: Backup em cópia isolada da rede, testado por restauração periódica
- **0.1.q13**: Uma empresa contrata um serviço de segurança que cobre firewall, antivírus e monitoramento de rede, 
  - resposta: O contrato cobre o recorte digital; conversa, papel, crachá e comportamento das pessoas continuam sem tratamento

## 0.3 — Quem é o adversário

- **0.3.q7**: O que caracteriza o modelo de ransomware como serviço (ransomware as a service)?
  - resposta: Um grupo desenvolve e mantém o ransomware, e outros operam os ataques mediante divisão dos ganhos
- **0.3.q16**: Uma organização identifica que seu adversário mais plausível é o crime organizado com ransomware. Qu
  - resposta: Backup em cópia isolada, com teste periódico de restauração e prazo conhecido de recuperação
- **0.3.q17**: O plano é coerente com o adversário escolhido, exceto em um ponto. Qual?
  - resposta: O backup no mesmo servidor de arquivos: ransomware cifra também as cópias acessíveis a partir do sistema comprometido
- **0.3.q28**: O que a sigla APT designa, e qual das três palavras é a mais determinante para a defesa?
  - resposta: Ameaça persistente avançada, e a palavra determinante é persistente: o adversário permanece no ambiente por longos períodos
- **0.3.q30**: Uma investigação revela que um invasor esteve no ambiente por sete meses, com acessos discretos em h
  - resposta: Comportamento típico de adversário persistente; a lacuna está na detecção, e a métrica a melhorar é o tempo até perceber

## 1.1 — Linux essencial

- **1.1.q2**: Qual é a diferença entre /etc/passwd e /etc/shadow?
  - resposta: /etc/passwd lista as contas e é legível por todos; /etc/shadow guarda os hashes de senha e é restrito ao root
- **1.1.q28**: Um analista encontra o arquivo /etc/shadow com permissão 644. Qual é o impacto?
  - resposta: Qualquer usuário da máquina pode copiar os hashes de senha e tentar quebrá-los offline, sem gerar tentativa de login
- **1.1.q30**: O que chama atenção nesta listagem?
  - resposta: backup-helper tem o bit SUID e data de modificação muito posterior aos demais

## 1.2 — Linha de comando e shell

- **1.2.q14**: Depois de remover um malware de um servidor, a infecção reaparece todos os dias no mesmo horário. Qu
  - resposta: Existe um mecanismo de persistência, como tarefa agendada ou serviço, que reinstala o código periodicamente

## 1.3 — Windows e Active Directory

- **1.3.q22**: Uma estação apresenta um processo do PowerShell iniciado por um documento de escritório, com linha d
  - resposta: Comportamento típico de execução maliciosa a partir de macro em documento; a codificação serve para dificultar a leitura do c
- **1.3.q29**: Durante uma triagem, você encontra uma conta local recém-criada em um servidor, pertencente ao grupo
  - resposta: Persistência criada por um invasor, usando nome semelhante ao de contas legítimas para não chamar atenção

## 1.4 — Redes I

- **1.4.q8**: Uma empresa afirma estar protegida porque todas as estações estão atrás de NAT. Quais riscos permane
  - resposta: Phishing, código malicioso, conexões de saída e ataques na rede interna

## 1.6 — Python para segurança

- **1.6.q10**: Qual trecho calcula o SHA-256 de um arquivo grande sem carregá-lo inteiro na memória?
  - resposta: h = hashlib.sha256()
with open(caminho, "rb") as arq:
    for bloco in iter(lambda: arq.read(8192), b""):
        h.update(bl
- **1.6.q28**: Uma equipe quer detectar alteração não autorizada em arquivos de configuração de servidores. Qual ab
  - resposta: Guardar o hash de cada arquivo à parte e comparar periodicamente

## 1.7 — Git e versionamento

- **1.7.q20**: Reescrever o histórico para remover um segredo resolve o problema?
  - resposta: Parcialmente: a reescrita não alcança clones já feitos nem backups

## 2.2 — Criptografia II

- **2.2.q4**: Um documento assinado digitalmente é também um documento secreto?
  - resposta: Não: a assinatura prova origem e integridade, não sigilo
- **2.2.q24**: Qual é a diferença entre assinatura digital e HMAC?
  - resposta: A assinatura usa par de chaves; o HMAC usa segredo compartilhado

## 2.3 — Criptografia III

- **2.3.q8**: O que é um canal lateral em criptografia?
  - resposta: Informação que vaza pelo comportamento, e não pelo texto cifrado

## 2.4 — Funções de hash, integridade e armazenamento de senhas

- **2.4.q17**: Qual é a diferença entre hash e HMAC na verificação de integridade?
  - resposta: O hash detecta corrupção acidental; o HMAC usa chave secreta
- **2.4.q20**: Qual item revela que a política não está apenas desatualizada, mas descreve algo tecnicamente imposs
  - resposta: O item 3: hash não é reversível, e ele promete recuperar a senha
- **2.4.q31**: Por que a resistência a colisão é a propriedade que mais importa em assinatura digital?
  - resposta: Porque a assinatura é calculada sobre o resumo, e não sobre o documento

## 2.5 — Autenticação e identidade

- **2.5.q30**: O que esta execução demonstra sobre o JWT?
  - resposta: O conteúdo é legível sem chave, mas alterá-lo quebra a verificação da assinatura
- **2.5.q32**: Qual é a falha deste verificador de JWT?
  - resposta: Ele lê o algoritmo do próprio token, e um token com alg:none passa sem assinatura

## 2.7 — Fator humano

- **2.7.q8**: Por que o padrão pré-definido (default) é o controle mais poderoso de uma interface?
  - resposta: Porque a maioria não muda configuração alguma, então quem escolhe o padrão escolhe o comportamento
- **2.7.q11**: O que o termostato de risco prevê sobre um novo controle de segurança?
  - resposta: Que parte do ganho será consumida por comportamento mais ousado, porque as pessoas miram um nível de risco
- **2.7.q23**: Uma empresa publica o ranking dos setores que mais clicaram na última simulação de phishing. Qual é 
  - resposta: Causa sofrimento e desconfiança na equipe e muda pouco o comportamento, sem tocar na causa do risco
- **2.7.q31**: Por que esta cartilha falha justamente contra a fraude de e-mail corporativo (BEC)?
  - resposta: Porque a mensagem de BEC não tem link, anexo nem erro, e o remetente pode ser um domínio sósia

## 3.3 — Varredura e enumeração

- **3.3.q7**: O que a detecção de versão (-sV) acrescenta, e o que a linha da saída passa a afirmar?
  - resposta: Ela interroga a porta aberta com uma base de sondas, e a linha passa a afirmar compatibilidade com uma assinatura

## 4.1 — Hardening

- **4.1.q9**: Os três perfis desta máquina saíram assim. O que essa combinação de valores informa a quem audita?
  - resposta: Que o mecanismo está ativo, mas nenhuma política definiu a ação padrão: o comportamento vem do que o sistema traz de fábrica

## 4.2 — Segurança de rede

- **4.2.q8**: Nenhuma regra de bloqueio aparece entre as 476 habilitadas desta máquina. O que sustenta, então, a p
  - resposta: O comportamento aplicado ao pacote que não casa com regra alguma; as 476 linhas são exceções cavadas nele, e não a proteção e

## 4.3 — Defesa em profundidade

- **4.3.q14**: No Windows, sem alterar nada, você quer saber de que motor e de que canal de atualização as proteçõe
  - resposta: `Get-MpComputerStatus`, que traz o estado, a versão de motor e a idade das assinaturas


**Total: 33 respostas certas já publicadas tocam o assunto.**
