# Roteiro de Apresentação — Sistema de Biblioteca (A3 UDWMJ)

Roteiro de apresentação, atendendo à cláusula **3.2/3.3** do contrato: cada item
implementado precisa ser explicado — só entregar vale zero.

- **Tema:** Sistema de gerenciamento de biblioteca.
- **Stack:** Django (MVT) + Django Templates, HTML/CSS/JS puros, Python 3.12, Oracle Autonomous Database (OCI via `oracledb`), ambiente Miniconda (`a3biblioteca`).
- **Equipe:** Mateus Machado, Matheus Iserhard e Lauro.

---

## 1. Visão geral (1 minuto — Mateus)

> "Nosso sistema é um monolito Django organizado em MVT, com **um app por classe** — 12 apps.
> Cada app tem models, views, urls e templates, seguindo o padrão das aulas. O banco é um
> Oracle Autonomous Database na nuvem OCI. Toda integração com o banco é feita pelas migrações
> do Django (`makemigrations` + `migrate`), então os models espelham as tabelas."

Mostre o dashboard (`/`) com os contadores: livros, exemplares disponíveis, empréstimos ativos,
atrasados, multas pendentes e reservas aguardando. Diga que todos são consultas ao banco em tempo real.

---

## 2. Os 12 apps (um bloco por app)

> Formato de cada bloco: **o que é** → **atributos e tipos** → **relacionamentos** →
> **onde está o código** (models / views / urls / templates).

### 2.1 `categorias` — Categoria (Mateus)

- **O que é:** classifica os livros do acervo (romance, realismo, modernismo…).
- **Atributos:** `nome` CharField, `slug` SlugField (unique), `descricao` TextField, `ativa` BooleanField.
- **Relacionamentos:** 1 Categoria → * Livros.
- **Código:** `categorias/models.py`, `categorias/views.py` (CRUD por função), `categorias/urls.py` (`app_name = 'categorias'`), `categorias/templates/categorias/categoria_{list,detail,form,confirm_delete}.html`.

### 2.2 `autores` — Autor (Mateus)

- **O que é:** quem escreveu cada livro.
- **Atributos:** `nome` CharField, `nacionalidade` CharField, `data_nascimento` DateField, `biografia` TextField, `foto` ImageField (upload).
- **Relacionamentos:** * Autor — * Livro (ManyToMany definido em `Livro.autores`).
- **Código:** `autores/models.py`, `autores/views.py`, `autores/urls.py`, `autores/templates/autores/autor_*.html`. A foto mostra miniatura na listagem e tem preview no formulário.

### 2.3 `editoras` — Editora (Mateus)

- **O que é:** a empresa que publica o livro.
- **Atributos:** `nome` CharField, `cnpj` CharField (unique), `email` EmailField, `site` URLField, `cidade` CharField.
- **Relacionamentos:** 1 Editora → * Livros.
- **Código:** `editoras/models.py`, `editoras/views.py`, `editoras/urls.py`, `editoras/templates/editoras/editora_*.html`. O campo CNPJ tem máscara.

### 2.4 `estantes` — Estante (Matheus Iserhard)

- **O que é:** o local físico onde o exemplar fica guardado.
- **Atributos:** `setor` CharField, `corredor` CharField, `prateleira` PositiveIntegerField, `capacidade` IntegerField, `largura_metros` FloatField.
- **Relacionamentos:** 1 Estante → * Exemplares.
- **Código:** `estantes/models.py`, `estantes/views.py`, `estantes/urls.py`, `estantes/templates/estantes/estante_{list,detail,form,confirm_delete}.html`.

### 2.5 `livros` — Livro (Mateus)

- **O que é:** o título do acervo (a obra, não a cópia física).
- **Atributos:** `titulo` CharField, `isbn` CharField (unique), `ano_publicacao` IntegerField, `num_paginas` PositiveIntegerField, `sinopse` TextField, `capa` ImageField (upload), `preco_reposicao` DecimalField, `autores` ManyToManyField, `editora` FK, `categoria` FK.
- **Relacionamentos:** * Livro — * Autor; Editora 1 — * Livro; Categoria 1 — * Livro; 1 Livro → * Exemplares, Reservas e Avaliações.
- **Código:** `livros/models.py`, `livros/views.py`, `livros/urls.py`, `livros/templates/livros/livro_*.html`. A listagem é em **cards com a capa**.

