# Cyber — app de estudo de cibersegurança

Aplicativo de mesa, local e offline, para estudar cibersegurança do zero até
nível de engenharia. Python + CustomTkinter na interface, SQLite para o
progresso, JSON para todo o conteúdo de estudo.

A trilha tem 6 níveis e 41 módulos previstos. Cada módulo traz blocos curtos de
teoria e de 35 a 60 questões, com dica, pergunta socrática, explicação e fonte.
O motor decide o que mostrar (questão nova, revisão espaçada ou leitura), e o
progresso fica em `progress.db`, na própria pasta.

Estado atual, números e decisões técnicas: [PROGRESS.md](PROGRESS.md).

---

## Como rodar

Requisitos: **Python 3.11 ou mais novo** no Windows (o app foi feito e testado no
Windows 11; o código é multiplataforma, mas o atalho e o `run.bat` são do Windows).

```bash
pip install -r requirements.txt
```

Abrir o app — qualquer um dos três funciona:

- clicar duas vezes em **`run.bat`**;
- clicar no atalho **Cyber — Estudo de Cibersegurança** na área de trabalho;
- pela linha de comando: `pythonw main.py`.

O `run.bat` usa a `.venv` da pasta se ela existir e, se não existir, o Python do
sistema. Ele chama `pythonw`, então o app abre sem janela de terminal atrás.

Na primeira execução o arquivo `progress.db` é criado sozinho, com as tabelas
vazias. Apagar esse arquivo zera o progresso e não quebra nada.

### Testes

```bash
python -m pytest -q
```

O `conftest.py` na raiz é o que faz o pytest enxergar o pacote `app`. Rodar os
testes não toca no `progress.db`: os testes de banco usam arquivo temporário.

---

## Estrutura de pastas

```
cybersecurity-app/
├── main.py                  janela, barra lateral e roteamento entre telas
├── run.bat                  abre o app (usa .venv se existir)
├── app.ico                  ícone da janela e do atalho
├── conftest.py              faz o pytest achar o pacote `app`
├── requirements.txt         customtkinter (única dependência de execução)
├── requirements-dev.txt     pytest
├── app/
│   ├── theme.py             paleta Tokyo Night, fontes e componentes visuais
│   ├── db.py                única porta de entrada do SQLite
│   ├── content.py           carga e validação de esquema dos JSONs
│   ├── engine.py            revisão espaçada, domínio, desbloqueio, sessão, streak
│   ├── pedagogy.py          dicas, pergunta socrática, embaralho, correção
│   └── views/               uma tela por arquivo: home, trilha, modulo, sessao,
│                            progresso (prontas); desafio, glossario,
│                            ferramentas (ainda são esboços)
├── data/
│   ├── niveis.json          os 6 níveis e as regras de desbloqueio
│   └── modulos/*.json       um arquivo por módulo — é aqui que mora o conteúdo
├── exemplo/
│   └── modulo-minimo.json   módulo de exemplo, comentado, para copiar
├── ferramentas/
│   └── validar_modulo.py    valida um módulo escrito à mão antes de publicá-lo
├── tests/                   6 arquivos de teste
├── docs/                    PDFs de referência — fora do Git, não vai para o GitHub
└── progress.db              criado no primeiro uso — fora do Git
```

Duas regras de arquitetura que valem para qualquer mudança futura:

1. **Tela nunca fala com o SQLite.** Todo acesso passa por `app/db.py`.
2. **Nenhum conteúdo de estudo dentro de `.py`.** Teoria e questão vivem em
   `data/`. Se você está escrevendo texto de estudo dentro de um arquivo Python,
   está no lugar errado.

---

## Como o conteúdo é organizado

`data/niveis.json` define os 6 níveis e quando cada um destrava:

```json
{
  "id": 2,
  "nome": "Núcleo de segurança — cripto, identidade e acesso",
  "resumo": "Os mecanismos que sustentam a confiança: ...",
  "desbloqueio": { "tipo": "dominio", "niveis": [1], "minimo": 0.7 }
}
```

- `desbloqueio.tipo` é `"aberto"` (sempre liberado) ou `"dominio"`;
- em `"dominio"`, o nível abre quando o domínio médio dos níveis listados em
  `niveis` alcança `minimo` (0.7 = 70% de acerto).

O cadeado é **por nível, não por módulo**: dentro de um nível liberado, o aluno
escolhe a ordem. O campo `pre_requisitos` do módulo é ordem sugerida, não trava.

Cada arquivo em `data/modulos/` é um módulo. O nome do arquivo é livre — o que
vale é o campo `id` de dentro dele. A convenção usada até aqui é
`NN-MM-titulo-em-minusculas.json`, por exemplo `02-05-autenticacao-e-identidade.json`
para o módulo de `id` `"2.5"`.

