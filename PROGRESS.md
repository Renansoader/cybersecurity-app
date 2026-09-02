# Cybersecurity Study App — estado do projeto

Aplicativo desktop local de estudo de cibersegurança, em Python + CustomTkinter,
com SQLite para progresso e JSON para conteúdo. Roda offline.

Última atualização: 2026-09-01 · nível 0 inteiro corrigido de comprimento
(0.1-0.4, 11 de 27 acima do teto) · 3.113 testes passando

Repositório: <https://github.com/Renansoader/cybersecurity-app> (privado)

---

## 1. Números

| Item | Quantidade |
|---|---|
| Módulos de conteúdo escritos | 27 de 41 |
| Questões | 946 |
| Blocos de teoria | 164 |
| Tags distintas | 789 |
| Testes automatizados | 3.112 |
| Linhas de código Python | ~2.280 no app · ~3.830 com ferramentas e testes |

Questões por nível: **nível 0** 141 (4 módulos) · **nível 1** 245 (7 módulos) ·
**nível 2** 245 (7 módulos, completo) · **nível 3** 105 (3 de 9 módulos) · **nível 4** 210 (6 de 8 módulos).

Tipos de questão em uso: conceitual 404, cenário 201, ataque→defesa 71,
caça ao erro 70, comando 56, artefato 57, pareamento 51, ordenação 36.

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

**Nível 4 — Defensivo** (210 questões, 6 de 8)
4.1 Hardening · 4.2 Segurança de rede · 4.3 Defesa em profundidade · 4.4 Malware ·
4.5 SIEM e monitoramento · 4.6 MITRE ATT&CK e caça a ameaças

**Nível 3 — Ofensivo** (105 questões, 3 de 9)
3.1 Metodologia de pentest · 3.2 OSINT e reconhecimento ·
3.3 Varredura e enumeração

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

### Conteúdo — 14 módulos

- **Nível 3 — Ofensivo** (6 restantes): Web I/II/III, OWASP Top 10, quebra de
  senhas, engenharia social e redes sem fio
- **Nível 4 — Defensivo** (2 restantes): resposta a incidentes, forense
- **Nível 5 — Engenharia e carreira** (6): desenvolvimento seguro, nuvem,
  modelagem de ameaças, GRC, economia da segurança, carreira

O próximo bloco natural é o nível 3, que desbloqueia com 70% no nível 2 —
agora completo. Os laboratórios de verificação ficam em pé: quebra de senhas
(3.8) reaproveita o material de 2.4 e 2.5, e Web I–III (3.4–3.6) pede captura
real de requisição.

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
  | 0.1 | 35,5% | ok (era 61,3% — piloto de correção, ver abaixo) |
  | 0.2 | 35,5% | ok (era 45,2%) |
  | 0.3 | 35,5% | ok (era 41,9%) |
  | 0.4 | 35,5% | ok (era 45,2%) |
  | 1.5 | 35,5% | ok |
  | 1.7 | 34,4% | ok |
  | 1.4 | 32,3% | ok |
  | 4.4 | 31,2% | ok |
  | 2.1 | 28,1% | ok |
  | 2.2 | 28,1% | ok |
  | 1.6 | 27,3% | ok |
  | 2.3 | 21,2% | ok |
  | 2.4 | 21,2% | ok |
  | 4.5 | 19,4% | ok |
  | 4.3 | 15,6% | ok |
  | 4.6 | 15,6% | ok |

  **11 de 27 módulos acima do teto de 40%** (era 15 antes do nível 0; nível
  0 (0.1-0.4) está inteiro abaixo do teto agora). O teto não é palpite:
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
7. **Distribuição de comprimento da alternativa correta se mede depois das
   primeiras 8 questões de qualquer módulo novo, nunca só no fim.** No 4.5 e
   no 4.6 a correta saiu mais longa em 100% e 97% das questões na primeira
   escrita — mesmo com a regra escrita no prompt as duas vezes — porque a
   medição só aconteceu com o módulo inteiro pronto, quando corrigir já
   significava reescrever 30+ alternativas. Corrigir 8 é barato; corrigir 35
   não é. Rode `python -m ferramentas.chutador_de_forma <arquivo parcial>`
   assim que a oitava questão for escrita, ajuste o hábito de escrita ali, e
   só então siga para as 27 restantes.

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
