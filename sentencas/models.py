from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Autor(models.Model):
    nome = models.CharField(max_length=128, help_text='Autor/Fonte da Sentença')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, editable=False)
    ativo = models.BooleanField(default=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['nome', 'usuario'], name='unique_nome_usuario_autor'),
        ]
        verbose_name_plural = "Autores"

    def __str__(self):
        return self.nome


class Area(models.Model):
    nome = models.CharField(max_length=128, help_text='Área de Conhecimento/Matéria (escolar) da Sentença')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, editable=False)
    ativo = models.BooleanField(default=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['nome', 'usuario'], name='unique_nome_usuario_area'),
        ]

    def __str__(self):
        return self.nome


class Sentenca(models.Model):
    conteudo = models.TextField(max_length=1024, help_text='Conteúdo da Sentença')
    autor = models.ForeignKey(Autor, on_delete=models.CASCADE)
    area = models.ForeignKey(Area, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, editable=False)
    observacoes = models.CharField(max_length=256, help_text='Observações adicionais como página de livro, etc', null=True)
    ativo = models.BooleanField(default=True)