---

## Esquema JSON de um módulo, campo a campo

A validação está em [`app/content.py`](app/content.py) e roda toda vez que o app
abre. Módulo malformado **não entra**: o app mostra uma faixa vermelha dizendo
qual arquivo e qual campo estão errados, e continua funcionando com os outros.

### Nível do módulo

| Campo | Tipo | Obrigatório | O que é |
|---|---|---|---|
| `id` | texto | sim | Identificador do módulo, `"2.5"`. Prefixo de todos os ids internos |
| `nivel` | inteiro 0–5 | sim | A que nível o módulo pertence |
| `titulo` | texto | sim | Nome que aparece na trilha |
| `objetivos` | lista de texto | sim | O que o aluno sai sabendo. **Todo objetivo precisa de pelo menos uma questão que o teste** |
| `pre_requisitos` | lista de ids | sim (pode ser `[]`) | Ordem sugerida. Cada id precisa existir |
| `teoria` | lista de blocos | sim, 4 a 8 blocos | Ver abaixo |
| `questoes` | lista de questões | sim, 35 a 60 | Ver abaixo |

### Bloco de teoria

| Campo | Obrigatório | O que é |
|---|---|---|
| `id` | sim | `"2.5.t1"` — começa com o id do módulo |
| `titulo` | sim | Título curto do bloco |
| `texto` | sim | 2 ou 3 parágrafos separados por `\n\n`, entre 500 e 900 caracteres |
| `analogia` | convenção | Uma frase que ancora o conceito no mundo físico |
| `erro_comum` | convenção | O engano clássico sobre esse assunto |
| `fonte` | sim | Livro + capítulo, norma + seção, ou "verificado em execução" |

`analogia` e `erro_comum` não são exigidos por `content.py`, mas os 18 módulos
escritos têm os dois em todos os 110 blocos. O validador de `ferramentas/`
cobra os dois.

### Questão

Campos comuns a todos os tipos:

| Campo | O que é |
|---|---|
| `id` | `"2.5.q7"` — começa com o id do módulo, sequencial |
| `tipo` | um dos nove tipos da tabela abaixo |
| `dificuldade` | inteiro de 1 a 3 |
| `objetivos` | lista de índices dos objetivos do módulo que esta questão testa, ex.: `[0]` ou `[1, 3]` |
| `enunciado` | a pergunta, curta e direta |
| `dicas` | lista de 3 dicas progressivas. Nenhuma entrega a resposta |
| `pergunta_socratica` | pergunta feita **entre** o Confirmar e o resultado. Começa com "Antes de conferir:" |
| `explicacao` | 3 a 6 frases dizendo por que a correta está certa e qual é o princípio |
| `fonte` | de onde saiu o conteúdo |
| `tags` | 3 a 5, minúsculas, com hífen, sem acento |

Campos que dependem do tipo:

| `tipo` | Campos adicionais obrigatórios |
|---|---|
| `conceitual` | `alternativas`, `correta`, `por_que_erradas` |
| `cenario` | `alternativas`, `correta`, `por_que_erradas` |
| `comando` | `alternativas`, `correta`, `por_que_erradas` |
| `ataque_defesa` | `alternativas`, `correta`, `por_que_erradas` |
| `artefato` | `artefato` (log, saída de ferramenta, cabeçalho), `alternativas`, `correta`, `por_que_erradas` |
| `caca_erro` | `trecho` (código ou configuração com uma falha), `alternativas`, `correta`, `por_que_erradas` |
| `pareamento` | `pares` — lista de `[esquerda, direita]`, no mínimo 2 |
| `ordenacao` | `itens` e `ordem_correta` (permutação de `0..n-1`) |
| `desafio` | `desafio_id` — **ainda não implementado**, não use |

Sobre os campos de alternativa:

- `alternativas`: lista de 4 textos (o mínimo do esquema é 2; a convenção do
  projeto é 4);
- `correta`: **índice** da certa dentro de `alternativas`, começando em 0;
- `por_que_erradas`: objeto com uma chave **em texto** para cada índice diferente
  do correto, justificando cada distrator. Faltou uma, o módulo não carrega.

```json
"alternativas": ["certa", "errada A", "errada B", "errada C"],
"correta": 0,
"por_que_erradas": {
  "1": "por que a A está errada",
  "2": "por que a B está errada",
  "3": "por que a C está errada"
}
```

Em `ordenacao` e `pareamento`, o arquivo guarda a ordem **certa**, e o app
embaralha na hora de exibir — com semente derivada do id da questão, para ser
sempre igual para a mesma questão e nunca sair na ordem correta.

O aluno nunca recebe o gabarito antes de responder: `pedagogy.questao_para_exibir()`
remove `correta`, `explicacao`, `por_que_erradas`, `ordem_correta` e `pares`
antes de a tela ver a questão.

