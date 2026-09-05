# Cybersecurity Study App — estado do projeto

Aplicativo desktop local de estudo de cibersegurança, em Python + CustomTkinter,
com SQLite para progresso e JSON para conteúdo. Roda offline.

Última atualização: 2026-09-05 · módulo 3.8 (Quebra de senhas) escrito e
publicado — a economia do ataque (on-line×off-line, custo = tentativas/s ×
espaço de busca, previsibilidade humana, ataque estruturado, o que
"quebrado" significa), não operação de ferramenta · dois laboratórios só
com hashes e senhas autogerados · defeito real achado por lente adversarial
(inversão multiplicar/dividir na conta de custo, contradizendo `q7`/`q14`
do próprio módulo) corrigido antes de publicar · nenhuma sétima variante de
molde encontrada (2,9%, a menor taxa da linha) · duas regras novas de
processo (PROGRESS.md §7, regras 9 e 10): citação sempre confirmada em
fonte bruta, achado de lente é hipótese a verificar · 3.886 testes passando

Repositório: <https://github.com/Renansoader/cybersecurity-app> (privado)

---

## 1. Números

| Item | Quantidade |
|---|---|
| Módulos de conteúdo escritos | 34 de 41 |
| Questões | 1.192 |
| Blocos de teoria | 206 |
| Tags distintas | 897 |
| Testes automatizados | 3.886 |
| Linhas de código Python | ~2.280 no app · ~3.950 com ferramentas e testes |

Questões por nível: **nível 0** 141 (4 módulos) · **nível 1** 245 (7 módulos) ·
**nível 2** 245 (7 módulos, completo) · **nível 3** 281 (8 de 9 módulos) · **nível 4** 280 (8 de 8, completo).

Tipos de questão em uso: conceitual 471, cenário 264, ataque→defesa 97,
caça ao erro 96, comando 57, artefato 85, pareamento 71, ordenação 51.

---

## 2. Estrutura de arquivos

```
C:\Dev\cybersecurity-app\
├── README.md                como rodar, esquema JSON e como escrever um módulo
├── main.py                  ponto de entrada: janela, sidebar, roteamento
├── app.ico                  ícone da janela e do atalho
├── conftest.py              faz o pytest achar o pacote `app`
├── run.bat                  usa .venv se existir, senão o Python do sistema
├── requirements.txt         customtkinter (única dependência de runtime)
├── requirements-dev.txt     pytest
├── .gitignore               docs/, progress.db, __pycache__, .venv
├── app/
│   ├── theme.py             paleta Tokyo Night + helpers visuais reutilizáveis
│   ├── db.py                camada SQLite: tentativas, SRS, status, preferências
│   ├── content.py           carga e validação de esquema dos JSONs
│   ├── engine.py            SRS, domínio, desbloqueio, sessão, streak
│   ├── pedagogy.py          dicas, pergunta socrática, embaralho, correção
│   └── views/               home, trilha, modulo, sessao, progresso (prontas)
│                            desafio, glossario, ferramentas (stubs)
├── data/
│   ├── niveis.json          6 níveis e regras de desbloqueio
│   ├── modulos/*.json       25 módulos (00-01 … 04-04)
│   └── rascunhos/            laboratórios, fontes e relatórios de procedência
├── exemplo/
│   └── modulo-minimo.json   modelo comentado, um exemplo de cada tipo de questão
├── ferramentas/
│   ├── validar_modulo.py    valida um módulo antes de ele entrar em data/modulos/
│   ├── chutador_de_forma.py portão de comprimento: taxa de "mais_longa" por módulo
│   ├── medidor_molde_dica.py triagem (não portão) de molde de frase repetido em dicas
│   ├── avisos_aceitos.json  casos já lidos e justificados, que não viram aviso
│   └── gerar_icone.py       redesenha o app.ico (precisa de pillow)
├── tests/                   7 arquivos de teste
├── docs/                    PDFs de referência (fora do Git)
└── progress.db              criado no primeiro uso (fora do Git)
```

---

## 3. Decisões técnicas

### Arquitetura

- **Views nunca falam com o SQLite.** Tudo passa por `app/db.py`.
- **Views são funções `montar(pai, app)`**, não classes — segue o padrão do
  fullstack-study-app e não pagava nada como classe.
- **Roteamento dentro de `main.py`**, sem arquivo de navegação: trocar frame são
  ~10 linhas.
- **`theme.py` copiado, não importado** do fullstack-study-app. Dependência entre
  pastas de projeto quebraria o repositório separado.
- **Conteúdo carregado uma vez** na inicialização; erros de validação aparecem em
  faixa vermelha na interface, sem derrubar o app.

### Banco de dados

- **A regra "só a primeira tentativa conta" é garantida pelo banco**, não pelo
  código de tela:

  ```sql
  CREATE UNIQUE INDEX idx_primeira_tentativa
  ON tentativas(questao_id) WHERE n_tentativa = 1;
  ```

  Uma segunda tentativa gravada como primeira levanta `IntegrityError` em vez de
  inflar a estatística em silêncio.
- **`registrar_tentativa()` calcula o `n_tentativa` internamente**, com
  `MAX(n_tentativa) + 1`. O chamador não pode passar esse número — verificado por
  teste com `inspect.signature`. `COUNT(*) + 1` foi descartado: apagar uma linha
  do meio faria dois registros receberem o mesmo número.
- **Duas métricas distintas, propositalmente:**
  - `dominio_modulo()` divide pelo **total** de questões → mede *progresso*.
  - `dominio_sobre_vistas()` divide pelas **vistas** → mede *desempenho*.

  Reforço e pontos fracos usam a segunda, e só julgam com pelo menos 30% do
  módulo visto.
- **Atividade diária derivada de `tentativas`**, não de contadores paralelos. A
  tabela `sessoes` do esquema existe e está sem uso — uma verdade só.

### Modelo pedagógico

- **`pedagogy.questao_para_exibir()` remove** `correta`, `explicacao`,
  `por_que_erradas`, `ordem_correta` e `pares`. A tela nunca recebe o gabarito —
  não é disciplina da view, é o que o dado carrega.
- **Ordenação e pareamento são embaralhados na exibição.** O conteúdo grava os
  itens na ordem correta, então remover o campo não bastava: confirmar sem mexer
  acertaria. `_permutar()` usa semente derivada do id da questão —
  determinístico, testável, e nunca igual à ordem correta (se o sorteio cair
  nela, rotaciona).
- **Dica só após 20 s**, uma por clique. Quem pediu dica vale 0,5 no domínio.
- **Pergunta socrática entre o Confirmar e o resultado**, com opção de voltar.
- **`engine.modo_da_questao()`** decide `nova` / `revisao` / `leitura` — a tela
  não decide.
- **SRS conforme a tabela 6.3 da spec**: acerto limpo ×2,5, acerto com dica ×1,3,
  erro volta para 1 dia. Multiplicadores fixos; a coluna `facilidade` fica
  reservada.
- **Cadeado é por nível, não por módulo.** `pre_requisitos` do conteúdo é ordem
  sugerida — travar módulo por módulo prendia o nível 0 inteiro no primeiro.

### Embaralho das alternativas

- **A alternativa correta está no índice 0 em todas as questões escritas**, e a
  permutação acontece na exibição, não no arquivo. Foi assim que o defeito
  passou despercebido por 18 módulos: `mapa_de_exibicao()` só embaralhava
  ordenação e pareamento, e a resposta certa saía sempre na primeira linha da
  tela. Corrigido em `7908e99`.
- **`conferir()` e `feedback()` recebem o índice exibido** e traduzem para o
  índice do arquivo. A tela não conhece a tradução — mesma divisão de
  responsabilidade que já valia para ordenação e pareamento.
- Um teste trava a distribuição: a correta precisa cair nas quatro posições, e
  nenhuma pode concentrar mais de 40%. Hoje está em 20/26/28/26.

### Validação de conteúdo

- **Campos pedagógicos são esquema, não regra de qualidade.** Questão sem
  `pergunta_socratica`, `dicas`, `explicacao`, `fonte` ou com distrator não
  justificado em `por_que_erradas` **não carrega**.
- **Regra de cobertura de objetivos**: cada questão declara quais objetivos do
  módulo ela testa (`objetivos: [índices]`), e objetivo declarado sem nenhuma
  questão reprova o módulo. Já pegou dois erros reais durante a escrita.
- **`test_qualidade_conteudo.py` é parametrizado por módulo** — módulo novo entra
  no teste sozinho: 35–60 questões, 4–8 blocos de teoria, no mínimo 4 tipos,
  nenhuma alternativa repetida, índice `correta` válido, todo distrator
  justificado, pré-requisitos existentes.

### Interface

- **`theme.painel` nasce com `height=0`.** `CTkFrame` vazio tem 200 px de altura
  por padrão; painéis vazios somavam 450 px e empurravam a pergunta socrática
  para fora da tela.
- **Alternativas são frames clicáveis**, não botões: `CTkButton` não aceita
  `wraplength` no ctk 6.0.0, e alternativa longa precisa quebrar linha.
- **Ordenação por botões ▲▼ e pareamento por menu suspenso.** Sem arrastar: em Tk
  quebra, e o pedido era simples e sólido.
- **Barra de progresso sem `corner_radius` próprio** e com trilho em
  `BG_PRIMARY` — raio maior que a altura virava bolinha, e trilho da mesma cor da
  linha ficava invisível.

### Verificação de fato antes de escrever

- **O que dá para executar, executa.** Os módulos 2.5 e 2.6 saíram de laboratórios
  rodados na máquina: JWT HS256 montado à mão, token `alg:none` aceito por
  verificador que lê o `alg` do próprio token, confusão RS256→HS256 com par de
  chaves RSA gerado no openssl, vetores de HOTP (RFC 4226), TOTP (RFC 6238) e
  PKCE (RFC 7636), bits POSIX e saída real de `icacls`.
- **Artefato de questão é saída real, anonimizada.** Nome de máquina, usuário e
  SID reais viram `CONTOSO` e `ana.silva`; o formato da saída fica intacto. Um
  validador de conteúdo recusa o arquivo se algum dado pessoal escapar.
- **A linha de base de senha é o NIST SP 800-63B rev. 4** (2025), conferida na
  fonte: 15 caracteres para senha como fator único, 8 apenas dentro de MFA,
  `SHALL NOT` para regra de composição e para troca periódica.

### Processo

- **Uma fase por vez, com validação entre elas.** Commit ao fim de cada fase.
- **Relatório separando fato verificado × escrito de memória** em todo bloco de
  conteúdo. É o que está segurando a qualidade factual.
- **Fatos verificáveis são executados antes de virarem questão**: comandos de
  shell, código Python, comportamento do Git, números de rede, colisão de MD5.

---

## 4. O que está pronto

### Fases da especificação