### 2.6 `exemplares` — Exemplar (Mateus)

- **O que é:** cada **cópia física** de um livro no acervo (identificada pelo tombo).
- **Atributos:** `livro` FK, `codigo_tombo` CharField (unique), `estado` CharField (choices: novo/bom/regular/danificado/perdido), `disponivel` BooleanField, `data_aquisicao` DateField, `estante` FK.
- **Relacionamentos:** Livro 1 → * Exemplar; Estante 1 → * Exemplar; 1 Exemplar → * Empréstimos.
- **Método da regra:** `pode_emprestar` — só disponível **e** fora de danificado/perdido.
- **Código:** `exemplares/models.py`, `exemplares/views.py`, `exemplares/urls.py`, `exemplares/templates/exemplares/exemplar_*.html`.

### 2.7 `leitores` — Leitor (Matheus Iserhard)

- **O que é:** quem pode pegar livros emprestados (aluno, professor ou comunidade).
- **Atributos:** `nome` CharField, `cpf` CharField (unique), `email` EmailField, `telefone` CharField, `tipo` CharField (choices: aluno/professor/comunidade), `foto` ImageField (upload), `ativo` BooleanField, `data_cadastro` DateTimeField (auto_now_add).
- **Relacionamentos:** 1 Leitor → * Empréstimos, Reservas e Avaliações.
- **Métodos da regra:** `limite_emprestimos()` (aluno 3, comunidade 2, professor 5) e `possui_multa_pendente()` (consulta `Multa` por `emprestimo__leitor`).
- **Código:** `leitores/models.py`, `leitores/views.py`, `leitores/urls.py`, `leitores/templates/leitores/leitor_*.html`. CPF e telefone têm máscara; a foto tem preview.

### 2.8 `funcionarios` — Funcionario (Matheus Iserhard)

- **O que é:** quem registra os empréstimos no balcão.
- **Atributos:** `nome` CharField, `matricula` CharField (unique), `cargo` CharField (choices: bibliotecário/atendente/auxiliar/gerente), `salario` DecimalField, `hora_entrada` TimeField, `hora_saida` TimeField.
- **Relacionamentos:** 1 Funcionário → * Empréstimos.
- **Código:** `funcionarios/models.py`, `funcionarios/views.py`, `funcionarios/urls.py`, `funcionarios/templates/funcionarios/funcionario_*.html`.

### 2.9 `emprestimos` — Emprestimo ⭐ (Mateus)

- **O que é:** o registro de um livro saindo e voltando; onde fica **toda a regra de negócio central**.
- **Atributos:** `leitor` FK, `exemplar` FK, `funcionario` FK, `data_emprestimo` DateTimeField (auto_now_add), `data_prevista` DateField, `data_devolucao` DateField (nulo), `status` CharField (choices: ativo/devolvido/atrasado).
- **Relacionamentos:** Leitor 1 → * Empréstimo; Exemplar 1 → * Empréstimo; Funcionário 1 → * Empréstimo; Empréstimo 1 — 0..1 Multa.
- **Código:** `emprestimos/models.py` (`clean()`, `esta_atrasado`, `calcular_data_prevista`), `emprestimos/views.py` (`emprestimo_criar` e `emprestimo_devolver` com `transaction.atomic`), `emprestimos/forms.py`, `emprestimos/urls.py`, `emprestimos/templates/emprestimos/emprestimo_*.html`, testes em `emprestimos/tests.py`.

### 2.10 `reservas` — Reserva (Matheus Iserhard)