---

## Como acrescentar um módulo novo à mão

1. **Copie o exemplo.** `exemplo/modulo-minimo.json` tem todos os campos
   preenchidos, um de cada tipo de questão, com comentário em `_comentario`
   explicando cada trecho. Campos que começam com `_` são ignorados pelo app.

2. **Salve em `data/modulos/`** com o nome no padrão
   `NN-MM-titulo-em-minusculas.json`.

3. **Preencha o cabeçalho**: `id`, `nivel`, `titulo`, `objetivos` (4 é o padrão
   do projeto), `pre_requisitos`.

4. **Escreva de 4 a 8 blocos de teoria** (6 é o padrão), cada um com `analogia`,
   `erro_comum` e `fonte`.

5. **Escreva de 35 a 60 questões** (35 é o padrão), com ids sequenciais
   `<id>.q1`, `<id>.q2`, … Use pelo menos 4 tipos diferentes — os módulos
   escritos usam de 6 a 8. Garanta que **cada objetivo declarado tenha ao menos
   uma questão** apontando para ele em `objetivos`.

6. **Valide antes de abrir o app:**

```bash
python ferramentas/validar_modulo.py data/modulos/03-01-metodologia-de-pentest.json
```

O validador cobra o esquema, as regras de quantidade, a convenção de
`analogia`/`erro_comum`, tags fora do padrão, alternativa repetida, enunciado
duplicado e dado pessoal em artefato. Ele também **avisa** quando a alternativa
correta é bem mais longa que as outras — sinal clássico de gabarito entregue de
graça.

### As seis regras de gabarito entregue

As cinco primeiras saíram de defeitos reais, encontrados à mão na revisão do
nível 3 e depois automatizados; a sexta saiu da constatação de que um molde de
redação específico produzia o defeito de novo a cada módulo. Todas produzem
**aviso**, nunca falha: são heurísticas, e quem decide é quem lê.

| Regra | O que procura | Caso que a originou |
|---|---|---|
| 1. Dica que reescreve o gabarito | Dica que traz ≥30% das palavras que **só** a alternativa correta tem (≥2 palavras) | 23 casos em 3.1, 3.2 e 3.3 — a dica parafraseava a resposta em vez de estreitar o raciocínio |
| 2. Artefato que carrega a resposta | `artefato` (≥35%) ou `trecho` (≥70%) com as palavras exclusivas da correta | `3.3.q14`: o laboratório imprimia `porta 8080 (HTTP nao fala primeiro)`, que era a resposta |
| 3. Enunciado que afirma a resposta | Enunciado com ≥35% das palavras exclusivas da correta (≥3 palavras) | `3.1.q17`: "por que X e Y **são independentes**?" afirmava o que a correta dizia |
| 4. Distrator que é gabarito de outra | Distrator com ≥72% de vocabulário em comum com a resposta certa de outra questão que **pergunta o mesmo** | `3.1.q24` usava como distrator a resposta certa de `3.1.q32` |
| 5. Duas questões ensinando o mesmo | Duas respostas certas com ≥55% de vocabulário em comum, inclusive **entre módulos** | `3.3.q25` repetia `3.2.q12`, e `4.1.q20` repetia `3.1.q35` |
| 5b. Pareamento que entrega gabarito | Lado direito de `pares` com ≥55% de vocabulário em comum com a resposta certa de outra questão | oito pares em seis questões; `1.5.q28` dizia o que `1.5.q13` ia cobrar |
| 6. Dica no molde "Pergunte ⟨…⟩" | Dica que abre — nela ou em qualquer frase dentro dela — com `Pergunte`, `Pergunte-se`, `Se pergunte`, `Questione` ou `Indague` | 41 dicas do 4.2 escritas no mesmo molde, nenhuma delas acusada pelas regras 1 a 5 |

O cálculo é sempre o mesmo: tomam-se as palavras da alternativa correta,
descontam-se as que aparecem em qualquer distrator (essas são vocabulário do
assunto, não gabarito) e mede-se quanto desse resto reaparece onde não devia.

**O que estas regras não pegam.** Elas veem eco literal, não paráfrase. Uma dica
que diz "o nome do meio indica mistura" para uma correta que diz "a combinação
das duas abordagens" não divide palavra nenhuma e passa batido — e metade dos
casos reais era desse tipo. Calibrando contra os três módulos antes da revisão, a
regra 1 reencontra cerca de um terço do que a leitura humana pegou. Serve como
rede, não como substituto.

