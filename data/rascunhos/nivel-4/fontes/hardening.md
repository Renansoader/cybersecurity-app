# Fontes do módulo 4.1 — Hardening

Levantamento feito pelo fio principal em 22/08/2026, direto na fonte. Cada item
diz se foi **[CONFIRMADO]** na fonte primária nesta rodada ou se é
**[CONSOLIDADO]**, conhecimento corrente que não foi reaberto aqui.

---

## 1. Gestão de patch — o ponto onde o material de treinamento está desatualizado

**A BOD 22-01 foi revogada.** [CONFIRMADO]
A CISA publicou a **BOD 26-04 — Prioritizing Security Updates Based on Risk**,
emitida em **10 de junho de 2026**, que supersede e revoga a BOD 19-02 e a
BOD 22-01 (de 03/11/2021). A página da BOD 22-01 no site da CISA aparece hoje
marcada como *(Revoked)*.
Fonte: <https://www.cisa.gov/news-events/directives/bod-26-04-prioritizing-security-updates-based-risk>
e a listagem de diretivas da CISA.

**Os prazos antigos não valem mais como regra.** [CONFIRMADO]
A BOD 22-01 impunha **6 meses** para CVE com identificador anterior a 2021 e
**duas semanas** para os demais. Esses dois números são o que praticamente todo
curso ainda ensina — e são exatamente o que a BOD 26-04 substituiu.

**O modelo novo é por risco, não por prazo fixo.** [CONFIRMADO no conceito,
[CONSOLIDADO] na tabela exata de faixas]
A urgência passa a sair da combinação de: o ativo está exposto publicamente?
a vulnerabilidade está no KEV? o adversário consegue automatizar todos os passos
da exploração? mais o impacto técnico. As janelas resultantes vão de **três dias**
no pior caso até corrigir na próxima atualização do sistema, no melhor.
Calendário de adoção: políticas de agência ajustadas até **07/08/2026**, e
avaliação e correção seguindo os prazos da BOD 26-04 a partir de **07/12/2026**.
Fonte do calendário: aviso do FedRAMP <https://www.fedramp.gov/notices/0014/>.

**O KEV continua existindo e continua sendo da CISA.** [CONFIRMADO]
O que mudou foi o papel dele: de gatilho de prazo fixo para um dos fatores da
decisão de prioridade.

**NIST SP 800-40 Rev. 4** [CONFIRMADO]
Título exato: *Guide to Enterprise Patch Management Planning: Preventive
Maintenance for Technology*, **abril de 2022**. É a revisão vigente e supersede a
Rev. 3, de julho de 2013. Enquadra patch como manutenção preventiva e "custo de
fazer negócio", e recomenda estratégia corporativa em vez de esforço caso a caso.
Fonte: <https://csrc.nist.gov/pubs/sp/800/40/r4/final>

**EPSS** [CONFIRMADO]
Definição literal do FIRST: *"The Exploit Prediction Scoring System (EPSS) is a
data-driven machine-learning model that estimates the probability that a published
CVE will be exploited in the wild in the next 30 days."* Nota de 0 a 1, mais
percentil. Mantido pelo EPSS Special Interest Group do FIRST, com as notas geradas
pela Empirical Security. Serve para priorizar, ao lado de CVSS e KEV — não para
substituir nenhum dos dois.
Fonte: <https://www.first.org/epss/>

---

## 2. Linha de base e benchmarks

**CIS Critical Security Controls v8.1 é a versão vigente.** [CONFIRMADO]
A página do projeto se refere à v8.1 como versão corrente, com v8 e v7.1 citadas
como anteriores. A data exata de publicação não apareceu na página lida — **não
cravar dia nem mês**.
Fonte: <https://www.cisecurity.org/controls>

**Grupos de implementação (IG1, IG2, IG3)** [CONSOLIDADO]
A página lida não descreve os grupos. A ideia corrente é que o IG1 é a higiene
cibernética essencial, e IG2 e IG3 acrescentam controles conforme o porte e o
perfil de ameaça da organização. **Não foi reconfirmado aqui** — se virar questão,
declarar como conhecimento consolidado.

