from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter
def animate(value, arg):
    return arg + value * 0.2

@register.filter
# Check if there is already an OrderItem for the MenuItem
def matchingID(items, menuID):
    try:
        item = items.filter(menuItem=menuID).first()
        result = {
                'count': item.count,
                'id': item.id
            }
    except:
        return mark_safe(f'''
              <li class="page-item">
                <button class="remove-order-button page-link font-weight-bold text-dark button-disabled" disabled>-</button>
              </li>
              <li class="page-item disabled"><a class="page-link order-item-count">0</a></li>
            ''')

    return mark_safe(f'''
          <li class="page-item">
            <button class="remove-order-button page-link font-weight-bold text-dark" data-id="{result['id']}">-</button>
          </li>
          <li class="page-item disabled"><a class="page-link order-item-count">{result['count']}</a></li>
        ''')