**Dois falsos positivos previsíveis**, que valem ser reconhecidos em vez de
silenciados: um conjunto de questões que define termos vizinhos (as três letras
da tríade CIA, por exemplo) usa a definição de uma como distrator da outra de
propósito — por isso a regra 4 só acusa quando as duas questões perguntam a mesma
coisa; e em `caça ao erro` o gabarito cita o item defeituoso do próprio trecho,
por construção — por isso ali a régua da regra 2 sobe para 70%.

**A régua da regra 4 subiu de 60% para 72% depois de medida.** Ela não pegou
nenhum dos dois casos reais que a originaram: `3.1.q24` × `3.1.q32` dividia só
22% do vocabulário, e a duplicação entre módulos de `3.3.q25` × `3.2.q12`,
42% — as duas eram paráfrase, não cópia. O único disparo que ela produzia no
corpus era vocabulário de criptografia compartilhado entre duas questões
diferentes. A regra 5 nasceu dessa medição: comparar **resposta certa com
resposta certa**, que é onde a duplicação real aparece.

**A regra 6 é de forma, e é a única assim.** As outras cinco medem vocabulário;
esta olha só como a frase começa, e por isso não sabe se aquela dica específica
entrega alguma coisa. Ela existe porque o molde "Pergunte ⟨a pergunta cuja única
resposta é o gabarito⟩" reincidiu módulo após módulo mesmo proibido no encargo
do autor, e porque a paráfrase que ele produz é justamente a que as regras 1 a 5
não alcançam. Proibir a fôrma foi o que sobrou de acionável: dica boa aponta onde
olhar. O passivo herdado — **179 dicas em 15 módulos** — foi auditado um a um em
24/08/2026, módulo a módulo: 141 reescritas e 38 aceitas com justificativa em
[`ferramentas/avisos_aceitos.json`](ferramentas/avisos_aceitos.json). O corpus
inteiro está hoje sem nenhum aviso desta regra.

### Aviso aceito como legítimo

Nem todo disparo é defeito. Um cenário precisa conter os fatos que a resposta
classifica; um artefato precisa conter as linhas que a resposta lê; uma dica pode
dirigir a atenção com um contraste ou uma ordem de leitura sem afirmar a
conclusão — o que a regra 6 proíbe é o molde, não o ato de dirigir a atenção.

Esses casos ficam em [`ferramentas/avisos_aceitos.json`](ferramentas/avisos_aceitos.json),
com a justificativa de cada um. O validador consulta esse arquivo e não repete o
aviso — o registro ali é a única prova de que o caso foi lido e decidido. O
critério usado na revisão de 22/08/2026 está no topo do arquivo:

> **Corrigir** quando a dica **afirma** uma proposição que é a alternativa correta
> ou parte dela. **Aceitar** quando ela apenas dirige a atenção — pergunta,
> contraste, ordem de leitura — sem afirmar a resposta.

7. **Rode os testes:**

```bash
python -m pytest -q
```

`tests/test_qualidade_conteudo.py` é parametrizado por módulo: o arquivo novo
entra no teste sozinho, sem você mexer em nada.

8. **Abra o app** e confira o módulo na Trilha.

### Regras de conteúdo que o projeto não abre mão

1. A resposta correta nunca aparece antes de o aluno confirmar uma tentativa.
2. Só a primeira tentativa conta na estatística de domínio — garantido por índice
   único no banco, não por código de tela.
3. Não existe botão "ver resposta" nem como voltar e remarcar.
4. Nenhuma questão pode ter mais de uma alternativa defensável. Distrator
   plausível, mas inequivocamente errado.
5. Toda questão carrega `fonte`. Recomendação técnica citada é a **vigente** —
   conteúdo de segurança envelhece rápido.
6. Nada de acesso à rede durante o estudo.

---

## O banco de progresso

`progress.db` é criado no primeiro uso, na pasta do projeto, e nunca vai para o
Git. Tabelas: `tentativas`, `srs`, `modulos_status`, `sessoes`, `preferencias`,
`desafios_status`.

O detalhe que mais importa:

```sql
CREATE UNIQUE INDEX idx_primeira_tentativa
ON tentativas(questao_id) WHERE n_tentativa = 1;
```

Uma segunda tentativa gravada como primeira levanta erro em vez de inflar a
estatística em silêncio. O número da tentativa é calculado dentro de
`db.registrar_tentativa()`; quem chama não pode passá-lo.

Duas métricas convivem de propósito: `dominio_modulo()` divide pelo total de
questões e mede **progresso**; `dominio_sobre_vistas()` divide pelas questões já
vistas e mede **desempenho**.

---

## Material de referência

A pasta `docs/` guarda os PDFs usados como fonte (Security Engineering, Crypto
101, entre outros) e **está no `.gitignore`**: é material de terceiros, não é
redistribuído aqui. O app não depende dela para funcionar — ela serve a quem
escreve conteúdo novo.