- **O que é:** a fila de espera por um livro que está emprestado.
- **Atributos:** `leitor` FK, `livro` FK, `data_reserva` DateTimeField (auto_now_add), `posicao_fila` PositiveIntegerField, `status` CharField (choices: aguardando/disponível/cancelada/atendida).
- **Relacionamentos:** Leitor 1 → * Reserva; Livro 1 → * Reserva.
- **Código:** `reservas/models.py` (`save()` calcula `posicao_fila` = última da fila + 1), `reservas/views.py`, `reservas/urls.py`, `reservas/templates/reservas/reserva_*.html`.

### 2.11 `multas` — Multa (Mateus)

- **O que é:** a cobrança gerada pela devolução em atraso.
- **Atributos:** `emprestimo` OneToOneField, `dias_atraso` PositiveIntegerField, `valor` DecimalField, `paga` BooleanField, `data_pagamento` DateField (nulo), `comprovante` FileField (upload, nulo).
- **Relacionamentos:** Empréstimo 1 — 0..1 Multa.
- **Código:** `multas/models.py` (`calcular_valor`), `multas/views.py` (inclui `multa_marcar_paga`), `multas/urls.py`, `multas/templates/multas/multa_*.html`.

### 2.12 `avaliacoes` — Avaliacao (Lauro)

- **O que é:** a nota e o comentário de um leitor sobre um livro.
- **Atributos:** `leitor` FK, `livro` FK, `nota` PositiveSmallIntegerField (1–5, com `MinValueValidator`/`MaxValueValidator`), `comentario` TextField, `data` DateTimeField (auto_now_add).
- **Relacionamentos:** Leitor 1 → * Avaliação; Livro 1 → * Avaliação.
- **Código:** `avaliacoes/models.py`, `avaliacoes/views.py`, `avaliacoes/urls.py`, `avaliacoes/templates/avaliacoes/avaliacao_*.html`.

---

## 3. Regra de negócio central (Empréstimo e Devolução)

Tudo fica nos models/views de `emprestimos` — não está espalhado nos templates.

| # | Regra | Onde está no código |
|---|-------|---------------------|
| 1 | Só empresta exemplar disponível e com estado ≠ danificado/perdido | `Emprestimo.clean()` → `exemplar.pode_emprestar` (`exemplares/models.py`) |
| 2 | Leitor precisa estar ativo e sem multa pendente | `Emprestimo.clean()` → `leitor.ativo` e `leitor.possui_multa_pendente()` (`leitores/models.py`) |
| 3 | Limite simultâneo: aluno 3, comunidade 2, professor 5 | `Emprestimo.clean()` compara com `leitor.limite_emprestimos()` |
| 4 | Prazo automático: 14 dias (professor: 21) | `Emprestimo.calcular_data_prevista()`; usado em `emprestimo_criar` |
| 5 | Ao emprestar: `exemplar.disponivel = False` | `emprestimo_criar` (dentro de `transaction.atomic`) |
| 6 | Devolução: registra data, status devolvido, libera o exemplar | `emprestimo_devolver` (POST + `transaction.atomic`) |
| 7 | Multa automática: R$ 1,00 por dia de atraso | `emprestimo_devolver` (cria `Multa` com `Multa.calcular_valor`) |
| 8 | Reserva: ao devolver, a primeira "aguardando" vira "disponível" | `emprestimo_devolver` (filtra `Reserva.AGUARDANDO`, ordena por `posicao_fila`) |
| 9 | `esta_atrasado` para destacar o atraso na listagem | `Emprestimo.esta_atrasado` (property) + classe CSS `.linha-atrasada`/`.etiqueta-atraso` |

As regras 1, 2, 3 e 7 têm testes automatizados em `emprestimos/tests.py` (10 testes, rodados com
`python manage.py test --settings=biblioteca.settings_test`, usando SQLite em memória).

---

## 4. Matriz de tipos de dados (cláusula 1.8)

