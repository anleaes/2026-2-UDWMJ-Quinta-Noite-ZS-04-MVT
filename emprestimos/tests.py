"""Testes da regra de negócio de empréstimo e devolução (regras 1 a 9 do empréstimo)."""
from datetime import timedelta
from decimal import Decimal

from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone

from categorias.models import Categoria
from editoras.models import Editora
from emprestimos.models import Emprestimo
from estantes.models import Estante
from exemplares.models import Exemplar
from funcionarios.models import Funcionario
from leitores.models import Leitor
from livros.models import Livro
from multas.models import Multa


class BaseEmprestimoTest(TestCase):
    """Cria os dados mínimos usados por todos os testes."""

    def setUp(self):
        categoria = Categoria.objects.create(nome='Romance', slug='romance', descricao='x', ativa=True)
        editora = Editora.objects.create(nome='Editora X', cnpj='00', email='e@x.com', site='https://x.com', cidade='Curitiba')
        estante = Estante.objects.create(setor='A', corredor='1', prateleira=1, capacidade=10, largura_metros=1.5)
        self.livro = Livro.objects.create(
            titulo='Livro Teste', isbn='9780000000001', ano_publicacao=2020, num_paginas=100,
            preco_reposicao=Decimal('50.00'), editora=editora, categoria=categoria,
        )
        self.funcionario = Funcionario.objects.create(
            nome='Ana', matricula='F1', cargo='atendente', salario=Decimal('2000.00'),
            hora_entrada='08:00', hora_saida='17:00',
        )
        self.estante = estante

    def criar_exemplar(self, tombo, **kwargs):
        dados = {
            'livro': self.livro, 'codigo_tombo': tombo, 'estado': 'bom',
            'disponivel': True, 'data_aquisicao': timezone.localdate(), 'estante': self.estante,
        }
        dados.update(kwargs)
        return Exemplar.objects.create(**dados)

    def criar_leitor(self, cpf, tipo=Leitor.ALUNO, ativo=True):
        return Leitor.objects.create(
            nome=f'Leitor {cpf}', cpf=cpf, email=f'{cpf}@x.com', telefone='41 9999',
            tipo=tipo, ativo=ativo,
        )


