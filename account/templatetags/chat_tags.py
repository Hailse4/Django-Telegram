from django import template

register = template.Library()

@register.simple_tag
def get_time(value):
    time = value[:4]
    return time