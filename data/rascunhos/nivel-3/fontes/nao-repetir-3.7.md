# O que os módulos publicados já ensinam — não repetir no 3.7

Levantado em 04/09/2026, sobre os 32 módulos publicados (1.121 questões,
bloco Web completo com 3.6). O 3.7 (OWASP Top 10) é o oitavo módulo do
nível 3 e fecha praticamente todo o vocabulário de mecanismo web que a
lista nomeia — o risco que o usuário apontou é real e mapeado item a
item abaixo.

## 0. Versão vigente — reconfirmada na fonte, 04/09/2026

`owasp-versao-VERIFICADA.md` (19/08/2026) já continha a verificação
correta; reconferido agora porque a restrição do usuário trata isso
como crítico e duas semanas é tempo suficiente para o projeto mudar.

- **[CONFIRMADO agora]** `https://owasp.org/www-project-top-ten/`:
  "The most current released version is the OWASP Top 10 2025." Sem
  mudança em relação à verificação anterior.
- **[CONFIRMADO agora]** `https://owasp.org/Top10/2025/0x00_2025-Introduction/`
  — as dez categorias batem exatamente com o arquivo já verificado.
  Nenhuma divergência.
- **[NOVO, não estava no arquivo anterior]** A metodologia não é
  "dados reais, sem opinião", como a proposta original do usuário
  descreve — é **híbrida**, e a própria introdução diz isso de forma
  explícita: *"This installment of the Top Ten remains data-informed,
  but not blindly data-driven."* Oito categorias vêm de análise
  empírica (CVE agrupado por CWE, 2,8 milhões de aplicações, 589 CWEs
  nesta edição); **duas foram votadas pela comunidade**, não medidas:
  A09 (Security Logging & Alerting Failures) e A10 (Mishandling of
  Exceptional Conditions, categoria nova). Motivo declarado para A09:
  *"This category will always be underrepresented in the data, and was
  again voted into a position."* — falha de log é estruturalmente
  invisível para o método automatizado que constrói as outras oito.
- **[NOVO]** Frase sobre o limite do próprio método: *"The results in
  the data are largely limited to what the industry can test for in an
  automated fashion... Everything we find is looking back in the
  past."* Isso é munição direta para o eixo sobre o que a lista não
  consegue capturar por construção.
- Nenhuma data oficial de publicação segue sem aparecer nas páginas
  lidas — mantém-se a regra já registrada: citar "OWASP Top 10:2025",
  sem dia, e não reinventar a data do release candidate/final sem
  marcar como consolidado.

## 1. Mapa item a item — quem já é dono do mecanismo

