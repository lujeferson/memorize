from django.urls import path

from . import views

app_name = 'usuarios'
urlpatterns = [
    path('', views.index, name='index'),
    path('cadastro', views.cadastro, name='cadastro'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('configuracoes', views.configuracoes, name='configuracoes'),
    path('configuracoes/definir', views.definir_configuracoes, name='definir_configuracoes'),
    path('senha/redefinir', views.redefinir_senha, name='redefinir_senha'),
    path('senha/recuperar', views.recuperar_senha, name='recuperar_senha'),
    path('senha', views.definir_senha, name='definir_senha'), # necessário encurtar a url, devido a bloqueios de e-mail
    path('excluir_conta', views.excluir_conta, name='excluir_conta'),
]