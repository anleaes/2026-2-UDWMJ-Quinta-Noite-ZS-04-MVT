# Cronograma de Atividades — A3 UDWMJ (Sistema de Biblioteca)

Cláusula 2.3 do contrato: cronograma de atividades com prazos e responsáveis.

## Equipe

| Membro | Apps sob responsabilidade |
|--------|---------------------------|
| Mateus Machado | estrutura-inicial, `categorias`, `autores`, `editoras`, `livros`, `exemplares`, `emprestimos` ⭐, `multas`, `frontend` |
| Matheus Iserhard | `estantes`, `leitores`, `funcionarios`, `reservas` |
| Lauro | `avaliacoes` |

## Cronograma

| Data | Marco | Responsável | Atividades |
|------|-------|-------------|-----------|
| Seg 23/11 | Arrancada | Mateus | Fases 0, 1 e 2 locais: ambiente Miniconda, diagrama, cronograma, Django + Oracle; diagrama enviado ao professor |
| Ter 24/11 | Base no Git + cadastros | Mateus / Matheus Iserhard | Push da `estrutura-inicial` (assim que sair o convite); `categorias`, `autores`, `editoras` (Mateus); `estantes`, `leitores`, `funcionarios` (Matheus Iserhard) |
| Qua 25/11 | Núcleo | Mateus / Matheus Iserhard / Lauro | `livros`, `exemplares`, `emprestimos`, `multas` + regra de negócio (Mateus); `reservas` (Matheus Iserhard); `avaliacoes` (Lauro) |
| **Qui 26/11** | **Aprovação para apresentação** (presença obrigatória de todos) | Todos | Versão funcional; mostrar diagrama, cronograma e Git |
| 27/11–01/12 | Garantia / polimento | Todos | Front-end, dados demo, correções pedidas pelo professor |
| Ter 02/12 | Ensaio | Todos | Cada um explica os próprios apps; revisão do checklist |
| **Qui 03/12** | **Apresentação final** | Todos | Demonstração + explicação de cada item |

## Fluxo por app (cláusula 1.15/1.16)

Para cada app: branch `feature/<app>` a partir da `main` atualizada,
**≥ 4 commits** (Models, Views, Urls, Templates), **1 push**, **1 Pull Request** e
**1 merge** na `main`.

Ordem dos apps (respeitando dependências de chave estrangeira):

categorias → autores → editoras → estantes → livros → exemplares → leitores →
funcionarios → emprestimos → reservas → multas → avaliacoes → frontend

## Entregáveis de documentação

| Entregável | Prazo | Responsável |
|------------|-------|-------------|
| `docs/diagrama_classes.md` validado pelo professor | 23/11 | Mateus |
| `docs/cronograma.md` | 23/11 | Mateus |
| `README.md` | 23/11 | Mateus |
| `docs/roteiro_apresentacao.md` | 02/12 | Todos |
