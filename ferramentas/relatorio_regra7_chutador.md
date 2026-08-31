# Relatório — chutador de forma contra a regra 7 (unicidade estrutural)

Terceira tentativa de medir se os eixos dígito/negação da regra 7 medem
vazamento real. Rodadas anteriores falharam por não serem cegas de verdade:

1. Amostra manual de 15 achados — classificada por quem já sabia o gabarito.
   Não generaliza: viés de confirmação garantido.
2. Agente cego (LLM), instruído a ignorar mérito técnico — ambos os grupos
   (marcado e controle) bateram no teto (93,8% e 97,9%), porque nenhuma
   instrução apaga o pré-treino do modelo em cibersegurança. Sem sinal.

Esta rodada tira o modelo do circuito: `ferramentas/chutador_de_forma.py` é
um conjunto de heurísticas determinísticas em Python — nunca lê `correta`,
só `enunciado` e `alternativas`. Não tem como "entender" a questão.

## Populações

- **A** — 96 questões que disparam a regra 7 hoje (10 dígito + 86 negação)
- **B** — 96 questões controle, mesma distribuição por módulo, sorteadas
  entre as que não têm NENHUMA marca estrutural (nem as 8 já aceitas em
  `avisos_aceitos.json`), seed `20260831`
- **C** — as 859 questões de múltipla escolha do corpus inteiro, linha de base

## Resultado bruto

```
mais_longa             pop=A  acertos= 44/ 96  abstencoes=  0/ 96  taxa= 45.8%  IC95%=[36.2%, 55.8%]
mais_longa             pop=B  acertos= 31/ 96  abstencoes=  0/ 96  taxa= 32.3%  IC95%=[23.8%, 42.2%]
mais_longa             pop=C  acertos=355/859  abstencoes=  0/859  taxa= 41.3%  IC95%=[38.1%, 44.7%]

unica_com_negacao      pop=A  acertos= 76/ 82  abstencoes= 14/ 96  taxa= 92.7%  IC95%=[84.9%, 96.6%]
unica_com_negacao      pop=B  acertos=  0/ 29  abstencoes= 67/ 96  taxa=  0.0%  IC95%=[0.0%, 11.7%]
unica_com_negacao      pop=C  acertos= 76/279  abstencoes=580/859  taxa= 27.2%  IC95%=[22.4%, 32.7%]

unica_sem_negacao      pop=A  acertos= 10/ 10  abstencoes= 86/ 96  taxa=100.0%  IC95%=[72.2%, 100.0%]
unica_sem_negacao      pop=B  acertos=  0/  6  abstencoes= 90/ 96  taxa=  0.0%  IC95%=[0.0%, 39.0%]
unica_sem_negacao      pop=C  acertos= 10/ 37  abstencoes=822/859  taxa= 27.0%  IC95%=[15.4%, 43.0%]

unica_com_digito       pop=A  acertos=  9/ 16  abstencoes= 80/ 96  taxa= 56.2%  IC95%=[33.2%, 76.9%]
unica_com_digito       pop=B  acertos=  0/  7  abstencoes= 89/ 96  taxa=  0.0%  IC95%=[0.0%, 35.4%]
unica_com_digito       pop=C  acertos= 16/ 81  abstencoes=778/859  taxa= 19.8%  IC95%=[12.5%, 29.7%]

unica_sem_digito       pop=A  acertos=  1/  1  abstencoes= 95/ 96  taxa=100.0%  IC95%=[20.7%, 100.0%]
unica_sem_digito       pop=B  acertos=  0/  2  abstencoes= 94/ 96  taxa=  0.0%  IC95%=[0.0%, 65.8%]
unica_sem_digito       pop=C  acertos=  2/ 20  abstencoes=839/859  taxa= 10.0%  IC95%=[2.8%, 30.1%]

evita_absoluto          pop=A  acertos= 43/ 96  abstencoes=  0/ 96  taxa= 44.8%  IC95%=[35.2%, 54.7%]
evita_absoluto          pop=B  acertos= 34/ 96  abstencoes=  0/ 96  taxa= 35.4%  IC95%=[26.6%, 45.4%]
evita_absoluto          pop=C  acertos=366/856  abstencoes=  3/859  taxa= 42.8%  IC95%=[39.5%, 46.1%]
```

