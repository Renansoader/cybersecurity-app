# Rascunhos do nível 3 — bloco 3.1 a 3.3

Conteúdo **escrito e ainda não revisado**. Nada daqui é carregado pelo app: o
`content.carregar_modulos()` só lê `data/modulos/`. Um módulo só sai desta pasta
depois de passar pela revisão e pelo validador.

Esta pasta existe porque este material já se perdeu uma vez, quando morava fora
do repositório.

## O que tem aqui

| Pasta | Conteúdo |
|---|---|
| `modulos/` | Os módulos ainda não promovidos: 3.2 OSINT e reconhecimento, 3.3 varredura e enumeração. 35 questões cada |
| `relatorios/` | Relatório de procedência de cada módulo (`3.1.md`, `3.2.md`) e as notas de pesquisa das fontes (`metodologia.md`, `osint.md`, `varredura.md`, `owasp-attack.md`, `owasp-versao-VERIFICADA.md`) |
| `lab/` | Os laboratórios executados e a saída real que virou artefato de questão |

## Estado, por módulo

| Módulo | Escrito | Validação estrutural | Revisão adversarial | Em `data/modulos/` |
|---|---|---|---|---|
| 3.1 | sim | passa | **feita** | **sim** — promovido em `3ec2e5c` |
| 3.2 | sim | passa | pendente | não |
| 3.3 | sim | passa | pendente | não |

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
