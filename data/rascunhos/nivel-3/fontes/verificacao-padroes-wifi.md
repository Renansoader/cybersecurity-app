# Verificação em fonte bruta — evolução dos padrões de proteção sem fio (módulo 3.9)

Verificado em 05/09/2026, via `curl -sL -A "Mozilla/5.0" <url> | grep`, direto no
HTML — sem WebFetch resumido, seguindo a regra 9 do PROGRESS.md (§7): toda
citação literal, número, seção nomeada ou prazo normativo que vá para dentro de
um módulo é confirmado no texto bruto, não em resumo.

Fontes consultadas:
- `https://www.wi-fi.org/discover-wi-fi/security`
- `https://en.wikipedia.org/wiki/WPA3` (citando comunicados da Wi-Fi Alliance)

## O que foi confirmado, com a citação literal

**WPA2 — certificação e obrigatoriedade.** "Certification began in September,
2004. From March 13, 2006, to June 30, 2020, WPA2 certification was mandatory
for all new devices to bear the Wi-Fi trademark."

**WPA3 — certificação e obrigatoriedade.** "Certification began in June 2018,"
e "WPA3 support has been mandatory for devices which bear the 'Wi-Fi
CERTIFIED™' logo since July 2020." Confirmado também no site da Wi-Fi
Alliance: "WPA3 is mandatory for Wi-Fi CERTIFIED devices."

**SAE — origem.** "Simultaneous Authentication of Equals (SAE) exchange, a
method originally introduced with IEEE 802.11s, resulting in a more secure
initial key exchange in personal mode."

**KRACK — o que a falha explora.** "The KRACK attack is believed to affect all
variants of WPA and WPA2; however, the security implications vary between
implementations, depending upon how individual developers interpreted a
poorly specified part of the standard. Software patches can resolve the
vulnerability but are not available for all devices." A falha está na
confirmação de instalação de chave do aperto de mão, não na cifra (AES)
usada para o conteúdo — a página não atribui a falha à força da criptografia
em nenhum momento.

**Modo de transição — segurança documentada como inadequada.** "Concerns
were also raised about the inadequate security in transitional modes
supporting both WPA2 and WPA3."

**Falhas de 2021 (FragAttacks) — categoria de problema, não mecanismo
detalhado.** Seção própria da página ("FragAttacks"): "In May 2021
FragAttacks, a set of new security vulnerabilities, were revealed... These
include design flaws in the Wi-Fi standard, affecting most devices, and
programming errors in Wi-Fi products, making almost all Wi-Fi products
vulnerable. The vulnerabilities impact all Wi-Fi security protocols,
including WPA3 and WEP."

**WEP — por que foi abandonado.** "WEP was once widely used, but its
significant vulnerabilities led to the adoption of more secure protocols."
Chave estática (64 ou 128 bits, não muda sozinha) e verificação de
integridade por CRC, descrita como insuficientemente forte.

## Correção feita depois da revisão adversarial

A primeira versão do bloco `3.9.t4` descrevia o mecanismo do FragAttacks como
"processamento de quadros... como fragmentos e agregações de pacote são
remontados" — mais específico do que a fonte consultada realmente afirma. A
página cita duas categorias (falha de projeto do padrão; erro de programação
na implementação), sem detalhar o mecanismo de fragmentação/agregação nesses
termos. Corrigido para citar só as duas categorias verificadas.

## O que NÃO virou pergunta com resposta decorável

Por instrução explícita do usuário, nenhum nome de padrão, número de norma
ou ano é resposta correta de questão neste módulo — os fatos acima entram
como contexto de teoria, e as questões testam o raciocínio (por que a
compatibilidade cria a lacuna, por que a falha do aperto de mão não é uma
falha de cifra, por que abrangência ampla indica falha de especificação),
nunca "em que ano" ou "qual é o nome do padrão".
