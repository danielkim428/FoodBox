from django import template

register = template.Library()

@register.filter
def animate(value, arg):
    return arg + value * 0.2