**Perfis Level 1 e Level 2 dos CIS Benchmarks** [CONSOLIDADO]
Level 1 é o conjunto que se espera aplicável sem quebrar a operação; Level 2 é
defesa em profundidade para ambiente que tolera restrição maior, com custo
operacional maior. Não reaberto na fonte nesta rodada.

**NIST SP 800-123 — Guide to General Server Security** [CONFIRMADO]
**Julho de 2008.** A página do CSRC não traz nota de retirada ou substituição, e o
documento segue listado como final. Ou seja: continua válido como referência, e é
**de 2008** — citar sempre com a data, porque o exemplo tecnológico envelheceu.
Fonte: <https://csrc.nist.gov/pubs/sp/800/123/final>

**NIST SP 800-70 (National Checklist Program)** [CONSOLIDADO]
Não foi aberto nesta rodada. Se entrar no conteúdo, verificar a revisão vigente
antes.

**Menor funcionalidade no NIST SP 800-53** [CONSOLIDADO]
O controle costuma ser citado como **CM-7, Least Functionality**. O identificador
não foi reconferido nesta rodada; declarar como consolidado ou verificar antes de
afirmar o código do controle.

---

## 3. Específicos de sistema — todos [CONSOLIDADO], nenhum reaberto aqui

- **SMBv1 no Windows**: desabilitado ou removido por padrão nas instalações
  recentes de Windows 10/11 e Windows Server. A tentativa de consultar o estado
  nesta máquina falhou: `Get-WindowsOptionalFeature` exige elevação, e o
  laboratório é somente leitura. Não afirmar versão exata sem verificar.
- **WDAC x AppLocker**: a orientação corrente da Microsoft é preferir o Windows
  Defender Application Control para política nova, com o AppLocker no papel de
  complemento ou legado.
- **Security Compliance Toolkit**: o que a Microsoft distribui com as linhas de
  base dela para Windows.
- **OpenSCAP / SCAP Security Guide**: perfis de conformidade para Linux, com
  perfis por norma. O que a distribuição entrega por padrão varia.

---

## 4. O limite da prática — o que o módulo precisa ensinar

[CONSOLIDADO, com apoio parcial nas fontes acima]

- Aplicar benchmark inteiro, sem exceção, quebra sistema em produção. Por isso os
  benchmarks vêm em perfis, e por isso existe **desvio autorizado** (exceção
  registrada, com dono, prazo e justificativa) como parte do processo — não como
  falha do processo.
- Conformidade mede distância entre o declarado e o real. Não mede segurança:
  uma linha de base pode estar 100% aplicada e proteger contra a ameaça errada.
- Checklist não substitui modelo de ameaça. A BOD 26-04 é o exemplo institucional
  disso: ela troca prazo uniforme por decisão que olha exposição e explorabilidade
  do caso concreto.

---

## ARMADILHAS: o que NÃO escrever

1. **"O KEV obriga a corrigir em 15 dias"** — era a BOD 22-01, revogada em 2026.
   Hoje o prazo sai do modelo de risco da BOD 26-04, e o piso é de três dias no
   pior caso.
2. **"A BOD 22-01 é a diretiva vigente"** — está marcada como revogada.
3. **"CIS Controls v8"** como versão atual — a vigente é a **v8.1**.
4. **"NIST SP 800-40 Rev. 3"** — superada pela Rev. 4, de abril de 2022.
5. **Citar o SP 800-123 sem a data** — é de 2008; vale o princípio, não o exemplo.
6. **"EPSS mede gravidade"** — mede probabilidade de exploração em 30 dias; a
   gravidade é o CVSS, e as duas coisas respondem perguntas diferentes.
7. **"Hardening é aplicar o benchmark inteiro"** — sem exceção documentada, isso
   derruba serviço e vira desculpa para desligar o programa.
8. **Afirmar o estado do SMBv1 nesta máquina** — não foi possível consultar sem
   elevação, e o laboratório é somente leitura.
