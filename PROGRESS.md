# Cybersecurity Study App — estado do projeto

Aplicativo desktop local de estudo de cibersegurança, em Python + CustomTkinter,
com SQLite para progresso e JSON para conteúdo. Roda offline.

Última atualização: 2026-08-19 · commit `e9c72a5` · 938 testes passando

---

## 1. Números

| Item | Quantidade |
|---|---|
| Módulos de conteúdo escritos | 18 de 41 |
| Questões | 631 |
| Blocos de teoria | 110 |
| Tags distintas | 548 |
| Testes automatizados | 938 |
| Linhas de código Python | ~3.260 |

Questões por nível: **nível 0** 141 (4 módulos) · **nível 1** 245 (7 módulos) ·
**nível 2** 245 (7 módulos, completo).

Tipos de questão em uso: conceitual 296, cenário 131, caça ao erro 48,
ataque→defesa 44, pareamento 34, comando 32, ordenação 24, artefato 22.

---

## 2. Estrutura de arquivos

```
C:\Dev\cybersecurity-app\
├── main.py                  ponto de entrada: janela, sidebar, roteamento
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
│   └── modulos/*.json       18 módulos (00-01 … 02-07)
├── tests/                   6 arquivos de teste
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
| 7 | Níveis 3 e 4 + desafios práticos | pendente |
| 8 | Nível 5 + simulado + trilha de 90 dias | pendente |
| 9 | Ícone, atalho, README, publicação | pendente |

### Conteúdo escrito

**Nível 0 — Alicerce** (141 questões)
0.1 O que é cibersegurança · 0.2 Superfície de ataque · 0.3 Quem é o adversário ·
0.4 Ética, escopo e lei

**Nível 1 — Base técnica** (245 questões)
1.1 Linux essencial · 1.2 Linha de comando e shell · 1.3 Windows e Active
Directory · 1.4 Redes I · 1.5 Redes II · 1.6 Python para segurança ·
1.7 Git e versionamento

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

### Conteúdo — 23 módulos

- **Nível 3 — Ofensivo** (9): metodologia de pentest, OSINT, varredura,
  Web I/II/III, OWASP Top 10, quebra de senhas, engenharia social e redes sem fio
- **Nível 4 — Defensivo** (8): hardening, segurança de rede, defesa em
  profundidade, malware, SIEM, MITRE ATT&CK, resposta a incidentes, forense
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
- Ícone `.ico`, atalho na área de trabalho, README, publicação no GitHub

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

---

## 6. Regras invioláveis do projeto

1. A resposta correta nunca aparece antes da confirmação de uma tentativa.
2. Só a primeira tentativa conta na estatística de domínio.
3. Não existe botão "ver resposta" nem como voltar e remarcar.
4. Desafios práticos nunca vêm com a solução — só checklist e dicas.
5. Nenhum conteúdo de estudo hardcoded em `.py`.
6. Nada de acesso à rede em tempo de estudo.

---

## 7. Como rodar

O comando abre o app usando a `.venv` da pasta, se existir, ou o Python do
sistema:

```bash
run.bat
```

Testes:

```bash
python -m pytest -q
```
