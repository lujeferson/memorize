from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Configuracoes_Usuario(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, editable=False)

    MANHA = '1'
    MANHA_TARDE = '2'
    MANHA_TARDE_NOITE = '3'
    RELATORIOS_POR_DIA_CHOICES = [
            (MANHA, 'Manhã somente'),
            (MANHA_TARDE, 'Manhã e Tarde'),
            (MANHA_TARDE_NOITE, 'Manhã, Tarde e Noite'),
        ]
    relatorios_por_dia = models.CharField(
        max_length=32,
        blank=False,
        help_text='Quantidade de relatórios a receber por dia',
        default=1,
        choices=RELATORIOS_POR_DIA_CHOICES
    )

    SIMPLES = 'S'
    COMPLETO = 'C'
    TIPO_DE_RELATORIO_CHOICES = [
            (SIMPLES, 'Simples: Uma sentença geral'),
            (COMPLETO, 'Completo: Uma sentença por área'),
        ]
    tipo_de_relatorio = models.CharField(
        max_length=32,
        blank=False,
        help_text='Simples, contém apenas uma sentença; Completo, possui uma sentença por área',
        default=SIMPLES,
        choices=TIPO_DE_RELATORIO_CHOICES
    )
