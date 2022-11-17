from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import auth, messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Autor, Area, Sentenca


# Create your views here.
# INÍCIO: Sentenças -----------------------------------------------------------
def sentencas(request):
    if __usuario_nao_logado(request):
        return redirect('usuarios:login')

    sentencas = Sentenca.objects.filter(ativo=True, usuario=request.user).order_by('id')

    if not sentencas:
        messages.success(request, 'Crie sua primeira Sentença')
        return redirect('sentencas:criar_sentenca')

    paginator = Paginator(sentencas, 10)
    page = request.GET.get('page')
    sentencas_por_pagina = paginator.get_page(page)

    contexto = {'sentencas': sentencas_por_pagina}
    return render(request, 'sentencas/sentencas.html', contexto)


def criar_sentenca(request):
    if __usuario_nao_logado(request):
        return redirect('usuarios:login')

    if request.method != 'POST':
        autores = Autor.objects.filter(ativo=True, usuario=request.user).order_by('nome')
        if not autores:
            __ignorar_mensagens_anteriores(request)
            messages.success(request, 'Crie seu primeiro Autor')
            return redirect('sentencas:criar_autor')

        areas = Area.objects.filter(ativo=True, usuario=request.user).order_by('nome')
        if not areas:
            __ignorar_mensagens_anteriores(request)
            messages.success(request, 'Crie sua primeira Área de Conhecimento')
            return redirect('sentencas:criar_area')

        contexto = {'autores': autores, 'areas':areas}
        return render(request, 'sentencas/criar_sentenca.html', contexto)

    conteudo = request.POST['conteudo'].strip()
    autor = get_object_or_404(Autor, pk=request.POST['autor_id'])
    area = get_object_or_404(Area, pk=request.POST['area_id'])
    observacoes = request.POST['observacoes'].strip()
    usuario = request.user

    if not conteudo:
        messages.error(request, 'A sentença deve possuir conteúdo')
        return redirect('sentencas:criar_sentenca')

    sentenca = Sentenca(conteudo=conteudo, autor=autor, area=area, observacoes=observacoes, usuario=usuario, ativo=True)
    sentenca.save()
    messages.success(request, 'Sentença criada com sucesso')

    return redirect('sentencas:sentencas')


def editar_sentenca(request, sentenca_id):
    if __usuario_nao_logado(request):
        return redirect('usuarios:login')

    usuario = request.user
    try:
        sentenca = Sentenca.objects.get(pk=sentenca_id, usuario=usuario, ativo=True)
    except Sentenca.DoesNotExist:
        messages.error(request, 'Estas são as suas sentenças')
        return redirect('sentencas:sentencas')

    autores = Autor.objects.filter(ativo=True, usuario=request.user).order_by('nome')
    areas = Area.objects.filter(ativo=True, usuario=request.user).order_by('nome')

    contexto = {'autores': autores, 'areas': areas, 'sentenca': sentenca}
    return render(request, 'sentencas/editar_sentenca.html', contexto)


def atualizar_sentenca(request):
    if __usuario_nao_logado(request):
        return redirect('usuarios:login')

    if request.method != 'POST':
        return redirect('sentencas:sentencas')

    sentenca_id = request.POST['sentenca_id']
    usuario = request.user

    try:
        sentenca = Sentenca.objects.get(pk=sentenca_id, usuario=usuario, ativo=True)
    except Sentenca.DoesNotExist:
        messages.error(request, 'Estas são as suas sentenças')
        return redirect('sentencas:sentencas')

    conteudo = request.POST['conteudo'].strip()
    if not conteudo:
        messages.error(request, 'A sentença deve possuir conteúdo')
        return redirect('sentencas:sentencas')

    autor = get_object_or_404(Autor, pk=request.POST['autor_id'])
    area = get_object_or_404(Area, pk=request.POST['area_id'])
    observacoes = request.POST['observacoes'].strip()

    sentenca.conteudo = conteudo
    sentenca.autor = autor
    sentenca.area = area
    sentenca.observacoes = observacoes
    sentenca.save()
    messages.success(request, 'Sentença atualizada com sucesso')

    return redirect('sentencas:sentencas')


def excluir_sentenca(request, sentenca_id):
    if __usuario_nao_logado(request):
        return redirect('usuarios:login')

    try:
        usuario = request.user
        sentenca = Sentenca.objects.get(pk=sentenca_id, usuario=usuario, ativo=True)
    except Sentenca.DoesNotExist:
        messages.error(request, 'Estas são as suas sentenças')
        return redirect('sentencas:sentencas')

    sentenca.delete()
    return redirect('sentencas:sentencas')
# FIM: Sentenças --------------------------------------------------------------


# INÍCIO: Autores -------------------------------------------------------------
def autores(request):
    if __usuario_nao_logado(request):
        return redirect('usuarios:login')

    autores = Autor.objects.filter(ativo=True, usuario=request.user).order_by('nome')

    if not autores:
        messages.success(request, 'Crie seu primeiro Autor')
        return redirect('sentencas:criar_autor')

    paginator = Paginator(autores, 10)
    page = request.GET.get('page')
    autores_por_pagina = paginator.get_page(page)

    contexto = {'autores': autores_por_pagina}
    return render(request, 'sentencas/autores.html', contexto)


def criar_autor(request):
    if __usuario_nao_logado(request):
        return redirect('usuarios:login')

    if request.method != 'POST':
        return render(request, 'sentencas/criar_autor.html')

    usuario = request.user
    nome = request.POST['nome'].strip()

    if not nome:
        messages.error(request, 'Informe o nome do Autor')
        return redirect('sentencas:criar_autor')

    if not Autor.objects.filter(nome=nome, usuario=usuario).exists():
        autor = Autor(nome=nome, usuario=usuario)
        autor.save()
        messages.success(request, 'Autor criado com sucesso')
    else:
        messages.error(request, 'Autor já cadastrado')

    return redirect('sentencas:autores')