| Fase | Entrega | Estado |
|---|---|---|
| 1 | Esqueleto: janela, tema, navegação lateral | pronta |
| 2 | Camada de dados: 5 tabelas + índice parcial, validação de JSON | pronta |
| 3 | Motor: `engine.py` e `pedagogy.py` | pronta |
| 4 | Conteúdo dos níveis 0 e 1 (11 módulos) | pronta |
| 5 | Telas de sessão, trilha, home, módulo e progresso | pronta (antecipada) |
| 6 | Nível 2 + glossário + ferramentas | parcial: nível 2 completo; glossário e ferramentas pendentes |
| 7 | Níveis 3 e 4 + desafios práticos | em andamento: 3.1–3.3 e 4.1–4.4 prontos |
| 8 | Nível 5 + simulado + trilha de 90 dias | pendente |
| 9 | Ícone, atalho, README, publicação | pronta |

### Conteúdo escrito

**Nível 0 — Alicerce** (141 questões)
0.1 O que é cibersegurança · 0.2 Superfície de ataque · 0.3 Quem é o adversário ·
0.4 Ética, escopo e lei

**Nível 1 — Base técnica** (245 questões)
1.1 Linux essencial · 1.2 Linha de comando e shell · 1.3 Windows e Active
Directory · 1.4 Redes I · 1.5 Redes II · 1.6 Python para segurança ·
1.7 Git e versionamento

**Nível 4 — Defensivo** (280 questões, 8 de 8, completo)
4.1 Hardening · 4.2 Segurança de rede · 4.3 Defesa em profundidade · 4.4 Malware ·
4.5 SIEM e monitoramento · 4.6 MITRE ATT&CK e caça a ameaças ·
4.7 Resposta a incidentes · 4.8 Forense digital

**Nível 3 — Ofensivo** (281 questões, 8 de 9)
3.1 Metodologia de pentest · 3.2 OSINT e reconhecimento ·
3.3 Varredura e enumeração · 3.4 Web I · 3.5 Web II · 3.6 Web III ·
3.7 OWASP Top 10 · 3.8 Quebra de senhas

**Nível 2 — Núcleo de segurança** (245 questões, completo)
2.1 Criptografia I · 2.2 Criptografia II · 2.3 Criptografia III ·
2.4 Hash e senhas · 2.5 Autenticação e identidade · 2.6 Controle de acesso ·
2.7 Fator humano

### Telas funcionando

- **Início** — streak, meta diária selecionável (10/20/30), botão "Estudar
  agora", pontos fracos, próximo módulo sugerido
- **Trilha** — mapa dos 6 níveis, cadeado nos bloqueados, domínio por módulo
- **Sessão** — fluxo pedagógico completo, três modos, ordenação e pareamento
- **Módulo** — abas Teoria e Questões, "Refazer do zero" com cancelamento e aviso
- **Progresso** — heatmap anual em Canvas, domínio por nível, tópicos fracos

---

## 5. O que falta

### Conteúdo — 7 módulos

- **Nível 3 — Ofensivo** (1 restante): redes sem fio (3.9, fecha o nível)
- **Nível 4 — Defensivo**: completo (8 de 8)
- **Nível 5 — Engenharia e carreira** (6): desenvolvimento seguro, nuvem,
  modelagem de ameaças, GRC, economia da segurança, carreira

### Decisão de escopo — engenharia social não vira módulo novo, nível 3 fecha com 9 (não 10)

O roadmap original previa "engenharia social e redes sem fio" como um único
módulo do nível 3. Levantamento de não-repetição (medição por contagem de
menções nos 34 módulos publicados, não intuição — ver
`data/rascunhos/nivel-3/fontes/nao-repetir-3.9.md`) mostrou uma assimetria
severa: **engenharia social já tem dono** e **redes sem fio não tinha
nenhum**.

O módulo **2.7 ("Fator humano — por que a segurança falha nas pessoas") já
é, na prática, um módulo de engenharia social completo**: objetivo 2 nomeia
literalmente "phishing, pretexting e fraude de e-mail corporativo (BEC)";
`2.7.t5` tem título literal "Persuasão profissional, engenharia social e
phishing" (Cialdini, Stajano e Wilson, pretexting com caso real, definição
de BEC); tailgating não é menção solta, tem questão própria com mecanismo e
defesa (`2.7.q26`). Buscados também `1.1` e `4.4`, indicados como possíveis
pontos de toque: zero menção a engenharia social, phishing, pretexto ou
vetor humano em qualquer um dos dois.

Um recorte de "engenharia social como avaliação/teste autorizado" foi
proposto e **rejeitado**: consentimento de alvo e regra de engajamento já
são do **3.1** (objetivo 1, `3.1.t4`/`t5`); aplicar OSINT à construção de
pretexto já seria extensão de **3.2**; o que sobraria de território
genuinamente livre — vishing, voz sintética/deepfake, desenho de métrica de
campanha de conscientização — não sustenta 35 questões honestas sozinho.
Preenchê-lo até 35 seria exatamente o enchimento de linguiça que o
levantamento do 3.7 já tinha decidido evitar.

**Decisão**: o item do roadmap está cumprido pelo 2.7. Não haverá módulo
"3.9 Engenharia social". **O nível 3 fecha com 9 módulos, não 10** — o nono
e último é **3.9 Redes sem fio**, único dos dois assuntos com território
livre confirmado por medição.

**Dívida registrada, medida e não corrigida**: vishing, voz sintética/
deepfake como vetor de pretexto, e desenho/métrica de campanha de simulação
de phishing (o lado de quem constrói o programa de conscientização, não de
quem é o alvo) são território real e livre, mas finos demais para módulo
próprio. Candidatos a **bloco extra dentro do 2.7**, se ele for reaberto um
dia — nunca a módulo novo.

O próximo bloco natural é o nível 3, que desbloqueia com 70% no nível 2 —
agora completo. Bloco Web (3.4–3.6) fechado, o 3.7 (OWASP Top 10) fechado em
cima dele — a lista como instrumento (metodologia, posição, vocabulário,
ponto cego, mapeamento), não como catálogo de siglas reensinadas; sete das
dez categorias já tinham dono de mecanismo em outro módulo, medido antes de
escrever — e o 3.8 (Quebra de senhas) fechado logo depois: a economia do
ataque (on-line×off-line, custo = tentativas/s × espaço de busca,
previsibilidade humana, ataque estruturado, o que "quebrado" significa),
não a defesa em si, que já é do 2.4/2.5. Falta só o 3.9 (Redes sem fio,
único módulo restante — engenharia social já é o 2.7, ver decisão de
escopo acima) para fechar o nível 3 inteiro, em 9 módulos.

### Funcionalidades

- `data/glossario.json`, `data/ferramentas.json`, `data/desafios.json` e as três
  views correspondentes (hoje stubs)
- Simulado cronometrado de 40 questões com relatório por tópico
- Modo "Trilha de 90 dias"
- Modo reforço como entrada própria
- Retomar sessão interrompida (spec 6.5) — precisa persistir a posição da fila
- Navegação por teclado na sessão: 1-4, Enter, D, Esc

### Dívidas conhecidas

- **Texto não reflui ao redimensionar a janela.** `wraplength` é em pixels fixos.
  O helper `theme.texto()` existe e resolve; não foi aplicado às ~21 chamadas
  porque o layout está correto no DPI atual (1,25).
- **Tabela `sessoes` sem uso** — mantida por ser obrigatória na spec.
- **Coluna `facilidade` do SRS parada em 2,5** — a spec fixa os multiplicadores.
- **Duas exceções ao padrão de formato**, ambas dentro do esquema: o módulo 2.6
  tem 5 objetivos em vez de 4 (mecanismo de permissão × política ganhou objetivo
  próprio) e o 2.7 tem 7 blocos de teoria em vez de 6 (autenticação de e-mail:
  SPF, DKIM e DMARC).
- **Streak recalcula dias passados com a meta atual.** Guardar a meta de cada dia
  exigiria outra tabela.
- **O relatório de procedência do 3.3 nunca foi escrito.** Os outros dois estão
  em `data/rascunhos/nivel-3/relatorios/`; o do 3.3 se perdeu quando o processo
  foi interrompido. A verificação em si foi refeita e está registrada na mensagem
  do commit `48f9dd7`.
- **Dica que reescreve a alternativa correta** é o defeito recorrente do projeto:
  4 casos no 3.1, 6 no 3.2, 13 no 3.3 e 17 no 4.1, todos corrigidos na revisão.
  As regras do validador pegam a versão literal dele; a paráfrase, que é a
  maioria, continua dependendo de leitura. No 4.1 o defeito apareceu mesmo com a
  regra escrita no encargo do autor.
- **Sete pares de questões que ensinam a mesma coisa**, achados pela regra 5 em
  22/08/2026 e ainda não tratados. Os mais fortes: `2.3.q31` × `2.4.q14` (90% do
  vocabulário em comum), `2.3.q9` × `2.4.q14` (80%) e `1.2.q6` × `1.6.q6` (77%).
  Decidir, em cada par, qual questão fica e para onde a outra é repontada.
- **A dica que parafraseia o gabarito continua sendo o defeito mais teimoso do
  projeto — o que acabou foi o molde, não o defeito.** A **regra 6** acusa a
  fôrma "Pergunte ⟨a pergunta cuja única resposta é o gabarito⟩" por forma, e as
  179 ocorrências do corpus foram auditadas uma a uma em 24/08/2026: **141
  reescritas** (79%) e **38 aceitas** (21%), com justificativa em
  `ferramentas/avisos_aceitos.json`. O critério foi o efeito, não a sintaxe:
  reescrever quando a dica contém uma proposição que, se acreditada, identifica
  unicamente a alternativa correta; aceitar quando ela apenas nomeia um eixo ou
  um teste que ainda precisa ser aplicado às quatro opções. A regra segue de
  forma e **não alcança a paráfrase que dispensa o molde** — a leitura humana
  continua sendo a única rede para esses casos, e o passivo deles é
  desconhecido.
