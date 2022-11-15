# Generated by Django 4.1.3 on 2022-11-15 00:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0003_alter_configuracoes_usuario_relatorios_por_dia_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='configuracoes_usuario',
            name='relatorios_por_dia',
            field=models.CharField(choices=[(1, 'Manhã somente'), (2, 'Manhã e Tarde'), (3, 'Manhã, Tarde e Noite')], default=1, help_text='Quantidade de relatórios a receber por dia', max_length=1),
        ),
    ]