def editar_autor(request, autor_id):
    if __usuario_nao_logado(request):
        return redirect('usuarios:login')

    usuario = request.user
    try:
        autor = Autor.objects.get(pk=autor_id, usuario=usuario, ativo=True)
    except Autor.DoesNotExist:
        messages.error(request, 'Estes são os seus autores')
        return redirect('sentencas:autores')

    contexto = {'autor': autor}
    return render(request, 'sentencas/editar_autor.html', contexto)


def atualizar_autor(request):
    if __usuario_nao_logado(request):
        return redirect('usuarios:login')

    if request.method != 'POST':
        return redirect('sentencas:autores')

    autor_id = request.POST['autor_id']
    usuario = request.user
    try:
        autor = Autor.objects.get(pk=autor_id, usuario=usuario, ativo=True)
    except Autor.DoesNotExist:
        messages.error(request, 'Estes são os seus autores')
        return redirect('sentencas:autores')

    nome = request.POST['nome'].strip()
    if nome:
        autor.nome = nome
    autor.save()
    messages.success(request, 'Autor atualizado com sucesso')

    return redirect('sentencas:autores')


def excluir_autor(request, autor_id):
    if __usuario_nao_logado(request):
        return redirect('usuarios:login')

    usuario = request.user
    try:
        autor = Autor.objects.get(pk=autor_id, usuario=usuario, ativo=True)
    except Autor.DoesNotExist:
        messages.error(request, 'Estes são os seus autores')
        return redirect('sentencas:autores')

    autor.delete()
    return redirect('sentencas:autores')
# FIM: Autores ----------------------------------------------------------------


# INÍCIO: Áreas do Conhecimento -----------------------------------------------
def areas(request):
    if __usuario_nao_logado(request):
        return redirect('usuarios:login')

    areas = Area.objects.filter(ativo=True, usuario=request.user).order_by('nome')

    if not areas:
        messages.success(request, 'Crie sua primeira Área de Conhecimento')
        return redirect('sentencas:criar_area')

    paginator = Paginator(areas, 10)
    page = request.GET.get('page')
    areas_por_pagina = paginator.get_page(page)

    contexto = {'areas': areas_por_pagina}
    return render(request, 'sentencas/areas.html', contexto)


def criar_area(request):
    if __usuario_nao_logado(request):
        return redirect('usuarios:login')

    if request.method != 'POST':
        return render(request, 'sentencas/criar_area.html')

    usuario = request.user
    nome = request.POST['nome'].strip()

    if not nome:
        messages.error(request, 'Informe o nome da Área de Conhecimento')
        return redirect('sentencas:criar_area')

    if not Area.objects.filter(nome=nome, usuario=usuario).exists():
        area = Area(nome=nome, usuario=usuario)
        area.save()
        messages.success(request, 'Área de Conhecimento criada com sucesso')
    else:
        messages.error(request, 'Área de Conhecimento já cadastrada')

    return redirect('sentencas:areas')


def editar_area(request, area_id):
    if __usuario_nao_logado(request):
        return redirect('usuarios:login')

    usuario = request.user
    try:
        area = Area.objects.get(pk=area_id, usuario=usuario, ativo=True)
    except Area.DoesNotExist:
        messages.error(request, 'Estas são as suas áreas')
        return redirect('sentencas:areas')

    contexto = {'area': area}
    return render(request, 'sentencas/editar_area.html', contexto)


def atualizar_area(request):
    if __usuario_nao_logado(request):
        return redirect('usuarios:login')

    if request.method != 'POST':
        return redirect('sentencas:areas')

    area_id = request.POST['area_id']
    usuario = request.user
    try:
        area = Area.objects.get(pk=area_id, usuario=usuario, ativo=True)
    except Area.DoesNotExist:
        messages.error(request, 'Estas são as suas áreas')
        return redirect('sentencas:areas')

    nome = request.POST['nome'].strip()
    if nome:
        area.nome = nome
    area.save()
    messages.success(request, 'Área de Conhecimento atualizada com sucesso')

    return redirect('sentencas:areas')


def excluir_area(request, area_id):
    if __usuario_nao_logado(request):
        return redirect('usuarios:login')

    usuario = request.user
    try:
        area = Area.objects.get(pk=area_id, usuario=usuario, ativo=True)
    except Area.DoesNotExist:
        messages.error(request, 'Estas são as suas áreas')
        return redirect('sentencas:areas')

    area.delete()
    return redirect('sentencas:areas')
# FIM: Áreas do Conhecimento --------------------------------------------------

def index(request):
    return redirect('sentencas:sentencas')


# def get_sentenca_aleatoria(usuario, area=None):
#     if area:
#         sentenca = Sentenca.objects.filter(usuario=usuario, area=area).order_by("?").first()
#     else:
#         sentenca = Sentenca.objects.filter(usuario=usuario).order_by("?").first()
#     return sentenca


# def get_sentencas_aleatorias(usuario):
#     areas_id_list = Sentenca.objects.filter(usuario=usuario).distinct('area').values_list('area', flat=True)

#     sentencas = []
#     for area in areas_id_list:
#         sentenca = get_sentenca_aleatoria(usuario=usuario, area=area)
#         sentencas.append(sentenca)

#     return sentencas


def __usuario_nao_logado(request):
    usuario_nao_logado = not request.user.is_authenticated
    return usuario_nao_logado


def __ignorar_mensagens_anteriores(request):
    for message in messages.get_messages(request):
        pass