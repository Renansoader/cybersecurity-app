# Cybersecurity Study App — estado do projeto

Aplicativo desktop local de estudo de cibersegurança, em Python + CustomTkinter,
com SQLite para progresso e JSON para conteúdo. Roda offline.

Última atualização: 2026-08-25 · commit `4.3` · 2.768 testes passando

Repositório: <https://github.com/Renansoader/cybersecurity-app> (privado)

---

## 1. Números

| Item | Quantidade |
|---|---|
| Módulos de conteúdo escritos | 24 de 41 |
| Questões | 841 |
| Blocos de teoria | 146 |
| Tags distintas | 755 |
| Testes automatizados | 2.768 |
| Linhas de código Python | ~2.280 no app · ~3.830 com ferramentas e testes |

Questões por nível: **nível 0** 141 (4 módulos) · **nível 1** 245 (7 módulos) ·
**nível 2** 245 (7 módulos, completo) · **nível 3** 105 (3 de 9 módulos) · **nível 4** 105 (3 de 8 módulos).

Tipos de questão em uso: conceitual 369, cenário 173, ataque→defesa 64,
caça ao erro 61, comando 51, pareamento 46, artefato 46, ordenação 31.

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
│   ├── modulos/*.json       24 módulos (00-01 … 04-03)
│   └── rascunhos/            laboratórios, fontes e relatórios de procedência
├── exemplo/
│   └── modulo-minimo.json   modelo comentado, um exemplo de cada tipo de questão
├── ferramentas/
│   ├── validar_modulo.py    valida um módulo antes de ele entrar em data/modulos/
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
| 7 | Níveis 3 e 4 + desafios práticos | em andamento: 3.1–3.3 e 4.1–4.3 prontos |
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

**Nível 4 — Defensivo** (105 questões, 3 de 8)
4.1 Hardening · 4.2 Segurança de rede · 4.3 Defesa em profundidade

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

### Conteúdo — 17 módulos

- **Nível 3 — Ofensivo** (6 restantes): Web I/II/III, OWASP Top 10, quebra de
  senhas, engenharia social e redes sem fio
- **Nível 4 — Defensivo** (5 restantes): malware, SIEM, MITRE ATT&CK, resposta a
  incidentes, forense
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
- **Comprimento da alternativa correta: varrido só até o nível 2.** A régua de
  distribuição entrou em `a21ca56` e a varredura de classe (a) — cortar da
  correta a justificativa que a explicação já carrega — cobriu os níveis 0, 1 e
  os módulos 2.1 a 2.4. No corpus, "a correta é a mais longa" caiu de **76% para
  39%**; o acaso é 25%. O que ficou:

  - **20 questões de classe (b)**, em que a correta não tem gordura e o que falta
    é especificidade no distrator. Reescrevê-las é trabalho de conteúdo, não de
    faxina: é preciso escrever um erro plausível com a mesma densidade da
    resposta certa. Níveis 0 e 1: `0.1.q24` `0.1.q31` `0.2.q1` `0.2.q15`
    `0.2.q20` `0.4.q3` `0.4.q21` `0.4.q28` `1.2.q21` `1.4.q22` `1.6.q10`.
    Nível 2: `2.1.q9` e `2.1.q17`. Três subtipos: definição sem gordura contra
    distrator vago; lista em que cada item é parte da resposta; e comando ou
    bloco de código em que a resposta certa tem mais estágios.
  - **Oito módulos não varridos**, todos entre 38% e 75%: 2.6 (75%), 4.2 (62%),
    2.7 (56%), 3.1 (48%), 3.3 (47%), 3.2 (41%), 4.1 (41%) e 2.5 (38%). Ficaram
    de fora por decisão de prioridade: já estavam perto ou dentro do teto, e o
    retorno não pagava mais uma sessão.
  - **A zona cinzenta e os empates técnicos, deliberadamente não tocados.** Das
    288 questões em que a correta ainda é a mais longa, **174 são empate técnico**
    (razão abaixo de 1,2×, diferença de poucos caracteres) e **96 estão entre
    1,2× e 1,4×**. Mexer nelas produz churn sem reduzir sinal: a amostra mostrou
    que abaixo de 1,4× não há o que cortar.

  A regra dos 40% segue como **aviso**, e não como teste. Ela vira `assert` em
  `tests/` quando o corpus estiver abaixo do teto — antes disso deixaria a suíte
  vermelha em 22 módulos, o que não ajuda ninguém.
- **O atalho da área de trabalho aponta para o Python do sistema.** Se um dia
  existir `.venv` na pasta, o atalho continuará usando o Python global; o
  `run.bat` é quem prefere a `.venv`.

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
