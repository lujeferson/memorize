from django.db import models
from django.contrib.auth.models import User
import secrets

# Create your models here.
class Configuracoes_Usuario(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, editable=False)

    DESATIVADO = '0'
    MANHA = '1'
    MANHA_TARDE = '2'
    MANHA_TARDE_NOITE = '3'
    RELATORIOS_POR_DIA_CHOICES = [
            (DESATIVADO, 'Não enviar relatório'),
            (MANHA, 'Manhã somente'),
            (MANHA_TARDE, 'Manhã e Tarde'),
            (MANHA_TARDE_NOITE, 'Manhã, Tarde e Noite'),
        ]
    relatorios_por_dia = models.CharField(
        max_length=32,
        blank=False,
        help_text='Quantidade de relatórios a receber por dia',
        default=0,
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

class RecuperadorDeSenha(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, editable=False)
    token =  models.CharField(max_length=128, help_text='Token de recuperação de senha')

    @staticmethod
    def gerar_token():
        """Somente gera o token, não atribui"""
        # https://docs.python.org/3/library/secrets.html
        return secrets.token_urlsafe(64)
