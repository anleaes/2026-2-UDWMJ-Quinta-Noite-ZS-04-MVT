"""Model da classe Leitor."""
from django.db import models


class Leitor(models.Model):
    ALUNO = 'aluno'
    PROFESSOR = 'professor'
    COMUNIDADE = 'comunidade'

    TIPOS = [
        (ALUNO, 'Aluno'),
        (PROFESSOR, 'Professor'),
        (COMUNIDADE, 'Comunidade'),
    ]

    nome = models.CharField('nome', max_length=150)
    cpf = models.CharField('CPF', max_length=14, unique=True)
    email = models.EmailField('e-mail')
    telefone = models.CharField('telefone', max_length=20)
    tipo = models.CharField('tipo', max_length=15, choices=TIPOS, default=ALUNO)
    foto = models.ImageField('foto', upload_to='leitores/', blank=True, null=True)
    ativo = models.BooleanField('ativo', default=True)
    data_cadastro = models.DateTimeField('data de cadastro', auto_now_add=True)

    class Meta:
        ordering = ['nome']
        verbose_name = 'leitor'
        verbose_name_plural = 'leitores'

    def __str__(self):
        return self.nome

    def limite_emprestimos(self):
        """Quantidade máxima de empréstimos simultâneos, conforme o tipo."""
        limites = {self.ALUNO: 3, self.COMUNIDADE: 2, self.PROFESSOR: 5}
        return limites.get(self.tipo, 0)

    def possui_multa_pendente(self):
        """Indica se o leitor tem alguma multa não paga (via emprestimo__leitor)."""
        from multas.models import Multa

        return Multa.objects.filter(emprestimo__leitor=self, paga=False).exists()
