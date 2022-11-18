from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from django.core.mail import send_mail
from sentencas.models import Autor, Area, Sentenca
from usuarios.models import Configuracoes_Usuario

class Command(BaseCommand):
    help = 'Envia os Relatórios de Sentenças dos Usuários'

    def add_arguments(self, parser):
        parser.add_argument('periodo', nargs='+', type=int)

    def handle(self, *args, **options):
        periodo = options['periodo'][0] # Cuidado, options retorna uma lista
        usuarios = User.objects.filter(is_superuser=False)

        for usuario in usuarios:
            config = self.obter_configuracoes(usuario)
            relatorios_por_dia = int(config.relatorios_por_dia)
            recebe = self.recebe_relatorio(usuario, periodo, relatorios_por_dia)

            if not recebe:
                continue

            tipo_de_relatorio = config.tipo_de_relatorio
            if tipo_de_relatorio == 'S':
                sentencas = [Sentenca.get_sentenca_aleatoria(usuario),]
            else:
                sentencas = Sentenca.get_sentencas_aleatorias(usuario)

            texto_email = self.renderiza_texto_email(sentencas)

            subject = 'MEMOR!ZE: Relatório de Sentenças aleatórias'
            message = texto_email
            from_email = 'memorize@memorize.pro.br'
            recipient_list = [usuario.email,]
            send_mail(
                subject=subject,
                message=message,
                from_email=from_email,
                recipient_list=recipient_list,
                fail_silently=False,
            )


    def obter_configuracoes(self, usuario):
        if Configuracoes_Usuario.objects.filter(usuario=usuario).exists():
            config = Configuracoes_Usuario.objects.get(usuario=usuario)
        else:
            config = Configuracoes_Usuario(usuario=usuario)
            config.save()
        return config

    def recebe_relatorio(self, usuario, periodo, relatorios_por_dia):
        recebe = True
        recebe = recebe and relatorios_por_dia >= periodo
        recebe = recebe and Sentenca.objects.filter(usuario=usuario).exists()
        return bool(recebe)

    def renderiza_texto_email(self, sentencas):
        texto = ''
        for sentenca in sentencas:
            texto += f'{sentenca.conteudo}\nAutor: {sentenca.autor.nome}\nÁrea: {sentenca.area.nome}\n\n'
        return texto
