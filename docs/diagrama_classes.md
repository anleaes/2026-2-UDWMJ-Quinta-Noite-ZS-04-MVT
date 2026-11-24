# Diagrama de Classes — Sistema de Biblioteca

Diagrama de classes (UML) do sistema, em **Mermaid** (`classDiagram`).

> **Cláusula 1.4/1.5 do contrato:** este diagrama deve ser apresentado ao
> professor e **validado antes da implementação** dos apps.
>
> Para exportar a imagem (PNG): copie o bloco Mermaid abaixo e cole em
> <https://mermaid.live>, depois use *Actions → Download PNG*.

## Diagrama

```mermaid
classDiagram
    class Categoria {
        +CharField nome
        +SlugField slug
        +TextField descricao
        +BooleanField ativa
        +__str__()
    }

    class Autor {
        +CharField nome
        +CharField nacionalidade
        +DateField data_nascimento
        +TextField biografia
        +ImageField foto
        +__str__()
    }

    class Editora {
        +CharField nome
        +CharField cnpj
        +EmailField email
        +URLField site
        +CharField cidade
        +__str__()
    }

    class Estante {
        +CharField setor
        +CharField corredor
        +PositiveIntegerField prateleira
        +IntegerField capacidade
        +FloatField largura_metros
        +__str__()
        +tem_espaco() bool
    }

    class Livro {
        +CharField titulo
        +CharField isbn
        +IntegerField ano_publicacao
        +PositiveIntegerField num_paginas
        +TextField sinopse
        +ImageField capa
        +DecimalField preco_reposicao
        +ManyToManyField autores
        +ForeignKey editora
        +ForeignKey categoria
        +__str__()
        +exemplares_disponiveis() int
    }

    class Exemplar {
        +ForeignKey livro
        +CharField codigo_tombo
        +CharField estado
        +BooleanField disponivel
        +DateField data_aquisicao
        +ForeignKey estante
        +__str__()
        +pode_emprestar() bool
    }

    class Leitor {
        +CharField nome
        +CharField cpf
        +EmailField email
        +CharField telefone
        +CharField tipo
        +ImageField foto
        +BooleanField ativo
        +DateTimeField data_cadastro
        +__str__()
        +limite_emprestimos() int
        +possui_multa_pendente() bool
    }

    class Funcionario {
        +CharField nome
        +CharField matricula
        +CharField cargo
        +DecimalField salario
        +TimeField hora_entrada
        +TimeField hora_saida
        +__str__()
    }

    class Emprestimo {
        +ForeignKey leitor
        +ForeignKey exemplar
        +ForeignKey funcionario
        +DateTimeField data_emprestimo
        +DateField data_prevista
        +DateField data_devolucao
        +CharField status
        +__str__()
        +clean()
        +registrar_devolucao() Multa
        +esta_atrasado() bool
    }

    class Reserva {
        +ForeignKey leitor
        +ForeignKey livro
        +DateTimeField data_reserva
        +PositiveIntegerField posicao_fila
        +CharField status
        +__str__()
    }

    class Multa {
        +OneToOneField emprestimo
        +PositiveIntegerField dias_atraso
        +DecimalField valor
        +BooleanField paga
        +DateField data_pagamento
        +FileField comprovante
        +__str__()
        +calcular_valor() Decimal
    }

    class Avaliacao {
        +ForeignKey leitor
        +ForeignKey livro
        +PositiveSmallIntegerField nota
        +TextField comentario
        +DateTimeField data
        +__str__()
    }

    Editora "1" --> "*" Livro : publica
    Categoria "1" --> "*" Livro : classifica
    Autor "*" -- "*" Livro : escreve
    Livro "1" --> "*" Exemplar : possui
    Estante "1" --> "*" Exemplar : guarda
    Leitor "1" --> "*" Emprestimo : realiza
    Exemplar "1" --> "*" Emprestimo : emprestado em
    Funcionario "1" --> "*" Emprestimo : registra
    Emprestimo "1" -- "0..1" Multa : gera
    Leitor "1" --> "*" Reserva : faz
    Livro "1" --> "*" Reserva : reservado em
    Leitor "1" --> "*" Avaliacao : avalia
    Livro "1" --> "*" Avaliacao : recebe
```

## Tipos de dados usados (cláusula 1.8)

| Tipo | Contexto lógico |
|------|-----------------|
| CharField | nomes, ISBN, CPF, códigos, cargos |
| TextField | sinopse, biografia, descrição, comentário |
| IntegerField / PositiveIntegerField / PositiveSmallIntegerField | ano, páginas, prateleira, capacidade, dias de atraso, nota |
| FloatField | largura da estante (medida física) |
| DecimalField | preço de reposição, salário, valor da multa |
| BooleanField | ativa, disponível, ativo, paga |
| DateField | nascimento, aquisição, devolução prevista/real |
| DateTimeField | empréstimo, reserva, avaliação, cadastro |
| TimeField | turno do funcionário |
| EmailField / URLField / SlugField | contato, site, URL amigável |
| ImageField | capa do livro, foto do autor e do leitor |
| FileField | comprovante de pagamento da multa |

## Regra de negócio central (classe Emprestimo)

1. Exemplar precisa estar `disponivel` e com estado diferente de danificado/perdido.
2. Leitor precisa estar `ativo` e sem multa pendente.
3. Limite simultâneo: aluno 3, comunidade 2, professor 5.
4. Prazo: 14 dias (professor: 21 dias).
5. Ao emprestar: `exemplar.disponivel = False`.
6. Na devolução: registra data, status `devolvido` e libera o exemplar.
7. Devolução em atraso gera `Multa` (R$ 1,00 por dia).
8. Ao devolver, a primeira `Reserva` aguardando vira `disponivel`.