| Tipo | Onde é usado |
|------|--------------|
| CharField | nomes, ISBN, CPF, telefone, CNPJ, tombo, matrícula, setor |
| TextField | sinopse, biografia, descrição, comentário |
| IntegerField / PositiveIntegerField / PositiveSmallIntegerField | ano, páginas, prateleira, capacidade, posição na fila, dias de atraso, nota |
| FloatField | largura da estante (medida física) |
| DecimalField | preço de reposição, salário, valor da multa |
| BooleanField | categoria ativa, exemplar disponível, leitor ativo, multa paga |
| DateField | nascimento, aquisição, devolução prevista/real, pagamento |
| DateTimeField | empréstimo, reserva, avaliação, cadastro do leitor |
| TimeField | hora de entrada e de saída do funcionário |
| EmailField / URLField / SlugField | e-mail do leitor e da editora, site da editora, slug da categoria |
| ImageField | capa do livro, foto do autor e foto do leitor |
| FileField | comprovante de pagamento da multa |
| choices | estado do exemplar, status do empréstimo/reserva, tipo de leitor, cargo |
| ForeignKey / ManyToManyField / OneToOneField | todos os relacionamentos |

---

## 5. Otimização do front-end (cláusula 1.17)

HTML + CSS + **JavaScript puro** (sem bibliotecas):

- **Menu agrupado** (Acervo / Pessoas / Circulação) com dropdown em CSS/JS, hambúrguer em telas
  pequenas e item da seção atual destacado (`request.resolver_match.app_name`).
- **Dashboard** com contadores reais e os últimos 5 empréstimos.
- **Busca instantânea** em todas as 12 listagens (filtra linhas de tabela e cards, ignora acentos).
- **Preview da imagem** antes do upload (capa, foto do autor, foto do leitor, comprovante).
- **Máscaras** de CPF, telefone e CNPJ.
- **Confirmação** antes de excluir, registrar devolução e marcar multa como paga.
- CSS responsivo com variáveis, Flexbox/Grid e cards com capa.

Tudo em `static/css/estilo.css` e `static/js/app.js`; o layout global é `templates/base.html`.

---

## 6. Fluxo Git usado

- Repositório do professor: `2026-2-UDWMJ-Quinta-Noite-ZS-04-MVT` (branch `main`).
- `estrutura-inicial` → PR → merge; depois **1 branch por app** (`feature/<app>`) com
  **≥ 4 commits** (models, views, urls, templates) e **1 PR + merge** por branch.
- Merge sempre com "Create a merge commit" (preserva os 4 commits no `main`).
- Ordem respeitando as FKs: categorias → autores → editoras → estantes → livros → exemplares →
  leitores → funcionarios → emprestimos → reservas → multas → avaliacoes; por fim `frontend`.
- Cada membro commita com a própria conta. Segredos (`.env`, wallet) nunca vão ao Git.
- Registro de arquivos por etapa em `docs/publicacao.md`.

---

## 7. Demonstração ao vivo (~10 minutos)

| Tempo | Quem | O que mostrar |
|-------|------|----------------|
| 0:00–1:00 | **Mateus** | Dashboard com os contadores; explicar o monolito MVT e os 12 apps |
| 1:00–5:00 | **Mateus** | Categorias, Autores (upload de foto com preview), Editoras (máscara de CNPJ), Livros (cards com capa), Exemplares (tombo/estado), **Empréstimos** (criar um empréstimo; mostrar prazo automático; tentar emprestar para leitor com multa — bloqueio; registrar uma devolução atrasada e ver a multa R$ 1,00/dia surgir), Multas (marcar como paga) |
| 5:00–8:00 | **Matheus Iserhard** | Estantes, Leitores (máscaras de CPF/telefone, upload da foto, os 3 tipos e os limites 3/2/5), Funcionários (cargo/salário/horário), Reservas (posição na fila automática) — e mostrar a busca instantânea numa listagem |
| 8:00–9:00 | **Lauro** | Avaliações (nota de 1 a 5 com validação, comentário), pesquisar um livro e ver as avaliações |
| 9:00–10:00 | **Mateus** | Fechamento: `python manage.py test --settings=biblioteca.settings_test` (todos passando), Git no GitHub (branches e PRs) e o diagrama de classes em `docs/diagrama_classes.md` |

**Dica:** antes de começar, rode `python manage.py popular_dados --resetar` para deixar os dados
de demonstração num estado limpo e coerente.
