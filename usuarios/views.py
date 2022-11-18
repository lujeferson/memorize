from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth, messages
from django.core.mail import send_mail
from django.urls import reverse
from .models import Configuracoes_Usuario, RecuperadorDeSenha

# Create your views here.
def cadastro(request):
    if request.user.is_authenticated:
        messages.success(request, 'Você já é usuário do sistema')
        return redirect('usuarios:configuracoes')

    if request.method != 'POST':
        return render(request, 'usuarios/cadastro.html')

    nome = request.POST['nome']
    email = request.POST['email']
    senha = request.POST['senha']
    senha2 = request.POST['senha2']

    tem_erro = False
    if not tem_erro and __campo_vazio(nome):
        messages.error(request, 'O nome deve ser informado')
        tem_erro = True
    if not tem_erro and __campo_vazio(email):
        messages.error(request, 'O e-mail deve ser informado')
        tem_erro = True
    if not tem_erro and __campos_diferentes(senha, senha2):
        messages.error(request, 'As senhas não são iguais')
        tem_erro = True
    if not tem_erro and User.objects.filter(email=email).exists():
        messages.error(request, 'Usuário já cadastrado')
        tem_erro = True

    if tem_erro:
        return redirect('usuarios:cadastro')

    user = User.objects.create_user(username=email, first_name=nome, email=email, password=senha)
    user.is_superuser = False
    user.save()
    messages.success(request, 'Usuário cadastrado com sucesso')

    return redirect('usuarios:login')


def login(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method != 'POST':
        return render(request, 'usuarios/login.html')

    email = request.POST['email']
    senha = request.POST['senha']

    if __campo_vazio(email) or __campo_vazio(senha):
        messages.error(request, 'Informe e-mail e senha')
        redirect('usuarios:login')

    if User.objects.filter(email=email).exists():
        user = auth.authenticate(request, username=email, password=senha)
        if user is not None:
            auth.login(request, user)
    return redirect('home')


def logout(request):
    auth.logout(request)
    return redirect('home')


def configuracoes(request):
    if __usuario_nao_logado(request):
        return redirect('usuarios:login')

    usuario = request.user
    try:
        configuracoes = Configuracoes_Usuario.objects.get(usuario=usuario)
    except Configuracoes_Usuario.DoesNotExist:
        configuracoes = Configuracoes_Usuario(usuario=usuario)
        configuracoes.save()
        return redirect('usuarios:configuracoes')

    contexto = {'configuracoes':configuracoes}
    return render(request, 'usuarios/configuracoes.html', contexto)


def definir_configuracoes(request):
    if __usuario_nao_logado(request):
        return redirect('usuarios:login')

    if request.method != 'POST':
        return redirect('usuarios:configuracoes')

    usuario = request.user
    relatorios_por_dia = request.POST['relatorios_por_dia_value']
    tipo_de_relatorio = request.POST['tipo_de_relatorio_value']
    configuracoes = Configuracoes_Usuario.objects.get(usuario=usuario)
    configuracoes.relatorios_por_dia = relatorios_por_dia
    configuracoes.tipo_de_relatorio = tipo_de_relatorio
    configuracoes.save()
    messages.success(request, 'Configurações atualizadas')

    return redirect('usuarios:configuracoes')


def redefinir_senha(request):
    if __usuario_nao_logado(request):
        return redirect('usuarios:login')

    if request.method == 'POST':
        usuario = request.user
        senha = request.POST['senha']

        if not usuario.check_password(senha):
            messages.error(request, 'Senha incorreta')
            return redirect('usuarios:configuracoes')

        senha_nova = request.POST['senha_nova']
        senha_nova2 = request.POST['senha_nova2']
        if __campo_vazio(senha) or __campo_vazio(senha_nova) or __campo_vazio(senha_nova2):
            messages.error(request, 'Preencha os campos de senha')
            return redirect('usuarios:configuracoes')
        
        if senha_nova != senha_nova2:
            messages.error(request, 'Senhas novas não conferem')
            return redirect('usuarios:configuracoes')

        usuario.set_password(senha_nova)
        usuario.save()
        messages.success(request, 'Senha alterada com sucesso')

    return redirect('usuarios:configuracoes')


def recuperar_senha(request):
    if request.method == 'POST':
        email = request.POST['email']

        try:
            usuario = User.objects.get(email=email)
        except User.DoesNotExist:
            usuario = None

        recuperador = None
        if usuario:
            try:
                recuperador = RecuperadorDeSenha.objects.get(usuario=usuario)
            except RecuperadorDeSenha.DoesNotExist:
                token = RecuperadorDeSenha.gerar_token()
                recuperador = RecuperadorDeSenha(usuario=usuario, token=token)
                recuperador.save()

        if recuperador:
            query_string = '?r=' + recuperador.token  # r -> reset
            url_reset = reverse('usuarios:definir_senha') + query_string
            subject = 'MEMOR!ZE: Reset de senha'
            message = recuperador.token
            from_email = 'memorize@memorize.pro.br'
            recipient_list = [usuario.email,]
            html_message = f'Para recuperar sua senha, <a href=http://127.0.0.1:8000{url_reset}>clique aqui</a>'
            send_mail(
                subject=subject,
                message=message,
                from_email=from_email,
                recipient_list=recipient_list,
                fail_silently=False,
                html_message=html_message,
            )

    messages.success(request, 'Solicitação concluída com sucesso')
    return redirect('usuarios:login')


def definir_senha(request):
    if not __usuario_nao_logado(request):
        return redirect('usuarios:login')

    if request.method == 'GET':
        token = request.GET['r']
        contexto = {'token':token}
        return render(request, 'usuarios/definir_senha.html', contexto)

    if request.method == 'POST':
        token = request.POST['token']
        senha = request.POST['senha_nova']
        senha2 = request.POST['senha_nova2']

        try:
            recuperador = RecuperadorDeSenha.objects.get(token=token)
            usuario = recuperador.usuario
            if senha == senha2:
                usuario.set_password(senha)
                usuario.save()
                recuperador.delete()
                messages.success(request, 'Senha alterada com sucesso')
        except RecuperadorDeSenha.DoesNotExist:
            print('Redirecionar para o get. Mas, como?')

    return redirect('usuarios:login')


def excluir_conta(request):
    if __usuario_nao_logado(request):
        return redirect('usuarios:login')

    if request.method == 'POST':
        senha = request.POST['senha']
        usuario = request.user
        if usuario.check_password(senha):
            messages.success(request, 'Conta e dados associados excluídos com sucesso')
            usuario.delete()
            return redirect('usuarios:login')
        else: 
            messages.error(request, 'Falha na exclusão da conta, senha incorreta')
    
        return redirect('usuarios:configuracoes')


def index(request):
    return redirect('usuarios:configuracoes')


def __campo_vazio(campo):
    return not campo.strip()


def __campos_diferentes(campo, campo2):
    return campo != campo2


def __usuario_nao_logado(request):
    usuario_nao_logado = not request.user.is_authenticated
    return usuario_nao_logado


def __ignorar_mensagens_anteriores(request):
    for message in messages.get_messages(request):
        pass