class EmprestimoRegrasTest(BaseEmprestimoTest):
    def test_regra1_recusa_exemplar_indisponivel(self):
        """Regra 1: só empresta exemplar disponível."""
        exemplar = self.criar_exemplar('T1', disponivel=False)
        leitor = self.criar_leitor('111')
        emprestimo = Emprestimo(leitor=leitor, exemplar=exemplar, funcionario=self.funcionario)
        with self.assertRaises(ValidationError):
            emprestimo.full_clean()

    def test_regra1_recusa_exemplar_danificado(self):
        """Regra 1: exemplar danificado não pode ser emprestado, mesmo disponível."""
        exemplar = self.criar_exemplar('T2', estado='danificado')
        leitor = self.criar_leitor('112')
        emprestimo = Emprestimo(leitor=leitor, exemplar=exemplar, funcionario=self.funcionario)
        with self.assertRaises(ValidationError):
            emprestimo.full_clean()

    def test_regra2_recusa_leitor_inativo(self):
        """Regra 2: leitor precisa estar ativo."""
        exemplar = self.criar_exemplar('T3')
        leitor = self.criar_leitor('113', ativo=False)
        emprestimo = Emprestimo(leitor=leitor, exemplar=exemplar, funcionario=self.funcionario)
        with self.assertRaises(ValidationError):
            emprestimo.full_clean()

    def test_regra2_recusa_leitor_com_multa_pendente(self):
        """Regra 2: leitor com multa não paga não pode emprestar."""
        exemplar = self.criar_exemplar('T4')
        leitor = self.criar_leitor('114')
        anterior = Emprestimo.objects.create(
            leitor=leitor, exemplar=exemplar, funcionario=self.funcionario,
            data_prevista=timezone.localdate() - timedelta(days=2),
        )
        Multa.objects.create(emprestimo=anterior, dias_atraso=2, valor=Decimal('2.00'), paga=False)

        self.assertTrue(leitor.possui_multa_pendente())
        outro = self.criar_exemplar('T5')
        emprestimo = Emprestimo(leitor=leitor, exemplar=outro, funcionario=self.funcionario)
        with self.assertRaises(ValidationError):
            emprestimo.full_clean()

    def test_regra2_multa_paga_libera_o_leitor(self):
        """Multa paga não bloqueia novos empréstimos."""
        exemplar = self.criar_exemplar('T6')
        leitor = self.criar_leitor('115')
        anterior = Emprestimo.objects.create(
            leitor=leitor, exemplar=exemplar, funcionario=self.funcionario,
            data_prevista=timezone.localdate() - timedelta(days=2),
        )
        Multa.objects.create(emprestimo=anterior, dias_atraso=2, valor=Decimal('2.00'), paga=True)

        self.assertFalse(leitor.possui_multa_pendente())

    def test_regra3_limite_do_aluno(self):
        """Regra 3: aluno pode ter no máximo 3 empréstimos ativos."""
        leitor = self.criar_leitor('116', tipo=Leitor.ALUNO)
        for i in range(3):
            exemplar = self.criar_exemplar(f'A{i}')
            Emprestimo.objects.create(
                leitor=leitor, exemplar=exemplar, funcionario=self.funcionario,
                data_prevista=timezone.localdate() + timedelta(days=14),
            )
        quarto = self.criar_exemplar('A9')
        emprestimo = Emprestimo(leitor=leitor, exemplar=quarto, funcionario=self.funcionario)
        with self.assertRaises(ValidationError):
            emprestimo.full_clean()

    def test_regra3_limite_da_comunidade(self):
        """Regra 3: leitor da comunidade pode ter no máximo 2 empréstimos ativos."""
        leitor = self.criar_leitor('117', tipo=Leitor.COMUNIDADE)
        for i in range(2):
            exemplar = self.criar_exemplar(f'C{i}')
            Emprestimo.objects.create(
                leitor=leitor, exemplar=exemplar, funcionario=self.funcionario,
                data_prevista=timezone.localdate() + timedelta(days=14),
            )
        terceiro = self.criar_exemplar('C9')
        emprestimo = Emprestimo(leitor=leitor, exemplar=terceiro, funcionario=self.funcionario)
        with self.assertRaises(ValidationError):
            emprestimo.full_clean()

    def test_regra3_professor_tem_limite_maior(self):
        """Regra 3: professor pode ter até 5 empréstimos ativos."""
        leitor = self.criar_leitor('118', tipo=Leitor.PROFESSOR)
        for i in range(4):
            exemplar = self.criar_exemplar(f'P{i}')
            Emprestimo.objects.create(
                leitor=leitor, exemplar=exemplar, funcionario=self.funcionario,
                data_prevista=timezone.localdate() + timedelta(days=21),
            )
        quinto = self.criar_exemplar('P9')
        emprestimo = Emprestimo(leitor=leitor, exemplar=quinto, funcionario=self.funcionario)
        # Prazo do professor: 21 dias.
        self.assertEqual(emprestimo.prazo_em_dias(), 21)
        emprestimo.data_prevista = emprestimo.calcular_data_prevista()
        emprestimo.full_clean()  # 5º empréstimo ainda é permitido


class DevolucaoTest(BaseEmprestimoTest):
    def test_regra7_devolucao_com_atraso_gera_multa(self):
        """Regra 7: devolução após a data prevista cria multa de R$ 1,00 por dia."""
        exemplar = self.criar_exemplar('D1', disponivel=False)
        leitor = self.criar_leitor('200')
        emprestimo = Emprestimo.objects.create(
            leitor=leitor, exemplar=exemplar, funcionario=self.funcionario,
            data_prevista=timezone.localdate() - timedelta(days=4),
        )
        resposta = self.client.post(f'/emprestimos/{emprestimo.pk}/devolver/')
        self.assertEqual(resposta.status_code, 302)

        emprestimo.refresh_from_db()
        exemplar.refresh_from_db()
        self.assertEqual(emprestimo.status, Emprestimo.DEVOLVIDO)
        self.assertIsNotNone(emprestimo.data_devolucao)
        self.assertTrue(exemplar.disponivel)

        multa = Multa.objects.get(emprestimo=emprestimo)
        self.assertEqual(multa.dias_atraso, 4)
        self.assertEqual(multa.valor, Decimal('4.00'))
        self.assertFalse(multa.paga)

    def test_regra7_devolucao_no_prazo_nao_gera_multa(self):
        """Devolução no prazo não cria multa."""
        exemplar = self.criar_exemplar('D2', disponivel=False)
        leitor = self.criar_leitor('201')
        emprestimo = Emprestimo.objects.create(
            leitor=leitor, exemplar=exemplar, funcionario=self.funcionario,
            data_prevista=timezone.localdate() + timedelta(days=1),
        )
        self.client.post(f'/emprestimos/{emprestimo.pk}/devolver/')
        self.assertFalse(Multa.objects.filter(emprestimo=emprestimo).exists())