- **Comprimento da alternativa correta: dívida medida módulo a módulo,
  substituindo as estimativas antigas.** `python -m ferramentas.chutador_de_forma`
  roda a estratégia `mais_longa` (escolhe a alternativa com mais caracteres,
  sem ler nada) contra cada módulo publicado e mede a taxa de acerto contra o
  acaso de 25%. Medido em 01/09/2026, ordenado do pior para o melhor —
  **nível 0 inteiro corrigido (0.1 piloto + 0.2/0.3/0.4 em 01/09/2026), os
  outros 11 seguem como estavam**:

  | módulo | taxa `mais_longa` | status (teto 40%) |
  |---|---|---|
  | 2.6 | 78,1% | acima |
  | 2.7 | 62,5% | acima |
  | 4.2 | 62,5% | acima |
  | 3.1 | 58,1% | acima |
  | 1.1 | 56,2% | acima |
  | 1.2 | 56,2% | acima |
  | 2.5 | 56,2% | acima |
  | 1.3 | 46,9% | acima |
  | 3.2 | 46,9% | acima |
  | 3.3 | 46,9% | acima |
  | 4.1 | 43,8% | acima |
  | 3.5 | 39,3% | ok (módulo novo, 02/09/2026 — 52,9% no checkpoint 2 da regra 7, corrigido antes de seguir) |
  | 0.1 | 35,5% | ok (era 61,3% — piloto de correção, ver abaixo) |
  | 0.2 | 35,5% | ok (era 45,2%) |
  | 0.3 | 35,5% | ok (era 41,9%) |
  | 0.4 | 35,5% | ok (era 45,2%) |
  | 1.5 | 35,5% | ok |
  | 1.7 | 34,4% | ok |
  | 3.4 | 33,3% | ok (módulo novo, 02/09/2026 — 36,7% no checkpoint final da regra 7, baixou depois da revisão adversarial) |
  | 1.4 | 32,3% | ok |
  | 4.4 | 31,2% | ok |
  | 2.1 | 28,1% | ok |
  | 2.2 | 28,1% | ok |
  | 1.6 | 27,3% | ok |
  | 4.7 | 23,3% | ok (módulo novo, 02/09/2026 — corrigido pelo checkpoint da regra 7 antes de publicar) |
  | 2.3 | 21,2% | ok |
  | 2.4 | 21,2% | ok |
  | 4.5 | 19,4% | ok |
  | 4.3 | 15,6% | ok |
  | 4.6 | 15,6% | ok |
  | 3.6 | 13,8% | ok (módulo novo, 03/09/2026 — o viés reapareceu nos três checkpoints da regra 7, corrigido a cada vez antes de seguir) |
  | 4.8 | 12,9% | ok (módulo novo, 02/09/2026) |
  | 3.7 | 3,2% | ok (módulo novo, 04/09/2026 — rascunho nasceu em 97,0%, causa raiz era `correta` fixo no índice 0 em toda questão; corrigido por rotação de posição + reequilíbrio de comprimento antes do primeiro checkpoint) |
  | 3.8 | 18,8% | ok (módulo novo, 05/09/2026 — viés recorreu nos três lotes de escrita: 62,5%→50%→44% antes de cada correção; publicado bem abaixo do teto) |

  **11 de 31 módulos acima do teto de 40%** (era 15 antes do nível 0; nível
  0 (0.1-0.4) está inteiro abaixo do teto agora; 4.7, 4.8, 3.4 e 3.5,
  publicados depois desta medição original, também ficaram abaixo). O teto não é palpite:
  batia, módulo a módulo, com o critério estatístico independente de "o
  limite inferior do intervalo de Wilson (95%) da taxa passa de 25%" antes
  desta rodada — justificativa completa em `ferramentas/chutador_de_forma.py`,
  comentário de `TETO_MAIS_LONGA`.

  Isto substitui a varredura manual anterior (parcial, níveis 0-1 e módulos
  2.1-2.4, baseada em contagem direta de "a correta é a mais longa" em vez de
  taxa de acerto de uma estratégia): os números não são diretamente
  comparáveis porque o método mudou, mas a lista acima é a atual e é a que
  vale — os 11 módulos acima do teto são o alvo de correção, ainda não
  corrigidos.

  **Segundo eixo de dívida medida — `evita_absoluto`, 02/09/2026.** A
  revisão adversarial do módulo 4.8 achou qualificador absolutista
  ("nunca", "sempre", "automaticamente", "por padrão") só em alternativas
  **erradas**, nunca na correta — a mesma regra 6 do checklist do README
  ("afirmação absoluta não serve de distrator"), violada porque nenhum
  mecanismo automático a verificava. Diferente da regra 7 removida
  (dígito/negação), este achado não precisou de nova investigação: a
  estratégia `evita_absoluto` já existia no chutador desde 01/09/2026,
  criada durante a investigação da regra 7, e já tinha sido medida como
  sinal real contra o corpus inteiro (41-43%, bem acima do acaso). Só
  faltava rodar contra os 29 módulos atuais e decidir o teto — feito
  nesta rodada, **sem corrigir nenhuma questão**:

  | módulo | taxa `evita_absoluto` | IC95 (limite inferior) | status (teto 40%) |
  |---|---|---|---|
  | 2.6 | 65,6% (21/32) | 48,3% | acima |
  | 4.2 | 65,6% (21/32) | 48,3% | acima |
  | 1.2 | 62,5% (20/32) | 45,3% | acima |
  | 3.1 | 61,3% (19/31) | 43,8% | acima |
  | 2.5 | 59,4% (19/32) | 42,3% | acima |
  | 2.7 | 59,4% (19/32) | 42,3% | acima |
  | 0.1 | 54,8% (17/31) | 37,8% | **acima — dívida nova, não vista na medição de `mais_longa`** |
  | 1.3 | 53,1% (17/32) | 36,4% | acima |
  | 3.3 | 50,0% (16/32) | 33,6% | acima |
  | 1.1 | 45,2% (14/31) | 29,2% | acima |
  | 3.2 | 43,8% (14/32) | 28,2% | acima |
  | 4.1 | 40,6% (13/32) | 25,5% | acima |
  | 4.6 | 38,7% (12/31) | 23,7% | ok |
  | 4.4 | 37,5% (12/32) | 22,9% | ok |
  | 0.3 · 0.4 · 1.4 · 4.5 | 35,5% (11/31) | 21,1% | ok |
  | 4.7 | 34,5% (10/29) | 19,9% | ok |
  | 1.7 | 34,4% (11/32) | 20,4% | ok |
  | 1.6 | 33,3% (11/33) | 19,8% | ok |
  | 1.5 | 32,3% (10/31) | 18,6% | ok |
  | 0.2 | 29,0% (9/31) | 16,1% | ok |
  | 3.5 | 28,6% (8/28) | 15,3% | ok (módulo novo, 02/09/2026) |
  | 2.1 | 28,1% (9/32) | 15,6% | ok |
  | 2.3 | 27,3% (9/33) | 15,1% | ok |
  | 2.2 · 4.8 | 25,8% (8/31) | 13,7% | ok |
  | 3.4 | 23,3% (7/30) | 10,7% | ok (módulo novo, 02/09/2026) |
  | 2.4 | 18,2% (6/33) | 8,6% | ok |
  | 4.3 | 15,6% (5/32) | 6,9% | ok |
  | 3.6 | 13,8% (4/29) | 5,5% | ok (módulo novo, 03/09/2026) |
  | 3.7 | 25,8% (8/31) | 12,6% | ok (módulo novo, 04/09/2026) |
  | 3.8 | 19,4% (6/31) | 9,2% | ok (módulo novo, 05/09/2026) |

  **Mediana do corpus: 35,5%.** O teto de 40% não foi escolhido de novo —
  foi conferido contra o mesmo critério estatístico independente já usado
  para `mais_longa` (limite inferior do IC95 de Wilson passa de 25% de
  acaso), e os dois critérios **convergem exatamente**: o último módulo
  com sinal estatístico (4.1, 40,6%) fica acima de 40%, o primeiro sem
  sinal (4.6, 38,7%) fica abaixo. Mesma coincidência de dois critérios
  independentes que já validou o teto de `mais_longa` — não é palpite
  reaplicado, é o mesmo teste rodado de novo com resultado igual.

  **12 de 31 módulos acima do teto de 40% em `mais_longa` OU
  `evita_absoluto`** — 11 já conhecidos por `mais_longa`, mais **0.1**,
  que cruza só por `evita_absoluto` (54,8%) apesar de já ter sido
  corrigido para `mais_longa` no piloto de 01/09/2026. `ferramentas/chutador_de_forma.py`
  agora mede as três estratégias por padrão (`mais_longa`, `mais_curta`,
  `evita_absoluto`) e reprova um módulo se qualquer uma cruzar o teto —
  portão único, não três ferramentas separadas. **Nenhuma questão foi
  corrigida nesta rodada**, incluindo em 0.1: é medição, o alvo de
  correção fica para quando a dívida de forma for tratada como bloco,
  junto com os 11 módulos de `mais_longa`.

  **Terceiro eixo medido — molde de dica, 03/09/2026 — triagem, não
  portão.** A revisão adversarial do 3.5 achou a mesma frase de abertura
  em `dicas[2]` nas 28 de 28 questões de múltipla escolha do módulo —
  quarta variante desta família nesta sessão (frase de autorrejeição no
  4.7, qualificador absolutista no 4.8, hedge solto no 3.4). Antes de
  virar regra, medido contra o corpus inteiro, seguindo a lição da seção
  abaixo: `ferramentas/medidor_molde_dica.py` conta, por módulo e por
  índice de dica (0, 1 ou 2), a maior família de questões cujas dicas
  começam com as mesmas 5 palavras (N=5 escolhido e testado contra N=3 e
  N=8 sem mudar o ranking — ver comentário no arquivo).

  Resultado nos 31 módulos publicados até então: mediana 5,7%, a maioria
  abaixo de 6%, com três destaques reais — **3.4, 20,0% (7/35,
  "só uma alternativa aponta para" em `dicas[2]`, achado NOVO, não
  reportado na revisão adversarial daquele módulo)**, **4.8, 17,1%**
  ("pense no laboratório desta sessão" em `dicas[0]`) e **4.7, 11,4%**
  (resíduo do mesmo molde do 3.4, depois de já corrigido em 15 questões
  na publicação original).

  **Veredito, honesto: sustenta como ferramenta de triagem — não como
  teto automático de reprovação como `mais_longa`/`evita_absoluto`.**
  Diferença do caso da regra 7 (dígito/negação): aqui não há "acaso" a
  vencer — cinco palavras idênticas por coincidência linguística é quase
  impossível, então qualquer família ≥2 já é sinal real, não ruído
  estatístico. O motivo de não virar portão é outro, e seguindo a mesma
  disciplina desta seção — nomear o limite conhecido, como já existe para
  a regra 6 (README, "a leitura humana continua sendo a rede" para o que
  a regra 6 não alcança): **o medidor só pega o PREFIXO EXATO repetido.
  Trocar uma palavra ("alternativa"→"opção") zera a família de forma
  inteira sem eliminar o molde** — um módulo pode pontuar 0% aqui e ainda
  ter o defeito inteiro, só variado. Baixa contagem (2-3) também pode ser
  convenção legítima de tipo de questão, não vazamento (ex.: "compare as
  quatro opções pelo" em 3.1/3.2/3.3). Os dois casos exigem leitura para
  decidir — a régua automática não distingue.

  Adotado como parte do checklist de checkpoint (8ª, 20ª, final) a partir
  do 3.6, reportando a taxa junto com as outras três, mas sem reprovar
  módulo por ela sozinha.

  **Achado do 3.4 registrado como dívida medida e NÃO corrigida nesta
  rodada**: "Só uma alternativa aponta para" idêntico em `dicas[2]` de 7
  questões (`3.4.q4`, `q7`, `q12`, `q13`, `q23`, `q28`, `q32`) — 20,0% de
  família, a maior do corpus. É medição, não correção: fica registrado
  aqui para quando a dívida de forma do 3.4 for tratada como bloco.

  **Sexta variante, achada manualmente no 3.7, 04/09/2026 — confirma o
  limite já registrado acima.** O medidor não achou nada no rascunho do
  3.7 (pior família 5,6%), mas uma varredura manual por abertura semântica
  (em vez de prefixo exato) achou "Pense em/no/na..." ou "Volte a [id]..."
  em **23 das 108 dicas (21%)** — invisível à ferramenta porque cada
  ocorrência referencia um id diferente ("Volte a 2.3", "Volte a t4"),
  então só os 2 primeiros tokens repetem, não os 5 que o medidor exige.
  Reescritas 12 das 23; concentração final 10%. Prova, na prática, o que
  a seção acima já previa: o medidor mede o que sabe medir, não o molde
  inteiro.

  **Piloto de correção — módulo 0.1, 01/09/2026.** Escolhido por ser o
  primeiro módulo do curso (vazamento ali contamina a base inteira) e por
  ser pequeno o bastante para calibrar o método antes dos outros 14. Rodada
  única, sem varredura em série — a varredura anterior parou pela metade por
  ter começado grande demais.

  Classificação dos 19 achados de `mais_longa` do chutador (uma questão a
  mais que a contagem estrita do validador, por causa de um empate técnico
  exato — ver abaixo). Limite de julgamento em razão 1,2×: abaixo disso é
  empate técnico, mesmo padrão já usado na varredura de 2.1-2.4:

  | categoria | contagem | questões |
  |---|---|---|
  | empate técnico (razão < 1,2×, não tocado) | 7 | `0.1.q5` `0.1.q7` `0.1.q8` `0.1.q15` `0.1.q20` `0.1.q22` `0.1.q35` |
  | (a) CORTAR DA CORRETA | 3 | `0.1.q9` `0.1.q21` `0.1.q27` |
  | (b) ENGORDAR O DISTRATOR | 4 | `0.1.q17` `0.1.q24` `0.1.q31` `0.1.q36` |
  | (c) LEGÍTIMO, ratio ≥ 1,2× mas não tocado | 5 | `0.1.q10` `0.1.q13` `0.1.q18` `0.1.q26` `0.1.q29` |

  Os 5 de (c) ficaram sem correção porque, mesmo com razão entre 1,25× e
  1,30×, as 7 correções de (a)/(b) já eram suficientes para cruzar o teto de
  40% — corrigi-los também zeraria a métrica em vez de só tirar o sinal, o
  que o passo 2 pediu explicitamente para não fazer. `0.1.q24` e `0.1.q31`
  já constavam da lista antiga de "classe (b)" da varredura de 2.1-2.4
  (então mantive a classificação anterior, feita à mão, em vez de reabrir o
  julgamento); os outros 5 achados de (a)/(b)/(c) com ratio ≥ 1,2× não
  tinham classificação prévia.

  Resultado: **7 questões tocadas** (3 cortes na correta, 4 distratores
  engordados) — nenhuma alternativa nova, nenhum tipo de questão trocado,
  nenhuma dica ou explicação reescrita (só duas justificativas em
  `por_que_erradas` ajustadas para acompanhar o texto novo do distrator).

  | métrica | antes | depois |
  |---|---|---|
  | `mais_longa` (chutador) | 61,3% (19/31) | 38,7% (12/31) |
  | `mais_longa` (validador, contagem estrita) | 58,1% (18/31) | 35,5% (11/31) |
  | `mais_curta` (chutador, novo — ver seção "ajuste de método") | não medido | 6,5% (2/31) |

  `mais_curta` baixo confirma que a correção não empurrou o viés para o
  lado oposto — a correta ficou no meio da distribuição dos distratores,
  não virou a mais curta com frequência.

  **Validação:** `python -m pytest -q` (3.113 testes, 0 falhas) e
  `python ferramentas/validar_modulo.py data/modulos/00-01-o-que-e-ciberseguranca.json`
  rodados antes e depois — o único aviso que sobrevive
  (`0.1.q8` divide vocabulário com `1.6.q19`) já existia antes da correção;
  nenhum aviso novo apareceu, e o aviso de comprimento (que existia antes)
  desapareceu por ficar abaixo do teto.

  **Custo:** cerca de 40 minutos de trabalho de agente para classificar os
  19 achados, editar 7 alternativas e validar — a maior parte do tempo foi
  classificação (ler cada questão contra a explicação para decidir cortar
  vs. engordar), não a edição em si. Para os 14 módulos restantes, o número
  de achados de `mais_longa` (contagem bruta, não taxa) varia de 13 (0.3) a
  25 (2.6), média de 17 — perto do 0.1 (19), não muito maior. Projeção:
  cerca de 35-45 minutos por módulo na mesma proporção classificação/edição
  deste piloto, e mais tempo nos módulos com mais empate técnico pra
  descartar (0.1 teve 7 dos 19 nessa faixa) do que nos achados em si.

  **Ajuste de método no meio do caminho:** a estratégia `mais_curta` não
  existia no chutador antes deste piloto — foi adicionada durante esta
  rodada (`ferramentas/chutador_de_forma.py`) porque o risco de
  supercorreção (virar "a mais curta" o novo atalho) só vira mensurável com
  ela. Fica como parte permanente do portão para os próximos módulos, não
  como ferramenta descartável do piloto.

  **Nível 0 fechado — 0.2, 0.3, 0.4, 01/09/2026.** Piloto validado, mesmo
  método aplicado um módulo por vez, ordem de estudo (não de gravidade):
  os três eram baratos (delta pequeno até o teto). Nenhum módulo exigiu
  mais de 3 questões tocadas — bem abaixo do limite de 10 combinado com o
  usuário para parar e reportar.

  | módulo | achados `mais_longa` | empate técnico | tocadas | categoria |
  |---|---|---|---|---|
  | 0.2 | 14 | 3 | 3 | (b) `0.2.q15`; (a) `0.2.q20`, `0.2.q23` |
  | 0.3 | 13 | 4 | 2 | (a) `0.3.q30`, `0.3.q17` |
  | 0.4 | 14 | 7 | 3 | (b) `0.4.q3`, `0.4.q2`; (a) `0.4.q1` |

  | módulo | `mais_longa` antes → depois | `mais_curta` depois |
  |---|---|---|
  | 0.2 | 45,2% (14/31) → 35,5% (11/31) | 19,4% (6/31) |
  | 0.3 | 41,9% (13/31) → 35,5% (11/31) | 32,3% (10/31) — ver achado abaixo |
  | 0.4 | 45,2% (14/31) → 35,5% (11/31) | 25,8% (8/31), no acaso |

  Duas iterações no meio da edição, ambas pegas antes de commitar, não
  depois:

  - **0.2.q23** — o primeiro corte deixou a correta com 52 caracteres
    contra distratores de 59-69: virou a mais curta das quatro, o mesmo
    defeito do lado oposto. Recalibrado pro meio da distribuição (67
    caracteres). É exatamente o motivo de medir `mais_curta` depois de
    cada corte, não só no fim do módulo.
  - **0.2.q23** (mesma questão) — a reescrita também reintroduziu a regra
    1 (dica 3 ecoando "alcançável"/"a partir" que entraram no texto
    novo da correta). Trocado o vocabulário sem tocar a dica.

  Dois casos com razão alta (0.4.q21 1,86× e 0.4.q28 1,61×) foram
  classificados (c) LEGÍTIMO e não tocados: são enumerações legais
  fechadas (categorias de dado sensível da LGPD art. 5º II; verbos do
  art. 154-A do Código Penal) — cortar arrisca imprecisão jurídica, e
  engordar um distrator ao lado de uma lista legal precisa confundiria o
  próprio ponto pedagógico da questão.

  **Achado do 0.3 — resolvido em 02/09/2026, ruído, questão encerrada.**
  `mais_curta` do módulo 0.3 estava em 32,3% (10/31), acima do acaso de
  25%, medido antes da edição do 0.1-0.4 e não criado pelas 2 questões
  tocadas nele. Para decidir se era caso isolado ou padrão de corpus,
  rodei `mais_curta` contra os 27 módulos publicados e apliquei o mesmo
  critério estatístico já usado para `mais_longa` (intervalo de Wilson
  95%, "tem sinal" quando o limite inferior passa do acaso de 25%):

  | módulo | `mais_curta` | IC95 (limite inferior) | sinal > acaso? |
  |---|---|---|---|
  | 4.3 | 46,9% (15/32) | 30,9% | **sim** |
  | 4.4 | 37,5% (12/32) | 22,9% | não |
  | 0.3 | 32,3% (10/31) | 18,6% | não |
  | 1.4 | 32,3% (10/31) | 18,6% | não |
  | 1.1 | 31,2% (10/32) | 18,0% | não |
  | 1.7 | 28,1% (9/32) | 15,6% | não |
  | 0.4 | 25,8% (8/31) | 13,7% | não |
  | 1.6 | 24,2% (8/33) | 12,8% | não |
  | 2.4 | 21,2% (7/33) | 10,7% | não |
  | 0.2 | 19,4% (6/31) | 9,2% | não |
  | 2.7 | 18,8% (6/32) | 8,9% | não |
  | 1.2 | 18,8% (6/32) | 8,9% | não |
  | 2.5 | 18,8% (6/32) | 8,9% | não |
  | 1.5 | 16,1% (5/31) | 7,1% | não |
  | 3.1 | 12,9% (4/31) | 5,1% | não |
  | 1.3 | 12,5% (4/32) | 5,0% | não |
  | 3.2 | 12,5% (4/32) | 5,0% | não |
  | 4.1 | 12,5% (4/32) | 5,0% | não |
  | 2.1 | 12,5% (4/32) | 5,0% | não |
  | 2.3 | 12,1% (4/33) | 4,8% | não |
  | 2.2 | 9,4% (3/32) | 3,2% | não |
  | 0.1 | 6,5% (2/31) | 1,8% | não |
  | 2.6 | 6,2% (2/32) | 1,7% | não |
  | 4.2 | 6,2% (2/32) | 1,7% | não |
  | 4.6 | 6,2% (2/32) | 1,7% | não |
  | 3.3 | 0,0% (0/32) | 0,0% | não |
  | 4.5 | 0,0% (0/31) | -0,0% | não |

  **Mediana do corpus: 16,1%, abaixo do acaso de 25%** (não perto dele —
  o corpus, como um todo, não tem viés de `mais_curta`, se é que tem
  algum viés de comprimento é no sentido `mais_longa`, já rastreado).
  Aplicando ao 0.3 o mesmo rigor estatístico que valida a lista de
  `mais_longa` (evitar medir contra a amostra que já suspeita de si
  mesma — o mesmo princípio da seção 7), **o IC95 do 0.3 inclui o
  acaso: não é sinal, é ruído de amostra pequena (31 questões).**
  Questão encerrada, nenhuma correção necessária.

  **Achado novo, não relacionado ao 0.3: módulo 4.3 (Defesa em
  profundidade) tem viés real de `mais_curta`, 46,9% (15/32), IC95
  30,9%-62,9%, cruza inclusive o teto de 40% usado para `mais_longa`.**
  É o único módulo do corpus com sinal estatístico independente nesse
  eixo — e é justamente um dos módulos "limpos" pela métrica de
  `mais_longa` (15,6%, ok). Dívida nova, medida, **não corrigida nesta
  rodada** por decisão explícita: o foco atual é escrever os 14 módulos
  que faltam, não polir os 11 (mais este) que já existem.

  **Nenhum defeito de conteúdo (fato errado, fonte desatualizada,
  gabarito discutível) foi notado durante a leitura de 0.2, 0.3 ou 0.4.**
  Fontes citadas (MITRE ATT&CK, NIST CSF, CIS Benchmarks, Código Penal
  art. 154-A, LGPD art. 5º II, Marco Civil arts. 13/15) pareceram
  corretas e consistentes com a explicação de cada questão.

  Validação em cada módulo: `pytest -q` (3.113 testes, 0 falhas em cada
  um dos três) e `validar_modulo.py` antes/depois — nenhum aviso novo em
  nenhum dos três; os únicos avisos que sobrevivem são pré-existentes e
  não relacionados às questões tocadas (`0.4.q28` × `3.2.q35`, vocabulário).
  Três commits, um por módulo.
- **O atalho da área de trabalho aponta para o Python do sistema.** Se um dia
  existir `.venv` na pasta, o atalho continuará usando o Python global; o
  `run.bat` é quem prefere a `.venv`.
- ~~Regra 7 — unicidade estrutural (dígito, negação)~~ — **removida em
  01/09/2026, não é dívida.** A amostra manual de 31/08 (73% "vazamento
  real") e a medição por agente cego de 31/08 (dois grupos no teto, sem
  sinal) não bastaram para decidir — nenhuma das duas media a heurística
  contra o corpus inteiro, só contra o subconjunto que a própria regra
  definia. Um chutador determinístico (`ferramentas/chutador_de_forma.py`,
  sem ler `correta`) mediu a taxa de acerto de "escolher a única alternativa
  com dígito/negação" contra as 859 questões do corpus inteiro: 27,2% e
  27,0% para negação, 19,8% e 10,0% para dígito — todos com intervalo de
  confiança cobrindo os 25% de acaso. A marca não prediz a resposta certa
  fora do conjunto circular que a define. Os 96 achados (10 dígito + 86
  negação) não são dívida de conteúdo e nenhuma questão foi reescrita por
  causa deles. Ver `ferramentas/relatorio_regra7_chutador.md` para a
  metodologia completa e o padrão aprendido na seção 7 abaixo.
- **Módulo 4.7 escrito, 02/09/2026 — resposta a incidentes como decisão sob
  pressão, não fases decoradas.** Recorte final: autoridade de decisão
  pré-combinada, custo de agir com informação incompleta, comunicação como
  cadeia técnica interna (sincronizada com o prazo do 0.4, sem repeti-lo),
  pós-incidente que verifica mudança real. Duas colisões reais achadas no
  levantamento de não-repetição, não previstas no pedido original — eixo
  de contenção colidia com 4.4 (9 questões já cobrem isolar-vs-desligar) e
  eixo de comunicação colidia com 0.4 (prazo ANPD já ensinado) — os dois
  eixos foram reformulados antes de qualquer questão escrita; ver
  `data/rascunhos/nivel-4/fontes/nao-repetir-4.7.md`.

  **Regra 7 (checkpoint de comprimento nas 8 primeiras questões) confirmou
  o defeito pela terceira vez** (depois de 4.5 e 4.6): 100% das corretas
  eram a mais longa nas primeiras 8. Corrigido ali para 14,3% — mas o
  hábito não generalizou para as 27 questões seguintes, e o módulo
  terminou em 77% (23/30). Uma correção automática (corte no último
  travessão da correta, ou engorda do distrator mais curto) trouxe a taxa
  para dentro do teto, mas introduziu um defeito novo: 15 distratores
  passaram a compartilhar a mesma frase-molde de autorrejeição, um sinal
  de forma detectável sem ler o conteúdo. A revisão adversarial de duas
  lentes (abaixo) pegou isso, e a correção final ficou em **23,3%
  mais_longa, 20,0% mais_curta**, sem padrão de forma repetido.

  **Duas lentes de revisão adversarial, em paralelo, por agentes sem
  contexto da escrita**, acharam e corrigiram: o defeito sistêmico de
  frase-molde acima (15 questões); duas dicas que vazavam premissa antes
  do aluno inferir sozinho; uma justificativa (`por_que_erradas`) que
  citava um fato não estabelecido pela própria questão; duas questões
  onde só a correta citava número/rompia o molde gramatical dos
  distratores; e **um erro factual real**: o laboratório
  `cadeia_de_comunicacao.py` tratava "3 dias úteis" (o que o 0.4 realmente
  ensina) como equivalente a "72 horas corridas" — não são a mesma
  grandeza. Corrigido na fonte (constante do laboratório, artefato da
  questão, justificativa), com o laboratório re-executado. Relatório
  completo em `data/rascunhos/nivel-4/relatorios/4.7.md`.

  Validação final: `pytest -q` (3.223 testes, 0 falhas) e
  `validar_modulo.py data/modulos/*.json` (exit 0, 0 falhas em 28
  módulos). +35 questões, +1 bloco de teoria por módulo (6), nível 4 em
  7 de 8 (falta só forense).
- **Módulo 4.8 escrito, 02/09/2026 — forense digital como evidência que
  precisa se sustentar, fecha o nível 4 (8 de 8).** Recorte final:
  aquisição sem alterar (efeito observador), integridade e cadeia de
  custódia como propriedade matemática, o que uma evidência sustenta e o
  que não sustenta, limites honestos (timestamp, atribuição). Uma
  colisão real achada no levantamento — eixo de "ordem de volatilidade"
  era quase o título literal de `4.4.q17` — reformulada antes de
  escrever para "aquisição sem alterar" (custo físico da captura, não
  ordem de prioridade); ver
  `data/rascunhos/nivel-4/fontes/nao-repetir-4.8.md`.

  **Mudança de processo desta sessão, aplicada pela primeira vez: regra
  7 medida em TRÊS pontos** (8ª, 20ª, 35ª questão), não só uma — decisão
  tomada depois do 4.7, em que um único checkpoint pegou o defeito cedo
  mas o hábito não generalizou (14,3% → 77% entre a 8ª e a 35ª). No 4.8
  os três checkpoints mediram 85,7%, 55,6% e 41,9% — o defeito voltou
  nos três, mas em lotes menores (7, 10 e 13 questões por vez, contra 23
  de uma vez no 4.7). Uma primeira correção automática no checkpoint 1
  **overcorrigiu** para 85,7% `mais_curta` (o mesmo risco que a seção 5
  já registrava desde o piloto do 0.1); ajustada manualmente para o meio
  da faixa em cada questão. Taxa final: **6,5% mais_longa, 3,2%
  mais_curta**.

  **Achado novo da revisão adversarial, não visto no 4.7: qualificador
  absolutista como pista de forma.** A lente 1 achou "nunca", "sempre",
  "automaticamente" ou "por padrão" em pelo menos uma alternativa
  **errada** de 20 das 35 questões, e em nenhuma correta — exatamente a
  regra 6 do checklist do README ("afirmação absoluta não serve de
  distrator... é curta por natureza e autorrefutável"), regra já
  documentada no projeto, violada sistematicamente porque **nenhum
  mecanismo automático a verifica** — só a leitura humana ou de agente
  pega. Corrigidas as 30 ocorrências, substituindo o absoluto por
  qualificação realista ("costuma", "raramente"). Fica registrado como
  candidato a extensão futura do `chutador_de_forma.py` (uma estratégia
  `unica_sem_absoluto`, no mesmo molde de `evita_absoluto`), não
  construída nesta sessão — ver seção "Padrão aprendido" abaixo antes de
  decidir se vale a pena: a lição da regra 7 removida é medir contra o
  corpus inteiro antes de automatizar, não só contra este achado.

  A lente 2 achou um defeito de paridade gramatical em `4.8.q16` (as
  três erradas compartilhavam sujeito/verbo, a correta mudava de
  sujeito) — corrigido igualando a forma sem mudar o conteúdo de cada
  alternativa. Relatório completo em
  `data/rascunhos/nivel-4/relatorios/4.8.md`.

  Validação final: `pytest -q` (3.334 testes, 0 falhas) e
  `validar_modulo.py data/modulos/*.json` (exit 0, 0 falhas em 29
  módulos). +35 questões, +1 bloco de teoria por módulo (6). **Nível 4
  completo, 8 de 8.**
- **Módulo 3.4 escrito, 02/09/2026 — Web I, por que a aplicação web é
  atacável por construção. Abre o nível 3 depois de 3.1-3.3.** Recorte
  final: decisão de segurança sempre no servidor; reenvio automático de
  cookie como o que torna CSRF possível; validação client-side como
  conveniência, não controle; regra de mesma origem e CORS como exceção
  controlada. Uma colisão severa achada no levantamento — o eixo 2
  original ("sessão é invenção sobre HTTP sem estado") era quase o
  objetivo declarado do 2.5, que já tem 8 questões sobre sessão e
  cookie — reformulada antes de escrever para "reenvio automático" (a
  consequência de CSRF, não a mecânica de sessão já ensinada); ver
  `data/rascunhos/nivel-3/fontes/nao-repetir-3.4.md`.

  Primeiro módulo escrito com o checkpoint de três estratégias completo
  (`mais_longa`, `mais_curta`, `evita_absoluto`, ver item abaixo).
  Checkpoints 1 e 2 repetiram o mesmo par de defeitos (comprimento e
  qualificador absolutista) nas questões recém-escritas de cada lote —
  100%/50% e 50%/50% respectivamente, corrigidos nos dois casos. O
  checkpoint final (35ª questão) **não precisou de correção de forma
  por si só**: 36,7% / 6,7% / 26,7%, as três já dentro do teto — primeira
  vez nesta linha de módulos que isso acontece, ainda cedo para chamar
  de hábito consolidado. A revisão adversarial (item abaixo) ainda assim
  encontrou e corrigiu resíduos de forma que o portão numérico não pega
  sozinho; depois dessas correções, o número final publicado é
  33,3% / 10,0% / 23,3%.

  Um dos quatro laboratórios (regra de mesma origem) foi verificado com
  **navegador real** (Chrome, via automação desta sessão), não só
  script Python — necessário porque a regra é aplicada pelo navegador,
  e um script sozinho (como curl) não reproduz esse bloqueio. Console e
  log de rede reais confirmam: sem cabeçalho CORS, leitura bloqueada
  (`Failed to fetch`); com cabeçalho liberando a origem, leitura
  normal — o servidor respondeu nos dois casos, a diferença é só o que
  o navegador deixa o script ler.

  A revisão adversarial achou uma variante nova do defeito de
  frase-molde do 4.7/4.8: em 3 questões, um inciso de hedge solto
  ("na maioria das versões recentes,", "em geral,") sobrevivia como
  resíduo da correção automática dos checkpoints — mesma família de
  problema (padrão de forma detectável sem ler conteúdo), forma
  diferente da frase-molde completa do 4.7. Mais um achado de
  justificativa citando evidência não mostrada ao aluno, e dois de
  precisão textual (acento faltando num artefato, citação cruzada
  exagerando o que o 2.5 realmente ensina) — todos corrigidos.
  Relatório completo em `data/rascunhos/nivel-3/relatorios/3.4.md`.

  Validação final: `pytest -q` (3.444 testes, 0 falhas) e
  `validar_modulo.py data/modulos/*.json` (exit 0, 0 falhas em 30
  módulos). +35 questões, +1 bloco de teoria por módulo (6). Nível 3
  em 4 de 9.
- **Módulo 3.5 escrito, 02/09/2026 — Web II, a confusão entre dado e
  instrução.** Ensina SQL injection, XSS e injeção de comando de sistema
  como **um único mecanismo** repetido em três canais — dado sem
  fronteira em relação à instrução — em vez de três tópicos separados;
  fecha com contraponto defensivo obrigatório (nenhuma camada sozinha
  basta: separação estrutural, menor privilégio, monitoramento). O
  levantamento de não-repetição achou uma colisão real com o 1.6
  (Python), que já ensina a defesa específica de injeção de comando com
  código testado — reformulado antes de escrever: o canal de sistema
  operacional entra como a prova mais nua do mecanismo, a defesa em si
  é referência cruzada ao 1.6, não reensinada; ver
  `data/rascunhos/nivel-3/fontes/nao-repetir-3.5.md`.

  Quatro laboratórios locais/em memória, sem payload pronto para colar:
  `O'Brien` (nome real, não ataque) quebra consulta SQL concatenada e
  funciona por parâmetro; tag `<b>` inofensiva chega intacta sem escape
  e vira texto literal com escape; `&` embutido num dado vira separador
  de comando real via `shell=True`, inofensivo via lista de argumentos;
  a mesma string testada nos dois canais prova que "perigoso" é uma
  relação string↔canal, não propriedade da string. Duas correções de
  laboratório encontradas só na execução real: um "payload" de comentário
  SQL (`' --`) engolia a própria aspa de fechamento e não demonstrava
  nada (reescrito em torno do `O'Brien` real); o separador de comando
  testado (`;`) não tem efeito no `cmd.exe` desta máquina Windows —
  `&` é o separador real aqui, descoberto testando ao vivo.

  Checkpoint 1 (8ª questão) repetiu o mesmo viés de comprimento visto em
  todo módulo novo desta sessão (100% `mais_longa` inicial), corrigido
  para 0%/0%/0%. Checkpoint 2 (20ª questão) **cruzou o teto em duas
  estratégias ao mesmo tempo** — 52,9% `mais_longa` e 47,1%
  `evita_absoluto` — nas 9 questões novas do lote, corrigido reescrevendo
  cada correta dentro do intervalo de comprimento das outras três, sem
  palavra absolutista nova. O checkpoint final (35 questões) nasceu
  dentro do teto sem correção de forma: 39,3% / 0% / 32,1%.

  A revisão adversarial (duas lentes, agentes paralelos) confirmou, pela
  quarta vez nesta sessão, que a forma do defeito de molde muda a cada
  correção: desta vez foi a frase-abertura de `dicas[2]` ("Só uma
  alternativa... sem inventar...") repetida em **28 de 28** questões de
  múltipla escolha, sem exceção — reescritas todas com estrutura
  sintática variada. Achou também um distrator de "torna mais lento"
  reciclado em 5 questões e um de "exigência legal" em 3, sempre errados
  (reduzidos a 1 ocorrência cada, restante reescrito), e um par de
  questões caça-erro (SQL e HTML) que eram **clones de molde**
  alternativa-por-alternativa, inclusive a mesma cláusula final de dica —
  resolvível por posição, sem reconhecer o mecanismo no canal certo;
  distratores e dica reescritos para quebrar a correspondência. Uma
  correção introduziu um novo eco de gabarito no enunciado de uma questão
  (palavras que só a nova alternativa correta tinha) — achado e corrigido
  no mesmo ciclo, antes de seguir. Relatório completo em
  `data/rascunhos/nivel-3/relatorios/3.5.md`.

  Validação final: `pytest -q` (3.552 testes, 0 falhas) e
  `validar_modulo.py data/modulos/*.json` (exit 0, 0 falhas em 31
  módulos). +35 questões, +1 bloco de teoria por módulo (6). Nível 3
  em 5 de 9.
- **Módulo 3.6 escrito, 03/09/2026 — Web III, a requisição que o servidor
  não deveria ter atendido. Fecha o bloco Web (3.4-3.6).** Recorte final:
  escopo da autorização sobre o objeto pedido (autenticado ≠ autorizado
  para este recurso); mais portas de entrada do que telas (API móvel,
  endpoint legado, verbo HTTP esquecido) e por que a verificação precisa
  morar num ponto central; escalada horizontal e vertical como a mesma
  falha por ângulos diferentes; lógica de negócio (requisição perfeita,
  fora de ordem), fechando com o contraponto defensivo.

  O levantamento de não-repetição corrigiu um erro do próprio pedido do
  usuário — RBAC/menor privilégio foi atribuído a "2.3 e 2.4", mas o
  dono real, conferido no conteúdo, é o **2.6** — e achou a colisão mais
  severa desta série até agora: o eixo de IDOR proposto era, palavra por
  palavra, o mesmo enquadramento que **6 das 35 questões do 2.6** já
  ensinam (mecanismo, correção certa, priorização por explorabilidade).
  Removido como conteúdo novo, não reformulado — a primeira vez nesta
  linha de módulos que um eixo inteiro sai do recorte em vez de ser
  reescrito. O espaço vago foi para o eixo de superfície de rotas
  proposto pelo usuário, confirmado livre por varredura contra 3.2, 3.3
  e 4.1; ver `data/rascunhos/nivel-3/fontes/nao-repetir-3.6.md`.

  Quatro laboratórios HTTP reais (`127.0.0.1`, portas 8101-8104, cada um
  derrubado pelo próprio script): checagem de papel correta que nunca
  compara departamento (escopo); mesma rota com GET protegido e DELETE
  sem checagem nenhuma (superfície); uma única função `autorizado()` que
  abre, ao mesmo tempo, leitura de mensagem alheia e ativação de modo
  manutenção por usuário comum (escalada); e `/confirmar` decidindo o
  estado do pedido por um campo que o próprio cliente envia, em vez de
  consultar o que `/pagar` registraria (lógica de negócio). Citação
  factual verificada por `WebFetch` em 03/09/2026: **OWASP Top 10:2025
  existe e A01 continua "Broken Access Control"** — módulos anteriores
  (2.5, 2.6) citavam a edição 2021; A06 "Insecure Design" cita
  explicitamente o exemplo de reserva de cinema usado no eixo 4.

  Os três checkpoints da regra 7 mediram, pela primeira vez, as quatro
  taxas (incluindo a nova triagem de molde de dica — ver seção 5 acima):
  o viés de comprimento (correta mais longa) reapareceu nas três rodadas
  — 75,0%, 50,0% e 41,4% respectivamente, cada vez acima do teto e cada
  vez corrigido antes de seguir. Diferente do 3.4 e do 3.5, cujo
  checkpoint final já nasceu dentro do teto, o hábito não generalizou
  neste módulo mesmo depois de duas correções — registrado como recaída
  de processo, não regressão da regra. Publicado em **13,8% mais_longa /
  27,6% mais_curta / 13,8% evita_absoluto / 2,9% molde de dica**.

  A revisão adversarial (duas lentes, com o pedido explícito desta
  rodada de procurar molde em distratores, dicas, enunciados e perguntas
  socráticas) achou a **quinta variante** desta família nesta sessão: o
  molde **"Duas alternativas [verbo], não/sem [conceito]"** em `dicas[1]`
  de **18 das 35 questões**, mais uma variante ("A resposta certa
  fala/nomeia X, não Y") em 5 — reescritas as 23 ocorrências com
  referência ao conteúdo específico de cada questão, quebrando o molde.
  Achou também um banco reciclado de distratores-arquétipo (2FA, HTTPS,
  reduzir limite, log) com justificativa quase idêntica entre questões
  de eixos diferentes (9 questões), uma dica que entregava o gabarito
  por paráfrase em vez de eco literal (5 questões, mais sutil que o que
  o validador automático pega), uma justificativa citando um fato que o
  laboratório não chegou a demonstrar na execução mostrada ao aluno
  (`3.6.q3`), uma questão em que a correta se distinguia dos distratores
  pela forma gramatical (substantivo vs. infinitivo, `3.6.q8`), e uma
  atribuição de seção OWASP imprecisa em `3.6.t5` — todos corrigidos.
  Relatório completo em `data/rascunhos/nivel-3/relatorios/3.6.md`.

  Validação final: `pytest -q` (3.661 testes, 0 falhas) e
  `validar_modulo.py data/modulos/*.json` (exit 0, 0 falhas em 32
  módulos). +35 questões, +1 bloco de teoria por módulo (6). Nível 3
  em 6 de 9. **Bloco Web (3.4-3.6) fechado.**
- **Módulo 3.7 escrito, 04/09/2026 — OWASP Top 10, a lista como
  instrumento, não catálogo de siglas.** Levantamento de não-repetição
  mediu o risco que o usuário apontou antes de escrever: **sete das dez
  categorias 2025 já tinham dono total do mecanismo** em outro módulo
  (A01→2.6+3.6, A02→4.1, A04→2.1-2.4, A05→3.5, A06→3.6, A07→2.5), uma
  parcial (A09→4.5), só A03 e A08 livres de verdade — percorrer a lista
  item a item teria sido repetição em 70% dela. Recorte adotado: cinco
  eixos sobre a lista como instrumento — metodologia híbrida (dado onde
  o método enxerga, voto onde não enxerga), por que posição não é
  perigo, vocabulário do lado aplicação/dev, o ponto cego que o método
  cria por construção, e mapear achado real para categoria (ou reconhecer
  que não pertence a nenhuma).

  Duas colisões de argumento achadas e reformuladas antes de escrever: o
  eixo de "vocabulário comum entre times" colidia com o título e o
  objetivo 1 do **4.6** (mesma tese, outra taxonomia); o eixo de "erro de
  tratar como checklist" colidia forte com **4.1** (`4.1.t6` quase com a
  mesma frase). A primeira tentativa de reformulação ("assumir 4.1/4.6
  como já ensinados") era inválida por ordem de curso — nível 4 vem
  depois do 3 (`engine.niveis_desbloqueados`), o aluno não viu ainda.
  Reformulados como eixos autocontidos e estreitos em vez de genéricos.

  Verificação de fonte em duas rodadas: a primeira, por `WebFetch`,
  confirmou a metodologia híbrida ("data-informed, but not blindly
  data-driven", oito categorias de dado + duas de voto). Uma revisão
  adversarial contestou três dessas citações como possivelmente
  inventadas — forçou uma terceira rodada, `curl` + `grep` no HTML bruto,
  sem resumo no meio: duas das três contestações eram falso positivo do
  resumo automático (a citação de A02 sobre prevalência, e a frase de
  abertura "standard awareness document", ambas confirmadas literais na
  fonte), mas achou dois erros reais — a citação de A08 estava atribuída
  à seção errada (é "How to Prevent", não "Description"), e A10 estava
  incorretamente descrito como uma das duas categorias promovidas por
  voto (são **A03 e A09**, confirmado no HTML cru; A10 é só "nova
  categoria", sem menção a voto). **Achado de processo: `WebFetch` deu
  respostas diferentes pra mesma pergunta sobre a mesma URL em chamadas
  distintas** — citação literal de fonte externa não deveria se apoiar só
  numa chamada resumida quando o texto exato importa.

  Aproveitado o achado da citação desatualizada para corrigir, em dois
  commits separados e anteriores a este módulo, `2.6`: rótulo de edição
  2021→2025 em 5 lugares (conteúdo idêntico entre edições, conferido
  antes de trocar) e uma contagem de CWE errada dentro de uma explicação
  (34→40, a contagem de 2021 dentro de texto sobre 2025). Um fork depois
  auditou os 1.315 campos `fonte` do corpus inteiro por qualquer número,
  versão, posição ou prazo que possa ter mudado de edição — **zero
  divergências novas** além do caso já corrigido do 2.6 (relatório em
  `data/rascunhos/nivel-3/fontes/auditoria-currency-corpus.md`).

  A revisão adversarial (duas lentes) também achou uma referência cruzada
  quebrada dentro do próprio 3.7: uma questão de reconhecimento (A07,
  falhas de autenticação) atribuía três achados a "2.5 já ensinou", mas
  um deles é na verdade do **2.4** (limite de tentativas) e outro
  (enumeração de usuário por mensagem de erro) não é ensinado em módulo
  nenhum — conteúdo novo apresentado como reconhecimento. Corrigida a
  atribuição, mantida a resposta. Mais: vazamento de palavra exclusiva
  da correta em duas dicas, um distrator internamente contraditório, um
  par de pareamento ambíguo, e dois distratores defensáveis por quem tem
  bagagem de edições anteriores do Top10 — todos corrigidos.

  Os três checkpoints da regra 7 mostraram, de novo, o mesmo hábito de
  escrita dos módulos 3.4 e 3.6: rascunho nasceu com `correta` fixo no
  índice 0 em toda questão e 97,0% de taxa `mais_longa` — o pior número
  desta linha. Corrigido por script (rotação de posição entre os 4
  índices) mais edição manual de comprimento em ~30 questões, chegando a
  3,2% antes do primeiro checkpoint formal. Sexta variante de molde de
  dica achada manualmente (ver seção 5 acima): "Pense em/Volte a..." em
  21% das dicas, invisível ao medidor de prefixo exato. Publicado em
  **3,2% mais_longa / 3,2% mais_curta / 25,8% evita_absoluto / 5,6%
  molde de dica**.

  Contagem de questões justificada explicitamente no relatório, a pedido
  do usuário: 36 questões, nenhuma para bater meta — 5 de reconhecimento
  (mecanismo já ensinado, etiqueta nova) e 5 de mecanismo genuinamente
  novo (A02, A03, A08, A09, A10 — as únicas partes do Top10 que nenhum
  outro módulo ainda tocava) fecham o eixo 5, mais um caso de "não
  pertence a nenhuma das dez". Relatório completo em
  `data/rascunhos/nivel-3/relatorios/3.7.md`.

  Validação final: `pytest -q` (3.774 testes, 0 falhas) e
  `validar_modulo.py data/modulos/*.json` (exit 0, 0 falhas em 33
  módulos). +36 questões, +6 blocos de teoria. Nível 3 em 7 de 9.
- **Módulo 3.8 escrito, 04–05/09/2026 — Quebra de senhas, a economia do
  ataque, não a operação.** Colisão pesada e prevista com 2.4 (hash e
  senhas) e 2.5 (autenticação): levantamento por contagem de menções em
  todos os 33 módulos publicados achou 2.4 e 2.5 já donos de hash lento,
  sal, parâmetros de Argon2id e política de senha do NIST — inclusive com
  os mesmos números repetidos entre os dois. Território livre confirmado
  por medição, não intuição: nenhum módulo fazia a conta "tentativas por
  segundo × espaço de busca" com número medido em execução, nem explicava
  por que ataque real usa dicionário e regra de transformação em vez de
  força bruta pura. Os cinco eixos do pedido original sobreviveram ao
  levantamento sem reformulação — diferente de 3.4, 3.5, 3.6 e 3.7, todos
  reformulados depois de medir. Levantamento completo em
  `data/rascunhos/nivel-3/fontes/nao-repetir-3.8.md`.

  Dois laboratórios, sem ferramenta nomeada, sem lista de senha real, sem
  hash de terceiro, só `hashlib` da biblioteca padrão: `custo_da_tentativa.py`
  mede a taxa real de hash rápido (633.659 tentativas/s) contra hash lento
  calibrado (1,2 tentativas/s, PBKDF2 600.000 iterações — mínimo
  recomendado pela OWASP citado em 2.4.t5) — 542.845× de diferença,
  projetando 51,5 dias contra 766,4 séculos para o mesmo espaço de busca.
  `estrutura_e_o_que_quebrado_significa.py` gera 7.070 candidatos a partir
  de 7 palavras-base inventadas (catorze ordens de grandeza menor que o
  espaço teórico) e recupera duas senhas de formato humano em milissegundos,
  sem recuperar uma senha aleatória de 12 caracteres — demonstrando com
  execução real que "quebrar" é achar o candidato certo dentro da
  estratégia, não quebrar o algoritmo.

  Regra 9 do PROGRESS.md aplicada pela primeira vez (citação sempre
  confirmada em fonte bruta): como este módulo não buscou fonte externa
  nova, a disciplina foi aplicada ao próprio corpus — toda referência
  cruzada a 2.4/2.5 foi conferida lendo o JSON bruto desses módulos, nunca
  de memória.

  Os três checkpoints da regra 7 mostraram o mesmo hábito de escrita da
  linha 3.4–3.7: qualificador absolutista só em alternativa errada e
  correta sistematicamente mais longa, recorrendo em **cada um dos três
  lotes de escrita** (62,5%→0%, depois 50%→5,6%, depois 44%→12,5% de
  `mais_longa`, o mesmo padrão para `evita_absoluto`). Corrigido a cada
  checkpoint, não só no fim.

  Duas lentes de revisão adversarial (regra 10 em ação — achado é
  hipótese, não veredito): a lente de precisão achou um defeito real e
  grave — `3.8.t2` afirmava que baixar qualquer um dos dois fatores da
  conta de custo baixa o tempo total, o que é o oposto da verdade para a
  taxa (baixar a taxa aumenta o tempo — é o propósito do hash lento). O
  mesmo erro estava marcado como resposta **correta** em `3.8.q11`
  ("multiplicar" em vez de "dividir"), contradizendo `q7` e `q14` do
  próprio módulo. Os dois corrigidos. Achados menores confirmados: `t5`
  undercontava o fator de sufixo de símbolo do laboratório; `t2` atribuía
  ao NIST um número (600.000 iterações de PBKDF2) que é da OWASP. A lente
  de forma achou e a sessão aceitou: uma dica que entregava a fórmula
  pronta, quatro distratores fracos demais para exigir leitura, duas
  questões (`q4`/`q32`) testando a mesma ideia quase com as mesmas
  palavras (`q32` reformulado para um ângulo genuinamente distinto), uma
  questão com os três distratores absolutistas e só a correta sem, e uma
  lacuna teórica (o custo de calibrar hash tem teto do lado da latência do
  usuário legítimo, usado numa questão sem estar em nenhuma teoria —
  acrescentada uma frase em `t3`). Um padrão candidato a sétima variante de
  molde de dica foi levantado pela lente e **rejeitado com justificativa**:
  abertura binária "A ou B?" nas dicas é o mesmo estilo socrático usado no
  corpus inteiro desde o nível 0, não um defeito deste módulo — a taxa
  medida automaticamente (2,9%) é a menor já vista nesta linha, sem sétima
  variante real encontrada.

  Publicado em **18,8% mais_longa / 25,0% mais_curta / 19,4%
  evita_absoluto / 2,9% molde de dica**, todos dentro do teto. Contagem de
  35 questões justificada por eixo no relatório — nenhuma para bater meta.
  Relatório completo em `data/rascunhos/nivel-3/relatorios/3.8.md`.

  Validação final: `pytest -q` (3.886 testes, 0 falhas) e
  `validar_modulo.py data/modulos/*.json` (exit 0, 0 falhas em 34
  módulos). +35 questões, +6 blocos de teoria. Nível 3 em 8 de 9 — falta
  só redes sem fio (engenharia social resolvida como decisão de escopo,
  ver seção 5: o 2.7 já cumpre o item do roadmap).

---

## 6. Como continuar sem o Claude Code

Esta seção existe para o caso de o app precisar crescer sem assistente nenhum.
Nada aqui depende de ferramenta paga: é Python, um editor de texto e o `git`.

### O ciclo, em uma frase

Copiar o exemplo → escrever o JSON → validar o arquivo → rodar os testes →
abrir o app → commitar.

### Passo a passo para escrever um módulo à mão

1. **Escolha o módulo** na lista da seção 5 e veja o escopo dele no
   `cybersecurity-app-spec.docx` (seção 3, "Trilha de conteúdo"). Cada módulo tem
   uma linha dizendo o que precisa cobrir.

2. **Copie o modelo:**

   ```bash
   cp exemplo/modulo-minimo.json data/modulos/03-01-metodologia-de-pentest.json
   ```

   O modelo traz uma questão de cada tipo utilizável e comentários em chaves que
   começam com `_`, que o app ignora. Apague os comentários quando terminar.

3. **Preencha o cabeçalho**: `id` (`"3.1"`), `nivel` (3), `titulo`, quatro
   `objetivos` e `pre_requisitos`. O `id` é o prefixo de todos os ids internos.

4. **Escreva 6 blocos de teoria**, `3.1.t1` a `3.1.t6`, cada um com `texto` de 500
   a 900 caracteres em 2 ou 3 parágrafos, mais `analogia`, `erro_comum` e `fonte`.

5. **Escreva 35 questões**, `3.1.q1` a `3.1.q35`. Para cada uma:
   - `objetivos` com o índice do objetivo que ela testa — e, no conjunto, os
     quatro objetivos precisam aparecer;
   - 4 alternativas, `correta` como índice, e `por_que_erradas` com uma
     justificativa para **cada** índice diferente do correto;
   - 3 dicas progressivas que não entregam a resposta;
   - `pergunta_socratica` começando com "Antes de conferir:";
   - `explicacao` de 3 a 6 frases e `fonte` real.

   Use pelo menos 4 tipos diferentes (o padrão dos módulos escritos é de 6 a 8).

6. **Valide só o seu arquivo** — o erro sai com o campo exato:

   ```bash
   python ferramentas/validar_modulo.py data/modulos/03-01-metodologia-de-pentest.json
   ```

   Depois da oitava questão (regra 7 das invioláveis, seção 7), rode também o
   portão de comprimento contra o arquivo parcial:

   ```bash
   python -m ferramentas.chutador_de_forma data/modulos/03-01-metodologia-de-pentest.json
   ```

   Taxa de `mais_longa` acima de 40% ali é mais barato de corrigir com 8
   questões escritas do que com as 35 prontas.

7. **Rode a suíte inteira.** O teste de qualidade é parametrizado por módulo, e o
   arquivo novo entra sozinho:

   ```bash
   python -m pytest -q
   ```

8. **Abra o app** pelo atalho e confira o módulo na Trilha.

9. **Commite e publique:**

   ```bash
   git add data/modulos/03-01-metodologia-de-pentest.json
   git commit -m "feat: modulo 3.1 — metodologia de pentest"
   git push
   ```

### O que segura a qualidade quando não há revisor

Seis hábitos, em ordem de retorno:

1. **Verifique o fato antes de escrever a questão.** Se dá para executar, execute
   e use a saída real como artefato. Se é norma, abra a norma e cite a seção.
2. **Recomendação técnica envelhece.** Confira a versão vigente antes de ensinar
   uma lista ou um parâmetro — foi assim que o OWASP Top 10:2025 entrou no lugar
   da versão de 2021 e o mínimo de senha do NIST virou 15 caracteres.
3. **Leia cada questão perguntando "há duas respostas defensáveis aqui?"**. É o
   defeito mais comum e o mais fácil de não enxergar sozinho. Se houver, o
   problema é do distrator, não do aluno.
4. **Nunca deixe a alternativa correta ser a mais longa.** Não é sobre o caso
   isolado: o validador mede a **distribuição** do módulo e reprova acima de 40%,
   porque "escolher a mais longa" é uma heurística que funciona sem ler nada.
   **O objetivo não é minimizar "mais longa" e sim não deixar sinal nenhum** —
   medir os dois lados, porque cortar demais faz "escolher a mais curta" virar o
   novo atalho. Mire o meio da faixa dos distratores, não o mínimo.
5. **Os quatro distratores respeitam a forma que o enunciado pede.** Se a pergunta
   pede quatro pontos, os quatro trazem quatro pontos; se pede um conjunto de
   medidas, os quatro são conjuntos. Quando só a correta tem o formato de
   resposta, o aluno acerta sem ler o conteúdo — e isso nenhuma régua de tamanho
   pega.
6. **Afirmação absoluta não serve de distrator.** "Proíbe qualquer forma", "não
   tem efeito algum", "nunca acontece": é curta por natureza e autorrefutável,
   dois sinais na mesma opção. Pior, o próprio conteúdo ensina a desconfiar de
   absolutos, o que torna o distrator inútil.

### Manutenção do app

- **Zerar o progresso:** feche o app e apague `progress.db`. Ele é recriado vazio.
- **Redesenhar o ícone:** `pip install pillow` e
  `python ferramentas/gerar_icone.py`.
- **Recriar o atalho:** aponte um atalho novo para
  `pythonw.exe main.py`, com pasta de trabalho em `C:\Dev\cybersecurity-app` e
  ícone `app.ico`.
- **Material de referência:** os PDFs em `docs/` ficam fora do Git de propósito.
  Se você clonar o repositório em outra máquina, essa pasta não vem junto — e o
  app funciona sem ela.

---

## 7. Regras invioláveis do projeto

1. A resposta correta nunca aparece antes da confirmação de uma tentativa.
2. Só a primeira tentativa conta na estatística de domínio.
3. Não existe botão "ver resposta" nem como voltar e remarcar.
4. Desafios práticos nunca vêm com a solução — só checklist e dicas.
5. Nenhum conteúdo de estudo hardcoded em `.py`.
6. Nada de acesso à rede em tempo de estudo.
7. **Forma da alternativa correta se mede em TRÊS pontos de qualquer
   módulo novo — na 8ª questão, na 20ª e ao terminar — nunca só no fim, e
   nunca só uma vez. A partir do 4.9, a medição cobre as três estratégias
   do chutador (`mais_longa`, `mais_curta`, `evita_absoluto`), não só
   comprimento; a partir do 3.6, soma-se a triagem de molde de dica
   (`ferramentas/medidor_molde_dica.py`, seção 5 acima) — reportada
   junto, mas como leitura obrigatória sobre o achado, não como quarta
   trava de reprovação.** No 4.5 e no 4.6 a correta saiu mais longa em 100% e 97%
   das questões na primeira escrita, mesmo com a regra escrita no prompt
   as duas vezes, porque a medição só aconteceu com o módulo inteiro
   pronto. No 4.7 o checkpoint da 8ª questão pegou o defeito (100%) e a
   correção baixou pra 14,3% — mas o hábito não generalizou, e o módulo
   terminou em 77% (23/30) antes da correção final. No 4.8, a revisão
   adversarial (que só roda depois do módulo pronto) achou qualificador
   absolutista ("nunca", "sempre") em 20 de 35 questões — um defeito que
   `evita_absoluto` já media desde 01/09/2026, mas que nenhum checkpoint
   conferiu durante a escrita, porque o processo só olhava comprimento.
   Um único checkpoint antecipa o diagnóstico; não muda sozinho o hábito
   de escrita ao longo de 35 questões — e medir só um eixo de forma
   deixa passar os outros. Rode
   `python -m ferramentas.chutador_de_forma <arquivo parcial>` na 8ª
   questão, de novo na 20ª, e de novo ao terminar — reportando as três
   taxas de cada vez — e ajuste o hábito de escrita a cada checkpoint,
   não só na primeira.
8. **Toda correção em lote (script, não edição questão a questão) se mede
   contra o defeito que ELA pode criar, não só contra o defeito que ela
   corrige.** No 4.7, um script que cortava a alternativa correta ou
   engordava o distrator mais curto resolveu o viés de comprimento (77%
   → 23%) — mas usou um pool de só três frases genéricas de
   "autorrejeição" ("leitura que soa plausível, mas...", e variantes), e
   essa frase-molde vazou em 15 distratores, sempre a mesma família,
   nunca na correta: um aluno atento ao padrão, não ao conteúdo, ganhava
   eliminação grátis. Só a revisão adversarial (duas lentes, agentes sem
   contexto da escrita) pegou isso — o validador automático não acusa,
   porque não é eco de vocabulário da correta, é repetição de forma entre
   distratores. Depois de qualquer correção em lote, meça explicitamente:
   `mais_longa`, `mais_curta`, e repetição de molde/frase entre
   distratores da mesma questão e entre questões do módulo — não assuma
   que resolver uma métrica não criou outra.

9. **Citação literal, número, seção nomeada ou prazo normativo que entra num
   módulo precisa ser confirmado no texto bruto da fonte — nunca numa
   chamada resumida.** No 3.7, o WebFetch deu respostas diferentes para a
   mesma pergunta sobre a mesma URL em chamadas distintas, e dois erros de
   atribuição só apareceram quando a fonte foi lida em HTML cru, não no
   resumo. Chamada resumida serve para orientação e busca; não serve como
   prova de citação. Toda vez que um trecho entre aspas, um número, o nome
   de uma seção ou um prazo normativo for para dentro de um módulo, a
   confirmação final é no texto bruto — não no resumo que trouxe a pista.
10. **Achado de revisão adversarial é hipótese a verificar, não veredito a
    aceitar ou descartar de cara.** No 3.7, a lente acusou três citações de
    inventadas: duas estavam corretas (falso positivo da lente) e uma tinha
    o erro real — no mesmo processo, a mesma lente também achou dois erros
    reais de atribuição. As duas coisas ficam registradas juntas de
    propósito: a lente erra sozinha (não virar veredito automático) e a
    lente acha coisa real (não virar ruído descartável). Todo achado de
    lente adversarial sobre citação se resolve indo à fonte bruta antes de
    aceitar ou rejeitar — nunca pelo julgamento da própria lente.

### Padrão aprendido: regra nascida, medida e descartada

Este projeto já criou três regras de validador que nasceram de um defeito
real visto à mão, e as três só sobreviveram quando medidas contra o corpus
inteiro — não contra o conjunto de casos que a própria regra usa para se
definir:

- **Regra 4 original** ("única em forma interrogativa") nunca disparou em
  módulo nenhum e foi descartada antes de virar regra — o precedente mais
  barato dos três, porque a medição aconteceu antes do código existir.
- **Regra 7, eixo dígito e eixo negação** (31/08–01/09/2026): a heurística
  parecia forte (73% "vazamento real" numa amostra pequena, classificada por
  quem já sabia o gabarito) e só caiu quando medida contra as 859 questões do
  corpus inteiro — 27% de acerto, igual ao acaso.

**A lição que fica: medir uma heurística sobre o conjunto que ela mesma
define é tautologia — a única população que prova alguma coisa é o corpus
inteiro, marcado e não-marcado junto.** Uma regra nova só está pronta pra
virar código quando alguém já rodou essa heurística contra o corpus inteiro e
viu a taxa de acerto passar do acaso com folga — não contra os casos que
inspiraram a regra, que por construção sempre "confirmam" a si mesmos. Isso
não é fracasso: as três regras descartadas custaram uma tarde cada, contra
semanas de reescrita de conteúdo que teriam sido desperdiçadas corrigindo
questões que não tinham defeito nenhum. `ferramentas/chutador_de_forma.py`
existe para tornar essa medição de uma linha de comando, não de uma sessão
de análise — é ferramenta permanente do processo de escrita de módulo, não
artefato de uma investigação só.

---

## 8. Como rodar

O comando abre o app usando a `.venv` da pasta, se existir, ou o Python do
sistema:

```bash
run.bat
```

Testes:

```bash
python -m pytest -q
```
