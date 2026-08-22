# Rascunhos do nível 3 — bloco 3.1 a 3.3

Bloco **concluído**: 3.1, 3.2 e 3.3 passaram pelas duas lentes e estão em
`data/modulos/`. O que fica aqui é o rastro — laboratórios, relatórios de
procedência e notas de pesquisa —, que é o que permite reconferir uma questão
sem refazer a investigação. Nada desta pasta é carregado pelo app.

Esta pasta existe porque este material já se perdeu uma vez, quando morava fora
do repositório.

## O que tem aqui

| Pasta | Conteúdo |
|---|---|
| `modulos/` | Vazia: os três módulos do bloco foram revisados e promovidos para `data/modulos/` |
| `relatorios/` | Relatório de procedência de cada módulo (`3.1.md`, `3.2.md`) e as notas de pesquisa das fontes (`metodologia.md`, `osint.md`, `varredura.md`, `owasp-attack.md`, `owasp-versao-VERIFICADA.md`) |
| `lab/` | Os laboratórios executados e a saída real que virou artefato de questão |

## Estado, por módulo

| Módulo | Escrito | Validação estrutural | Revisão adversarial | Em `data/modulos/` |
|---|---|---|---|---|
| 3.1 | sim | passa | **feita** | **sim** — promovido em `3ec2e5c` |
| 3.2 | sim | passa | **feita** | **sim** — promovido em `cc2aad9` |
| 3.3 | sim | passa | **feita** | **sim** — promovido em `48f9dd7` |

O relatório de procedência do 3.3 nunca foi escrito — o processo foi interrompido
antes disso.

## Os laboratórios

Todos rodam **contra alvo próprio**, sem exceção. `recon_lab.py` sobe um alvo
HTTP e um serviço de banner em `127.0.0.1` dentro do próprio processo e varre
esse alvo. `osint_lab.sh` só consulta nomes reservados para documentação
(`example.com`, `.invalid`, RFC 2606). `metadados_lab.py` lê PDFs locais.

```bash
python data/rascunhos/nivel-3/lab/recon_lab.py
```

## O que conferir antes de promover um módulo

1. Sintaxe e comportamento de ferramenta — `nmap`, `gobuster` e `dig` **não estão
   instalados** nesta máquina, então nada disso foi executado: a fonte da questão
   precisa dizer que a sintaxe vem da documentação.
2. OWASP Top 10 — a versão vigente é a **2025**. A de 2021 não pode aparecer como
   atual.
3. Equilíbrio ataque/defesa — o objetivo 3 de cada módulo é o lado defensivo, e a
   meta combinada é de pelo menos 8 questões com contrapartida defensiva.
4. Alvo — nenhum endereço fora de `localhost`, RFC 1918 ou RFC 5737.
5. Tom — é um curso de ofício, não de aventura.

Depois de revisar: `python ferramentas/validar_modulo.py <arquivo>`, mover para
`data/modulos/`, rodar `python -m pytest -q` e commitar.
