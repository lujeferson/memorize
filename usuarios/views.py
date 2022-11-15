from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth, messages
from .models import Configuracoes_Usuario

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
        messages.success(request, 'Você já está logado')
        return redirect('usuarios:configuracoes')

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


def index(request):
    return redirect('usuarios:configuracoes')


def __campo_vazio(campo):
    return not campo.strip()


def __campos_diferentes(campo, campo2):
    return campo != campo2


def __usuario_nao_logado(request):
    usuario_nao_logado = not request.user.is_authenticated
    if usuario_nao_logado:
        messages.error(request, 'Você precisa se logar no sistema')
    return usuario_nao_logado
