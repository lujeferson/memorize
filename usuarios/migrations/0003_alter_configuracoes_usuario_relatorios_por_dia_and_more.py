# Generated by Django 4.1.3 on 2022-11-15 00:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0002_alter_configuracoes_usuario_tipo_de_relatorio'),
    ]

    operations = [
        migrations.AlterField(
            model_name='configuracoes_usuario',
            name='relatorios_por_dia',
            field=models.CharField(choices=[('1', 'Manhã somente'), ('2', 'Manhã e Tarde'), ('3', 'Manhã, Tarde e Noite')], default=1, help_text='Quantidade de relatórios a receber por dia', max_length=1),
        ),
        migrations.AlterField(
            model_name='configuracoes_usuario',
            name='tipo_de_relatorio',
            field=models.CharField(choices=[('SIMPLES', 'Uma sentença geral'), ('COMPLETO', 'Uma sentença por área')], default='SIMPLES', help_text='Simples, contém apenas uma sentença; Completo, possui uma sentença por área', max_length=8),
        ),
    ]
