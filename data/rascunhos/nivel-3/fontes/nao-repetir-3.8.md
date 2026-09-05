# Levantamento de não-repetição — módulo 3.8 (Quebra de senhas)

## Por que este levantamento é mais pesado que o normal

A colisão aqui é prevista, não uma surpresa a descobrir: o módulo 2.4
("Hash e senhas") e o 2.5 ("Autenticação e identidade") já cobrem armazenamento
de senha e política de senha em profundidade. Qualquer eixo de 3.8 que reensine
o que esses dois já ensinam é desperdício de módulo. A pergunta não é "existe
colisão?" — é "quanto território sobra depois de tirar o que já tem dono?".

## Medição, não estimativa

Contagem de menções por módulo publicado, varrendo teoria e questões de todos
os 33 módulos (`json.dumps` de cada bloco, contagem de substring, case-insensitive):

| eixo candidato | 2.4 | 2.5 | outros módulos com menção relevante |
|---|---|---|---|
| hash lento / Argon2id / scrypt / PBKDF2 / bcrypt / fator de custo | 72 | 5 | 1.6 (3, uso geral de hash em Python) |
| sal (único por usuário) | 21 | 0 diretas (entropia de sessão, não de senha) | 4.2 (13, "salt" em contexto de rede, falso positivo de palavra) |
| política de senha (comprimento, composição, troca periódica) | 14 | 32 | 2.1, 2.3, 2.7 (contexto de cripto/fator humano, não política em si) |
| limite de tentativas / bloqueio de conta | 21 | 1 | 1.3 (3, política de conta do AD) |
| "ataque offline" como conceito nomeado | 24 | 9 | — |

Achado central, com leitura do texto-fonte, não só da contagem:

- **2.4.t3 e 2.4.q11** já definem "ataque offline" como conceito nomeado e
  explicam por que ele muda a defesa (sem limite de tentativas, sem bloqueio,
  sem registro). **Isso é dono territorial: 3.8 não pode reintroduzir essa
  definição como se fosse nova.**
- **2.5.t2**, texto conferido linha a linha, já ensina o NIST SP 800-63B 2025
  completo para senha: 15 caracteres como fator único, 8 dentro de MFA, aceitar
  64+, proibição normativa (`SHALL NOT`) de regra de composição, troca periódica
  e pergunta de segurança, mais a obrigação de comparar contra lista de senhas
  vazadas no cadastro. **Os mesmos números que 2.4.t5 usa para Argon2id (19 MiB,
  2 iterações, paralelismo 1) aparecem de novo em 2.5.t2.** Não há brecha
  numérica para 3.8 preencher aqui — está coberto duas vezes já.
- **Busca por vocabulário de custo de ataque** (`entropia`, `espaço de busca`,
  `bits de entropia`, `tentativas por segundo`, `keyspace`) devolveu só três
  acertos genuínos: `2.3.t?` (espaço de chaves, contexto de cifra simétrica,
  não senha), `2.4.q?` (uma menção pontual a espaço de busca, não desenvolvida
  em conta numérica) e `2.5` (entropia de **identificador de sessão**, 64 bits,
  nada a ver com senha humana). **Nenhum módulo publicado faz a conta
  "tentativas por segundo × tamanho do espaço" para senha, com números medidos
  em execução.** Território livre, e é o mais defensável dos cinco eixos
  propostos.
- **Busca por vocabulário de ataque estruturado** (`ataque de dicionário`,
  `regra de transformação`, `mangling`, `leet`, `máscara`) devolveu só falso
  positivo: `1.4` usa "máscara" no sentido de máscara de sub-rede IPv4, sem
  relação nenhuma com transformação de senha. **Nenhum módulo ensina por que um
  ataque real usa estrutura em vez de varrer o espaço inteiro.** Território
  livre.