| Categoria 2025 | Dono do mecanismo hoje | Grau de posse |
|---|---|---|
| A01 Broken Access Control | **2.6** (IDOR, RBAC, menor privilégio) + **3.6** (escopo de objeto, superfície de rotas, escalada horizontal/vertical) | **Total.** 3.6 já cita "OWASP Top 10:2025, A01 Broken Access Control" como `fonte` em 8 das suas 35 questões. |
| A02 Security Misconfiguration | **4.1** (linha de base, benchmark, desvio de configuração) | **Total** no mecanismo, sem citar a sigla A02 — é literalmente do que a categoria trata (configuração padrão, exposição desnecessária, desvio de linha de base). |
| A03 Software Supply Chain Failures | Ninguém. Toque leve em **1.7** (uma questão: atualização automática de dependência sem revisão como caminho de ataque de cadeia de fornecimento) | **Livre**, com uma referência cruzada pontual a fazer. |
| A04 Cryptographic Failures | **2.1, 2.2, 2.3, 2.4** (bloco de criptografia inteiro) | **Total.** Confirma a premissa do usuário. |
| A05 Injection | **3.5** (SQLi, XSS, injeção de comando como confusão dado/instrução) | **Total.** Confirma a premissa do usuário. |
| A06 Insecure Design | **3.6** eixo 4 (lógica de negócio) | **Total.** 3.6 já cita "OWASP Top 10:2025, A06 Insecure Design" como `fonte` em 4 questões, incluindo o exemplo do cinema tirado direto de Example Attack Scenarios. |
| A07 Authentication Failures | **2.5** (autenticação e identidade) | **Total** no mecanismo. |
| A08 Software or Data Integrity Failures | Ninguém | **Livre.** |
| A09 Security Logging & Alerting Failures | **4.5** (SIEM: o que coletar, custo de reter, fadiga de alerta, validar detecção) | **Parcial/adjacente.** 4.5 ensina a engenharia de log e alerta como disciplina; não ensina "log insuficiente/ausente é uma categoria do Top 10", nem cita a sigla. Mecanismo de fundo é o mesmo (visibilidade insuficiente permite que o ataque passe despercebido); enquadramento é diferente (operação de SOC vs. causa raiz de falha de segurança). |
| A10 Mishandling of Exceptional Conditions | Ninguém como categoria de segurança | **Livre**, com toques leves e não-concorrentes: 1.6 (except genérico esconde falha, mas é sobre qualidade de script, não fail-open de negócio); 2.3 (tratamento de erro como canal lateral de cripto, mecanismo diferente); 4.7 (playbook: sinal que não bate com nenhum critério escala para humano — decisão operacional, não falha de design). |

**Contagem**: sete categorias têm dono total do mecanismo (A01, A02,
A04, A05, A06, A07), uma tem dono parcial que não usa o enquadramento
OWASP (A09), e só duas estão de fato livres (A03, A08 — A10 livre como
categoria, com toques leves não concorrentes). **Se o 3.7 percorrer a
lista explicando cada item, sete das dez perguntas já têm resposta
publicada em outro módulo — o risco que o usuário apontou se confirma
por medição, não por intuição.**

## 2. Território extra: quem já usa a citação "OWASP Top 10" como fonte

Achado que muda o corte do 3.7: **o app já ensina o aluno a reconhecer
A01 e A06 pelo nome**, porque 3.6 cita a fonte OWASP em quase um quarto
das suas questões. Isso significa duas coisas para o 3.7:

- Não pode reintroduzir "A01 = Broken Access Control" como se fosse
  novidade — o aluno que chegou até aqui já viu essa citação oito
  vezes.
- Pode (e talvez deva) usar esse histórico como gancho: a primeira
  pergunta socrática do módulo pode literalmente apontar para o que o
  aluno já leu em `3.6.q1`/`3.6.q19` e perguntar "que categoria era
  essa, e o que ela media" — cobrando reconhecimento de instrumento,
  não decoreba de sigla nova.

Achado colateral, fora do escopo do 3.7 mas relevante para registrar:
**2.6 cita "OWASP Top 10:2021 A01"** em três lugares (`2.6.t6`, e duas
`fonte` de questão), enquanto 3.6 já usa 2025. A01 não mudou de posição
entre as duas edições (Broken Access Control ficou em primeiro nas
duas), então não há erro factual na citação — mas é uma citação
desatualizada dentro do próprio corpus, o tipo de coisa que o eixo
"a posição muda entre edições" do 3.7 poderia expor sem querer, se um
aluno atento comparar. Não é bloqueador para escrever o 3.7; registro
para decisão do usuário sobre corrigir ou não a citação do 2.6 depois.

## 3. Colisões nos cinco eixos propostos

### Eixo 1 — como a lista é construída (dados de teste/incidente, não opinião de comitê)

**Sem colisão de módulo**, mas a premissa como formulada está
**factualmente incompleta** frente à fonte primária reconferida hoje
(seção 0 acima). A introdução da edição 2025 diz explicitamente que o
método **não** é "blindly data-driven" — é híbrido: oito categorias de
dado empírico, duas votadas pela comunidade porque o método automatizado
estruturalmente não as enxerga. Reformular o eixo para ensinar essa
nuance específica em vez da versão simplificada é mais forte
pedagogicamente e evita uma correção de prova incorreta: **não seria
uma pergunta decorável ("a lista é 100% dados") mas uma pergunta de
raciocínio sobre por que um método baseado em dado de teste automatizado
precisa de um mecanismo de correção não-automatizado para não ficar cego
a uma categoria inteira**.

