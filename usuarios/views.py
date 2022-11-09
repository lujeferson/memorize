from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth, messages

# Create your views here.
def cadastro(request):
    if request.user.is_authenticated:
        messages.success(request, 'Você já é usuário do sistema')
        return redirect('usuarios:dados')

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
        return redirect('usuarios:dados')

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


def dados(request):
    if request.user.is_authenticated:
        return render(request, 'usuarios/dados.html')
    return render(request, 'usuarios/nao_logado.html')


def index(request):
    return redirect('usuarios:dados')


def __campo_vazio(campo):
    return not campo.strip()


def __campos_diferentes(campo, campo2):
    return campo != campo2