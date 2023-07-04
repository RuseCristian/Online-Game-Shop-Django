from django import template

register = template.Library()

@register.filter(name='currency')
def currency(number):
    return "€ "+str(number)



@register.filter(name='multiply')
def multiply(number , number1):
    return number * number1

@register.filter
def is_in_cart(product, cart):
    return product in cart

@register.filter
def cart_quantity(product, cart):
    quantity = 0
    for item in cart:
        if item['product_id'] == product.id:
            quantity = item['quantity']
            break
    return quantity