### Eixo 2 — por que a posição muda entre edições

**Sem colisão.** Bem sustentado pela fonte: A02 subiu porque
"misconfigurations are more prevalent in the data for this cycle"
(prevalência relativa nos dados submetidos, não periculosidade
absoluta); A04/A05/A06 desceram porque outras categorias ficaram mais
prevalentes no mesmo ciclo, não porque cripto/injeção/design ficaram
mais seguros. Este eixo já era o ARMADILHA 3 do arquivo
`owasp-versao-VERIFICADA.md` — mantido, e agora com a citação exata da
fonte para a explicação de A02.

### Eixo 3 — a lista como vocabulário comum entre times que não compartilham código

**Colisão real de argumento com 4.6 (MITRE ATT&CK).** O título do 4.6
é literalmente *"comportamento como vocabulário compartilhado"*, e o
objetivo 1 é *"explicar por que a distinção [tática/técnica/procedimento]
resolve comunicação entre times de ataque e defesa"* — a mesma forma de
argumento (taxonomia padronizada resolve comunicação entre times que
não compartilham código/contexto), aplicada a outra lista. Há ainda uma
segunda ocorrência da mesma família retórica em 4.5 (SIEM): "o
vocabulário comum não nasce em nenhuma fonte específica — ele é
construído para ligar todas", sobre normalização de campo de log. Não é
o mesmo mecanismo (Top 10 categoriza falha de aplicação; ATT&CK
categoriza comportamento de adversário; SIEM normaliza campo de evento),
mas é a **terceira vez** que o corpus usaria "lista/taxonomia padronizada
= vocabulário comum entre times" como argumento central de um eixo.
Proposta de troca: não abrir o eixo como argumento genérico
("taxonomias ajudam comunicação"), e sim já assumir isso como
conhecimento estabelecido (referência cruzada a 4.6.t1) e perguntar o
que é **específico da posição do OWASP Top 10 nesse papel** — que ele é
o vocabulário do lado *aplicação/dev* (relatório de pentest, ticket de
correção, conversa entre segurança e time de produto), enquanto ATT&CK é
o vocabulário do lado *comportamento do adversário* (SOC, threat hunting)
— dois vocabulários compartilhados, para públicos e momentos diferentes
do mesmo processo de segurança.

### Eixo 4 — erro de tratar como checklist de conformidade

**Colisão severa com 4.1 (Hardening).** Este é o achado mais forte do
levantamento. 4.1 tem:
- Objetivo 1: *"e saber o que conformidade não mede"*.
- Objetivo 4: *"e reconhecer o limite do checklist"*.
- `4.1.t6`, título *"O limite do checklist: conformidade não é
  segurança"*, com a frase que o eixo 4 do 3.7 reproduziria quase
  literalmente: *"Ela é indicador de aderência: sobe quando o parque se
  parece com o documento, e não quando o adversário fica mais longe."*
- Uma questão cujo enunciado é quase a mesma pergunta que o eixo 4
  proposto faria: *"O que um checklist de endurecimento, por melhor que
  seja, estruturalmente não consegue fornecer?"*, com dica *"um
  checklist perfeito para uma organização é o mesmo para outra do mesmo
  tamanho?"*

