from django.urls import path

from . import views

app_name = 'sentencas'
urlpatterns = [
    path('', views.index, name='index'),
    path('sentencas', views.sentencas, name='sentencas'),
    path('sentenca/criar', views.criar_sentenca, name='criar_sentenca'),
    path('sentenca/<int:sentenca_id>/editar', views.editar_sentenca, name='editar_sentenca'),
    path('sentenca/atualizar', views.atualizar_sentenca, name='atualizar_sentenca'),
    path('sentenca/<int:sentenca_id>/excluir', views.excluir_sentenca, name='excluir_sentenca'),

    path('autores', views.autores, name='autores'),
    path('autor/criar', views.criar_autor, name='criar_autor'),
    path('autor/<int:autor_id>/editar', views.editar_autor, name='editar_autor'),
    path('autor/atualizar', views.atualizar_autor, name='atualizar_autor'),
    path('autor/<int:autor_id>/excluir', views.excluir_autor, name='excluir_autor'),

    path('areas', views.areas, name='areas'),
    path('area/criar', views.criar_area, name='criar_area'),
    path('area/<int:area_id>/editar', views.editar_area, name='editar_area'),
    path('area/atualizar', views.atualizar_area, name='atualizar_area'),
    path('area/<int:area_id>/excluir', views.excluir_area, name='excluir_area'),
]