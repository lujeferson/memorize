from django import template
from datetime import datetime
from sentencas.models import Sentenca

register = template.Library()


@register.simple_tag
def current_time():
    format_string = "%Y-%m-%d"
    return datetime.now().strftime(format_string)


@register.inclusion_tag('templatetags/_sentenca_aleatoria.html')
def exibir_sentenca_aleatoria(usuario):
    sentenca_aleatoria = Sentenca.get_sentenca_aleatoria(usuario)
    return {'sentenca_aleatoria': sentenca_aleatoria}