Escrever o eixo 4 como proposto — "cobrir os dez não é estar seguro" —
seria a mesma questão do 4.1 com "Top 10" no lugar de "benchmark CIS".
**Troca proposta**: assumir a crítica geral ao checklist como já
ensinada (referência cruzada a `4.1.t6`) e restringir o eixo à lacuna
**específica do Top 10 por construção**, usando a frase da fonte
reconfirmada hoje: *"largely limited to what the industry can test for
in an automated fashion"* — ou seja, o Top 10 não lista risco de
negócio específico da aplicação, não lista o que ainda não foi
descoberto/testável em escala, e (achado novo da seção 0) tem duas
categorias inteiras que só existem porque alguém votou nelas apesar do
dado automatizado não as enxergar — o que é uma falha de cobertura
**diferente** da falha genérica de checklist que 4.1 já ensina (lá é
"o documento pode estar desatualizado ou não refletir o parque"; aqui é
"o próprio método de construção da lista tem um ponto cego estrutural
para certas categorias de risco").

### Eixo 5 — mapear um achado real para o item certo, e reconhecer quando não pertence a nenhum

**Sem colisão.** Adjacência leve e não-concorrente com 3.1 (achado de
pentest: evidência, reprodução, impacto, correção, classificação de
risco) — 3.1 ensina a escrever o achado; o 3.7 ensinaria uma habilidade
que 3.1 não cobre, mapear esse achado (já escrito) para a categoria
certa da lista, e reconhecer os casos em que ele não se encaixa em
nenhuma das dez. Referência cruzada a 3.1 é oportunidade, não correção
de colisão.

## 4. Território livre confirmado — varredura direta

Buscado no corpus inteiro: `cadeia de suprimentos`, `supply chain`,
`dependência desatualizada`, `integridade de software`, `deserialização`,
`pipeline de build`, `assinatura de pacote`, `exceção não tratada`,
`fail-open`, `stack trace exposto`. Resultado: nenhum módulo publicado
ensina A03 (Software Supply Chain Failures) ou A08 (Software or Data
Integrity Failures) como mecanismo de segurança — só o toque pontual já
citado em 1.7. **Livre para uso como exemplo concreto no eixo 5** (achado
real mapeado para a categoria certa), sem risco de repetir mecanismo já
ensinado em outro módulo — o que também resolve, de graça, o problema de
"a lista percorrida item a item vira repetição": A03 e A08 são os únicos
dois itens da lista que o 3.7 pode usar como **exemplo de mecanismo**
sem pisar em módulo nenhum, porque nenhum outro módulo os ensinou ainda.

## 5. Resumo para decisão

| Eixo | Proposta original | Risco | Encaminhamento |
|---|---|---|---|
| 1 | Como a lista é construída — dados reais, não opinião | Nenhuma colisão de módulo; premissa **factualmente incompleta** | Reformular: metodologia híbrida (8 dados + 2 comunidade), e por quê |
| 2 | Por que a posição muda entre edições | Nenhuma | Manter como está, com citação exata da fonte |
| 3 | Lista como vocabulário comum entre times | **Colisão de argumento** com 4.6 (e eco em 4.5) | Assumir como conhecido (ref. cruzada 4.6.t1); focar no que é específico do Top 10 nesse papel (lado aplicação/dev vs. lado comportamento do 4.6) |
| 4 | Erro de tratar como checklist de conformidade | **Colisão severa** com 4.1 (`4.1.t6` e objetivos 1/4) | Assumir crítica geral como já ensinada (ref. cruzada 4.1.t6); restringir ao ponto cego **específico da construção do Top 10** (o que o método automatizado não enxerga, por que duas categorias tiveram que ser votadas) |
| 5 | Mapear achado para o item certo, e reconhecer quando não pertence a nenhum | Nenhuma; adjacência leve com 3.1 | Manter, com ref. cruzada a 3.1 e uso de A03/A08 como exemplos de mecanismo nunca ensinado |

Nenhum dos cinco eixos precisa ser descartado. Dois (3 e 4) precisam de
reformulação estrutural antes de virar questão, no mesmo padrão já usado
no 3.4/3.5/3.6: assumir o que já foi ensinado como fato dado e escrever
a pergunta que falta, não a que já foi respondida em outro módulo.
