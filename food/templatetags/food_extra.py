from django import template

register = template.Library()

@register.filter
def animate(value, arg):
    return arg + value * 0.2

@register.filter
def matchingID(items, menuID):
    try:
        item = items.filter(menuItem=menuID).first()
        result = item.count
    except:
        result = 0
        
    return result
