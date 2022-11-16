from django import template
from datetime import datetime

register = template.Library()


@register.simple_tag
def current_time():
    format_string = "%Y-%m-%d"
    return datetime.now().strftime(format_string)