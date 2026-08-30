# Fontes — módulo 4.5 (SIEM e monitoramento)

Levantado em 30/08/2026. Sessão com acesso à rede — as fontes abaixo foram
conferidas, não recuperadas de memória.

## Verificado em execução nesta máquina

| Onde aparece | O que foi executado | O que sustenta |
|---|---|---|
| `4.5.t1`, `4.5.t6`, q1, q3, q4, q6, q7, q9 | `lab/volume_de_eventos.py` | **642 eventos/24h no log System, 140 na Application**, média de **807 bytes/evento**. Projeção para 500 e 2000 máquinas mostra a razão **365/90 ≈ 4,06×** entre reter 1 ano e reter 90 dias — constante em qualquer escala de parque |
| `4.5.t5`, `4.5.t6`, q28, q29, q30 | `lab/validar_deteccao.py` | um arquivo-marcador criado de propósito foi detectado em **0,023s** por uma varredura própria — evidência mecânica de que "provocar o evento" transforma opinião sobre uma regra em medição real |
| q23 | `lab/frequencia_eventid.py` | EventID 28 (58), 6 (45), 112 (42), 55 (36), 29 (33), 16 (22), **10016 (19)**, 1 (16) — no log System desta máquina, últimas 24h |

### Limitação declarada

O log Security do Windows exige elevação administrativa, não disponível nesta
sessão. Os números de volume vêm só de System e Application — o texto e as
questões dizem isso explicitamente (`4.5.t1`, artefato de `4.5.q3`), em vez de
apresentar um número parcial como se fosse o total. Security tende a pesar mais
que os outros dois somados, o que é uma limitação a favor da cautela, não uma
lacuna escondida.

## Verificado por especificação pública, sem execução multiplataforma

Esta máquina roda Windows; não havia Linux disponível nesta sessão para gerar
uma linha real de `/var/log/auth.log`. O artefato de `4.5.q11` (três formatos do
mesmo evento) combina:

- **Evento 4625 do Windows** — campos documentados publicamente pela Microsoft
  (Account Name, Source Network Address, Failure Reason, Logon Type).
- **Linha de `/var/log/auth.log`** — formato de texto livre do OpenSSH,
  extremamente estável há décadas, no mesmo padrão já usado em `1.1.q12` deste
  corpus (`Failed password for invalid user ... from ... port ... ssh2`).
- **JSON de login de nuvem** — forma estrutural típica de log de auditoria de
  nuvem (evento, IP de origem, identidade do usuário, resultado), ilustrativa e
  genérica, sem citar nenhum provedor específico.

Endereço IP (203.0.113.44) é da faixa reservada para documentação (RFC 5737);
usuário (ana.silva) e domínio (CONTOSO) seguem a convenção de anonimização já
em uso no corpus.

## Documental, conferido nesta sessão

- **NIST SP 800-92**, *Guide to Computer Security Log Management* (2006) —
  ainda é a publicação final vigente; a revisão 1 (*Cybersecurity Log
  Management Planning Guide*) segue em rascunho público desde 2023, sem
  finalização confirmada nesta consulta. Nenhuma questão usa número de revisão
  ou data de publicação como resposta certa — mesma regra já aplicada em 4.4.
- **OCSF (Open Cybersecurity Schema Framework)** — conferido como iniciativa
  ativa e em uso, com consórcio de fornecedores (Splunk, AWS, CrowdStrike,
  Palo Alto Networks e outros). Citado como vocabulário consolidado, sem
  amarrar nenhuma resposta a uma versão específica do esquema.
- **Elastic Common Schema (ECS)** e **Splunk Common Information Model (CIM)** —
  citados como exemplos adicionais do mesmo problema resolvido por convenção de
  mercado, não como norma única.
- **MTTD (mean time to detect)** — métrica de operação de SOC amplamente
  documentada e estável no vocabulário da área; usada como conceito, sem
  número de benchmark de mercado citado como fato (esses números mudam de
  pesquisa para pesquisa e não sustentam nenhuma resposta certa).

## Conhecimento consolidado, sem norma única citada

- **EventID 10016** (erro de permissão DCOM) é citado na literatura de
  administração Windows como um dos eventos mais recorrentes e menos
  acionáveis de um parque — usado no artefato de `4.5.q23` como exemplo real
  de ruído de plataforma, não como afirmação normativa.
- **"Fadiga de alerta é defeito de engenharia, não de disciplina"** é
  enquadramento pedagógico deste módulo, apoiado em achados já publicados no
  corpus (`3.3.q30`, `4.2.q12`) e generalizado como princípio — declarado como
  tal em `4.5.t4`.

## Limites de escopo respeitados

`nao-repetir-4.5.md` foi escrito antes deste módulo e listou os pontos de maior
risco de colisão: a métrica "tempo até detectar" já é resposta certa em
`0.3.q13` e `0.3.q30` (argumento estratégico — por que detecção importa);
aqui ela entra como argumento operacional — o que decide se o monitoramento
funciona, contra contar regra e contar alerta. A regra 5 do validador (resposta
certa × resposta certa entre módulos) não acusou nenhuma duplicação no corpus
depois de o módulo escrito.

## Restrição de conteúdo, deliberada

O módulo ensina a **decidir e a validar**, não a operar uma ferramenta de SIEM
específica. Nenhuma questão depende de um produto comercial nomeado, nenhum
comando ou regra de correlação real de produção é reproduzido — os exemplos de
regra são ilustrativos, construídos para o ensino do eixo, não copiados de
nenhum ambiente real.