Eixos combinados (com + sem), população C:

- negação: 86/316 = **27,2%** IC95% [22,6%, 32,4%]
- dígito: 18/101 = **17,8%** IC95% [11,6%, 26,4%]

## Por que a taxa em A não serve — e por que isso não é "ambíguo"

A taxa de `unica_com_negacao`/`unica_sem_negacao`/`unica_com_digito`/
`unica_sem_digito` na população A é **tautológica**, não é sinal: a regra 7
define uma questão como "achado" exatamente quando essa mesma heurística
aponta para `correta`. Rodar a heurística de novo sobre o conjunto que ela
mesma definiu é reconferir a própria definição, não medir se alguém sem
saber o assunto acertaria. A taxa perto de 100% em A não mede vazamento —
mede que a regra 7 sabe reconhecer a própria regra.

A população B é o espelho: foi sorteada excluindo exatamente os casos em
que o marcador aponta para `correta`, então 0% ali também é garantido por
construção, não é achado.

**A população C é a única não-circular.** Nela, o marcador aparece em toda
parte do corpus — às vezes apontando para a correta (os 96 casos que já
formam a população A), às vezes para um distrator qualquer (a maioria) — e
mede a pergunta real: "se eu vir essa marca de forma em qualquer questão do
corpus, sem saber qual é, qual a chance de ela apontar pra resposta certa?"

## Leitura

- **Eixo negação**: 27,2% e 27,0% na população C, os dois intervalos de
  confiança cobrindo os 25% de acaso. Estatisticamente indistinguível de
  chute aleatório. **A marca não prediz a correta fora do conjunto que a
  própria regra já usa pra se definir — os 86 achados não são dívida de
  conteúdo.**
- **Eixo dígito**: 19,8% e 10,0% na população C — os dois intervalos
  também cobrem ou ficam abaixo de 25%, com IC largo por causa da
  população pequena (n=81 e n=20 de aplicação, população total de achados é
  só 10). Combinado: 17,8% IC95% [11,6%, 26,4%] — cobre o acaso. **Mesma
  conclusão do eixo negação, com menos confiança estatística pela amostra
  pequena, mas nenhum sinal de que o eixo prediga a correta.**
- **`mais_longa` e `evita_absoluto`** (comprimento, não fazem parte da
  regra 7) ficam bem acima do acaso nas três populações — 41-46% contra 25%
  — inclusive na população C, que não foi filtrada por nenhum critério.
  Isso é o viés de comprimento já documentado e parcialmente corrigido no
  PROGRESS.md (§5), e serve de prova de que o chutador funciona: quando
  existe sinal real, ele aparece nas três populações, não só na circular.

## Recomendação (PASSO 4)

Resultado **não é ambíguo** — ao contrário da rodada anterior, esta tem
número limpo e não-circular: **remover os eixos dígito e negação da regra
7**, ou rebaixá-los de aviso para comentário informativo sem entrar no
relatório do validador. Os 96 achados atuais (10 dígito + 86 negação) não
são dívida de conteúdo: a evidência não-circular (população C) diz que a
marca que os gerou não prediz a resposta certa mais do que o acaso.

O eixo que carrega sinal real e documentado é o de comprimento
(`mais_longa`), já coberto pela régua dos 40% do PROGRESS.md — esse
continua sendo o alvo legítimo de correção de conteúdo, não os achados da
regra 7.

Decisão de aplicar esta recomendação (remover/rebaixar os eixos, atualizar
PROGRESS.md) fica para o usuário — este relatório só mede.
