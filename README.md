# Sistema de Gerenciamento de Biblioteca

Projeto da **A3 de Desenvolvimento Web/POO (UDWMJ — Quinta à Noite, 2026/2)**.
Monolito Django (padrão MVT) para gerenciar acervo, leitores, empréstimos,
reservas e multas de uma biblioteca.

## Disciplina

**2026-2-UDWMJ-Quinta-Noite-ZS-04-MVT**

## Stack

| Item | Tecnologia |
|------|------------|
| Linguagem | Python 3.12 (orientado a objetos) |
| Framework | Django (MVT) |
| Banco de dados | Oracle Database (Autonomous DB — OCI) via `oracledb` |
| Front-end | Django Templates + HTML, CSS e JavaScript puros |
| Ambiente | Miniconda (env `a3biblioteca`) |
| Versionamento | Git + GitHub (1 branch, ≥ 4 commits e 1 PR por app) |

## Funcionalidades

- **12 classes/apps:** Categoria, Autor, Editora, Estante, Livro, Exemplar,
  Leitor, Funcionario, Emprestimo, Reserva, Multa, Avaliacao.
- **CRUD completo** para cada classe (listar, detalhar, criar, editar, excluir).
- **Regra de negócio central de empréstimo:**
  - Só empresta exemplar disponível e em bom estado.
  - Leitor precisa estar ativo e sem multa pendente.
  - Limite simultâneo por tipo de leitor (aluno 3, comunidade 2, professor 5).
  - Prazo de 14 dias (21 para professor).
  - Multa automática de R$ 1,00 por dia de atraso.
  - Devolução libera a próxima reserva da fila.
- **Upload de imagens** (capa de livro, foto de autor/leitor) e **arquivos**
  (comprovante de pagamento da multa).
- **Dashboard** com contadores e front-end responsivo.

## Estrutura

```
biblioteca/          # configuração do projeto Django
<app>/               # um app por classe: models, admin, views, urls, templates
templates/base.html  # layout global (menu, mensagens)
static/css, js/      # estilos e scripts
media/               # uploads (fora do Git)
docs/                # diagrama de classes, cronograma, roteiro de apresentação
```

## Como rodar

Pré-requisitos: Miniconda instalado e credenciais do Oracle Autonomous DB.

```powershell
# 1. Ambiente
conda env create -f environment.yml
conda activate a3biblioteca

# 2. Variáveis de ambiente (crie a partir do modelo)
Copy-Item .env.example .env
# edite .env com ORACLE_USER, ORACLE_PASSWORD, ORACLE_DSN (e wallet, se necessário)

# 3. Banco e usuário admin
python manage.py migrate
python manage.py createsuperuser

# 4. Servidor
python manage.py runserver
```

Acesse <http://127.0.0.1:8000/>.

> ⚠️ O arquivo `.env` contém segredos e **nunca** deve ser commitado
> (o repositório é público).

## Equipe

| Membro | Apps |
|--------|------|
| Mateus Machado | estrutura-inicial, categorias, autores, editoras, livros, exemplares, emprestimos, multas, frontend |
| Matheus Iserhard | estantes, leitores, funcionarios, reservas |
| Lauro | avaliacoes |

## Documentação

- [Diagrama de classes](docs/diagrama_classes.md)
- [Cronograma](docs/cronograma.md)
