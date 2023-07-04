from django import template

register = template.Library()

@register.simple_tag
def cart_total(cart):
    total = 0
    for item in cart:
        total += item['quantity']
    return total