- **3.2 e 3.3** (nível 3, já publicados) usam "força bruta" 15 e ~8 vezes
  respectivamente, mas sempre em enumeração de rede — subdomínio via
  transparência de certificado vs. wordlist de DNS (3.2), diretório web via
  gobuster (3.3). Conferido lendo o trecho ao redor de cada ocorrência, não só
  a contagem: **nenhuma menção trata de força bruta contra credencial de
  login.** Não há colisão de mecanismo, só reuso do termo genérico "força
  bruta" para um problema diferente — vale citar isso no módulo para não
  parecer que 3.8 inventa o termo do zero, mas sem reensinar enumeração de DNS.

## Veredito

Sobra território real, mas é estreito e específico: **economia do ataque**, não
armazenamento nem política. Os cinco eixos propostos originalmente sobrevivem à
medição, com um ajuste:

1. **Ataque on-line × off-line, e o que precisa acontecer antes do off-line ser
   possível.** 2.4 já nomeia e contrasta os dois; 3.8 não redefine o conceito —
   assume-o como visto (nível 2 é pré-requisito) e foca no que falta em 2.4: o
   evento que muda de regime (vazamento da base de hashes, não só do banco
   inteiro — precisa dos hashes especificamente) e por que, depois desse
   evento, as defesas de 2.4/2.5 (bloqueio de conta, limite de tentativas) já
   não fazem nada.
2. **A conta de custo: tentativas/segundo × tamanho do espaço.** Território
   livre confirmado acima. Este é o eixo estruturante do módulo — o laboratório
   `custo_da_tentativa.py` mede, nesta máquina, a taxa real de um hash rápido
   contra um hash lento calibrado com os mesmos 600.000 iterações de PBKDF2 que
   2.4.t5 já cita, e projeta o tempo para esgotar um espaço de exemplo. A
   referência aos parâmetros de 2.4 é cruzada, não reensinada: o módulo aponta
   "isto é o que aquele número compra", sem redefinir o que é Argon2id.
3. **Por que senha humana é previsível, e por que ataque real é estrutura,
   não busca exaustiva.** Território livre confirmado acima. Cuidado editorial
   aplicado: a lista de palavras-base do laboratório é inventada para este
   script (não é lista de senha real nem trecho de dicionário de ataque
   conhecido), e nenhuma senha comum de verdade é citada em teoria ou questão —
   a restrição do módulo pede exatamente isso.
4. **O que "quebrado" significa e o que não significa.** Território livre —
   nenhum módulo publicado distingue "recuperar esta senha dentro desta
   estratégia" de "quebrar o algoritmo de hash", nem alerta que tempo médio de
   quebra de um lote esconde o pior caso. O laboratório
   `estrutura_e_o_que_quebrado_significa.py` demonstra os dois pontos com
   execução real: duas senhas de formato humano caem em milissegundos contra a
   lista estruturada, uma senha aleatória de 12 caracteres não cai — e o
   SHA-256 das três continua igualmente íntegro, porque nada ali quebrou a
   função, só a estratégia de busca encontrou ou não a entrada certa.
5. **Contraponto defensivo, fechando o módulo, sem reensinar o 2.4.** Não é um
   eixo de conteúdo novo — é a costura final: a conclusão de que os parâmetros
   de 2.4 (hash lento, sal) e a política de 2.5 (comprimento, MFA) existem
   precisamente para encarecer os dois lados da conta do eixo 2. Formulado como
   referência cruzada ("volte a 2.4.t5" / "volte a 2.5.t2"), nunca como
   repetição do número.

## Ajuste feito em relação ao pedido original

Nenhum. Os cinco eixos propostos no pedido sobrevivem à medição sem
reformulação — diferente de 3.4, 3.5, 3.6 e 3.7, que precisaram de eixo
reformulado depois do levantamento. A única mudança é de ênfase no eixo 1:
como 2.4 já define ataque offline, 3.8 assume a definição como pré-requisito
(nível 2 completo) e entra direto no evento de transição de regime, em vez de
redefinir o conceito.

## Regra de cruzamento

O curso desbloqueia por nível: nível 3 pode referenciar nível 2 e anteriores
como já vistos (2.4, 2.5, 1.6), nunca nível 4 ou 5. Toda referência cruzada
neste módulo aponta para trás.
