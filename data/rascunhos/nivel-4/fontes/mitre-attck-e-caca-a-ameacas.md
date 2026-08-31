# Fontes — módulo 4.6 (MITRE ATT&CK e caça a ameaças)

Levantado em 30–31/08/2026. Sessão com acesso à rede — as fontes documentais
abaixo foram conferidas, não recuperadas de memória.

## Verificado em execução nesta máquina

| Onde aparece | O que foi executado | O que sustenta |
|---|---|---|
| `4.6.t2`, `4.6.t3`, q11, q12, q13, q14, q15, q16, q17 | `lab/mapear_comportamento.py` | Autostart real via `Get-CimInstance Win32_StartupCommand`: Discord e tipspace rodam de `AppData\Local` do usuário, com nome de atualizador genérico e sem privilégio elevado — mesma forma de um padrão de persistência conhecido, e nenhum dos dois é malicioso |
| `4.6.t4`, `4.6.t5`, q21, q22, q23, q24, q25 | `lab/caca_sem_hipotese.py` | Contagem real de eventos por hora no log System, últimas 48h: pico de **560 eventos às 00:00**, **9,3× a média de 60,0** — horário de manutenção do sistema, não indício de ataque |

### Limitação declarada

`Win32_StartupCommand` não cobre toda superfície de persistência possível
(serviços, tarefas agendadas e WMI subscriptions ficam de fora); o
laboratório também consultou `Get-ScheduledTask`, mas os dados de tarefa
agendada não entraram como artefato de questão — só o autostart via
Win32_StartupCommand foi usado, por ser mais direto de anonimizar e citar.

### Anonimização

O usuário real desta máquina foi substituído por `ana.silva` na saída salva,
seguindo a convenção já usada em 2.5/2.6/3.x deste corpus. Nenhum caminho,
SID ou nome de máquina real aparece em nenhum artefato do módulo.

## Documental, conferido nesta sessão

- **MITRE ATT&CK** — estrutura tática/técnica/procedimento, framework mantido
  e ativamente atualizado; já citado como fonte em seis módulos deste corpus
  (0.2, 0.3, 1.1–1.4, 3.2), nunca antes como estrutura ensinada. Nenhuma
  questão usa ID de técnica (como T1547.001) como resposta correta —
  conferido por varredura no arquivo final, zero ocorrências de padrão
  `T1\d{3}` fora de comentário interno de laboratório.
- **MITRE ATT&CK Navigator** — ferramenta de visualização de cobertura por
  técnica, conferida como o formato de referência que popularizou o "mapa de
  células coloridas"; citada de forma genérica, sem amarrar nenhuma resposta
  a uma versão específica da ferramenta.
- **Threat hunting hipótese-orientado** — prática consolidada na literatura
  de operação de SOC; nenhuma fonte única e datada foi tratada como norma
  vigente a ser citada por revisão.

## Conhecimento consolidado, sem norma única citada

- **Viés de confirmação / apofenia** aplicado a dados de segurança é
  vocabulário consolidado da psicologia cognitiva e da prática de análise de
  inteligência, sem definição normativa única — o mecanismo em si (sempre
  existe um valor máximo numa lista) é demonstrado por execução real, não
  por citação de fonte.

## Limites de escopo respeitados

`nao-repetir-4.6.md`, escrito antes do módulo, documentou a sobreposição
mais arriscada do nível 4: MITRE ATT&CK já citado como fonte em seis
módulos, vetor/ponto de entrada/movimento lateral já ensinados em 0.2,
cadeia de infecção como decisões já ensinada em 4.4, e três achados de 4.5
(pergunta antes da regra, regra nunca testada, contagem ≠ eficácia) próximos
o bastante para exigir reformulação deliberada, não só verificação de
palavra. Os eixos 3 (caça guiada por hipótese) e 4 (limite do mapa de
cobertura) foram reformulados antes da escrita — decisão registrada no
próprio arquivo `nao-repetir-4.6.md` — para diferenciar mecanismo e modo de
falha do 4.5, em vez de reaplicar o argumento com outro nome. A regra 5 do
validador não acusou nenhuma duplicação no corpus depois de o módulo
escrito.

## Restrição de conteúdo, deliberada

O módulo ensina a **classificar e a caçar**, não a operar uma ferramenta de
SIEM ou de gestão de caso específica. Nenhuma questão depende de um produto
comercial nomeado; os exemplos de autostart vêm de aplicativos reais e
legítimos desta máquina, nunca de malware real, amostra ou técnica de evasão
utilizável.
