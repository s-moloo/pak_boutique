from django import template

register = template.Library()

@register.simple_tag
def sum_cart_total(cart_items):
    total = sum(item.subtotal for item in cart_items)
    return f"{total:.2f}"