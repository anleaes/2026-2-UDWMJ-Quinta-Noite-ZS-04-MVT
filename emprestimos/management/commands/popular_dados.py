"""Comando de gerenciamento: popula o banco com dados de demonstração.

Uso: python manage.py popular_dados
     python manage.py popular_dados --resetar  (apaga os dados e recria)

Pode ser executado mais de uma vez: todos os registros são criados com
get_or_create (as migrações e regras de negócio continuam valendo).
"""
from datetime import timedelta
from decimal import Decimal

from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from autores.models import Autor
from avaliacoes.models import Avaliacao
from categorias.models import Categoria
from editoras.models import Editora
from emprestimos.models import Emprestimo
from estantes.models import Estante
from exemplares.models import Exemplar
from funcionarios.models import Funcionario
from leitores.models import Leitor
from livros.models import Livro
from multas.models import Multa
from reservas.models import Reserva


class Command(BaseCommand):
    help = 'Cria dados realistas de demonstração (sem duplicar se rodar de novo).'

    def add_arguments(self, parser):
        parser.add_argument(
            '--resetar',
            action='store_true',
            help='Apaga os dados de demonstração (na ordem das dependências) antes de recriar.',
        )

    def _resetar(self):
        """Apaga só os dados de demonstração, das tabelas dependentes para as bases."""
        self.stdout.write('Apagando dados de demonstração...')
        for modelo in (
            Multa, Emprestimo, Reserva, Avaliacao,
            Exemplar, Livro, Leitor, Funcionario,
            Estante, Editora, Autor, Categoria,
        ):
            apagados, _ = modelo.objects.all().delete()
            self.stdout.write(f'  {modelo._meta.verbose_name_plural}: {apagados} registro(s) apagado(s)')

    @transaction.atomic
    def handle(self, *args, **options):
        if options['resetar']:
            self._resetar()

        hoje = timezone.localdate()

        # --- Categorias ---
        categorias = {}
        for nome, slug, descricao in [
            ('Romance', 'romance', 'Narrativas de amor e drama social.'),
            ('Realismo', 'realismo', 'Obras da literatura realista brasileira.'),
            ('Modernismo', 'modernismo', 'Autores da Semana de Arte Moderna e depois.'),
        ]:
            categorias[slug], _ = Categoria.objects.get_or_create(
                slug=slug,
                defaults={'nome': nome, 'descricao': descricao, 'ativa': True},
            )

        # --- Autores (brasileiros) ---
        autores = {}
        for nome, nascimento, biografia in [
            ('Machado de Assis', '1839-06-21', 'Escritor carioca, fundador da Academia Brasileira de Letras.'),
            ('Graciliano Ramos', '1892-10-27', 'Autor de Vidas Secas, crítico social do sertão nordestino.'),
            ('Mário de Andrade', '1893-10-09', 'Poeta e romancista, uma das lideranças do Modernismo.'),
            ('Clarice Lispector', '1920-12-10', 'Ucraniana naturalizada brasileira; narrativa introspectiva.'),
        ]:
            autores[nome], _ = Autor.objects.get_or_create(
                nome=nome,
                defaults={
                    'nacionalidade': 'Brasileira',
                    'data_nascimento': nascimento,
                    'biografia': biografia,
                },
            )

        # --- Editoras ---
        editoras = {}
        for nome, cnpj, email, site, cidade in [
            ('Companhia das Letras', '11.111.111/0001-11', 'contato@companhiadasletras.com.br',
             'https://www.companhiadasletras.com.br', 'São Paulo'),
            ('Nova Fronteira', '22.222.222/0001-22', 'contato@novafronteira.com.br',
             'https://www.novafronteira.com.br', 'Rio de Janeiro'),
        ]:
            editoras[nome], _ = Editora.objects.get_or_create(
                cnpj=cnpj,
                defaults={'nome': nome, 'email': email, 'site': site, 'cidade': cidade},
            )

        # --- Estantes ---
        estantes = []
        for setor, corredor, prateleira, capacidade, largura in [
            ('A', '1', 1, 50, 2.0),
            ('A', '2', 1, 40, 1.8),
            ('B', '1', 1, 60, 2.2),
        ]:
            estante, _ = Estante.objects.get_or_create(
                setor=setor, corredor=corredor, prateleira=prateleira,
                defaults={'capacidade': capacidade, 'largura_metros': largura},
            )
            estantes.append(estante)

        # --- Livros clássicos brasileiros (sem capa; a capa entra pela tela) ---
        livros = {}
        for titulo, isbn, ano, paginas, preco, autoria, editora, categoria, sinopse in [
            ('Dom Casmurro', '9788535910663', 1899, 256, '34.90', 'Machado de Assis',
             'Companhia das Letras', 'realismo', 'Bento Santiago narra seu ciúme por Capitu.'),
            ('Memórias Póstumas de Brás Cubas', '9788535910670', 1881, 368, '39.90', 'Machado de Assis',
             'Companhia das Letras', 'realismo', 'Um defunto autor conta a própria vida.'),
            ('Vidas Secas', '9788503012214', 1938, 176, '29.90', 'Graciliano Ramos',
             'Nova Fronteira', 'realismo', 'A família de Fabiano e a seca do sertão.'),
            ('São Bernardo', '9788503012221', 1934, 224, '32.50', 'Graciliano Ramos',
             'Nova Fronteira', 'realismo', 'Paulo Honório e a fazenda, entre ambição e culpa.'),
            ('Macunaíma', '9788503012238', 1928, 208, '27.90', 'Mário de Andrade',
             'Nova Fronteira', 'modernismo', 'O herói sem nenhum caráter e a travessia do Brasil.'),
            ('A Hora da Estrela', '9788535914647', 1977, 96, '24.90', 'Clarice Lispector',
             'Companhia das Letras', 'romance', 'Macabéa, nordestina no Rio, e a narração de Rodrigo S.M.'),
        ]:
            livro, _ = Livro.objects.get_or_create(
                isbn=isbn,
                defaults={
                    'titulo': titulo,
                    'ano_publicacao': ano,
                    'num_paginas': paginas,
                    'preco_reposicao': Decimal(preco),
                    'editora': editoras[editora],
                    'categoria': categorias[categoria],
                    'sinopse': sinopse,
                },
            )
            livro.autores.add(autores[autoria])
            livros[titulo] = livro

        # --- Exemplares (2 por livro), distribuídos pelas estantes ---
        exemplares = {}
        for indice, (titulo, livro) in enumerate(livros.items()):
            for numero in (1, 2):
                tombo = f'T{indice + 1:02d}-{numero}'
                exemplar, _ = Exemplar.objects.get_or_create(
                    codigo_tombo=tombo,
                    defaults={
                        'livro': livro,
                        'estado': 'bom',
                        'disponivel': True,
                        'data_aquisicao': hoje - timedelta(days=120 - indice * 5),
                        'estante': estantes[(indice + numero) % len(estantes)],
                    },
                )
                exemplares[tombo] = exemplar

        # --- Leitores (3 tipos) ---
        leitores = {}
        for nome, cpf, tipo, email in [
            ('Ana Souza', '111.111.111-11', Leitor.ALUNO, 'ana.souza@exemplo.com'),
            ('Bruno Lima', '222.222.222-22', Leitor.ALUNO, 'bruno.lima@exemplo.com'),
            ('Carla Mendes', '333.333.333-33', Leitor.PROFESSOR, 'carla.mendes@exemplo.com'),
            ('Diego Rocha', '444.444.444-44', Leitor.COMUNIDADE, 'diego.rocha@exemplo.com'),
        ]:
            leitores[cpf], _ = Leitor.objects.get_or_create(
                cpf=cpf,
                defaults={
                    'nome': nome, 'email': email,
                    'telefone': '(41) 99999-0000',
                    'tipo': tipo, 'ativo': True,
                },
            )

        # --- Funcionários ---
        funcionarios = {}
        for nome, matricula, cargo, salario, entrada, saida in [
            ('João Pereira', 'FUNC-0001', 'bibliotecario', '4500.00', '08:00', '17:00'),
            ('Maria Alves', 'FUNC-0002', 'atendente', '2200.00', '13:00', '22:00'),
        ]:
            funcionarios[matricula], _ = Funcionario.objects.get_or_create(
                matricula=matricula,
                defaults={
                    'nome': nome, 'cargo': cargo, 'salario': Decimal(salario),
                    'hora_entrada': entrada, 'hora_saida': saida,
                },
            )
        bibliotecario = funcionarios['FUNC-0001']
        atendente = funcionarios['FUNC-0002']

        # --- Empréstimos ---
        # 3 ativos, 1 atrasado, 1 devolvido com atraso e com multa pendente.
        # Colunas: livro, cpf, tombo, dias desde o empréstimo, dias desde a prevista,
        # dias desde a devolução (None = ainda não devolvido), status, funcionário.
        emprestimos_demo = [
            ('Dom Casmurro', '111.111.111-11', 'T01-1', 7, None, None, Emprestimo.ATIVO, bibliotecario),
            ('Vidas Secas', '333.333.333-33', 'T03-1', 3, None, None, Emprestimo.ATIVO, bibliotecario),
            ("Macunaíma", '222.222.222-22', 'T05-1', 5, None, None, Emprestimo.ATIVO, atendente),
            ('São Bernardo', '444.444.444-44', 'T04-1', 20, 6, None, Emprestimo.ATRASADO, atendente),
            ('Memórias Póstumas de Brás Cubas', '222.222.222-22', 'T02-2', 25, 11, 5, Emprestimo.DEVOLVIDO, bibliotecario),
        ]

        for titulo, cpf, tombo, dias_emprestimo, dias_prevista, dias_devolucao, status, funcionario in emprestimos_demo:
            exemplar = exemplares[tombo]
            leitor = leitores[cpf]
            emprestimo, criado = Emprestimo.objects.get_or_create(
                leitor=leitor,
                exemplar=exemplar,
                defaults={
                    'funcionario': funcionario,
                    'data_prevista': hoje - timedelta(days=dias_prevista or 0),
                    'status': status,
                    'data_devolucao': None if dias_devolucao is None else hoje - timedelta(days=dias_devolucao),
                },
            )
            if not criado:
                continue

            # data_emprestimo é auto_now_add: ajusta depois da criação para ficar
            # cronologicamente antes da data prevista.
            Emprestimo.objects.filter(pk=emprestimo.pk).update(
                data_emprestimo=timezone.now() - timedelta(days=dias_emprestimo),
            )

            if status != Emprestimo.DEVOLVIDO:
                # Regra 5: empréstimo em aberto mantém o exemplar indisponível.
                exemplar.disponivel = False
                exemplar.save(update_fields=['disponivel'])
            else:
                # Regra 7: devolução após a data prevista gera multa de R$ 1,00 por dia.
                dias_atraso = dias_prevista - dias_devolucao
                Multa.objects.get_or_create(
                    emprestimo=emprestimo,
                    defaults={
                        'dias_atraso': dias_atraso,
                        'valor': Multa.calcular_valor(dias_atraso),
                        'paga': False,
                    },
                )

        # --- Reservas (livro com exemplares em uso) ---
        for titulo, cpf, status in [
            ('Dom Casmurro', '222.222.222-22', Reserva.AGUARDANDO),
            ('Vidas Secas', '111.111.111-11', Reserva.AGUARDANDO),
        ]:
            Reserva.objects.get_or_create(
                leitor=leitores[cpf],
                livro=livros[titulo],
                status=status,
                defaults={},
            )

        # --- Avaliações ---
        for titulo, cpf, nota, comentario in [
            ('Dom Casmurro', '111.111.111-11', 5, 'Um clássico absoluto.'),
            ('Vidas Secas', '333.333.333-33', 5, 'Linguagem seca e precisa.'),
            ('Macunaíma', '222.222.222-22', 4, 'Difícil, mas genial.'),
            ('A Hora da Estrela', '444.444.444-44', 5, 'Comovente do começo ao fim.'),
        ]:
            Avaliacao.objects.get_or_create(
                leitor=leitores[cpf],
                livro=livros[titulo],
                defaults={'nota': nota, 'comentario': comentario},
            )

        self.stdout.write(self.style.SUCCESS(
            'Dados de demonstração criados: '
            f'{Categoria.objects.count()} categorias, '
            f'{Autor.objects.count()} autores, '
            f'{Editora.objects.count()} editoras, '
            f'{Estante.objects.count()} estantes, '
            f'{Livro.objects.count()} livros, '
            f'{Exemplar.objects.count()} exemplares, '
            f'{Leitor.objects.count()} leitores, '
            f'{Funcionario.objects.count()} funcionários, '
            f'{Emprestimo.objects.count()} empréstimos, '
            f'{Multa.objects.count()} multas, '
            f'{Reserva.objects.count()} reservas, '
            f'{Avaliacao.objects.count()} avaliações.',
        ))
