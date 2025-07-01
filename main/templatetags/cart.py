from django import template

register = template.Library()

@register.filter(name='is_in_cart')
def is_in_cart(product  , cart):
    keys = cart.keys()
    for id in keys:
        if int(id) == product.id:
            return True
    return False;


@register.filter(name='cart_quantity')
def cart_quantity(product  , cart):
    keys = cart.keys()
    for id in keys:
        if int(id) == product.id:
            return cart.get(id)
    return 0;


@register.filter(name='total_cart_quantity')
def total_cart_quantity(cart):
    try:
        if cart:
            values = cart.values()
            carttot = 0;
            for i in values:
                carttot += i
            return carttot;
        else:
            carttot = 0;
            return carttot;
    except:
        carttot = 0
        return carttot



@register.filter(name='price_total')
def price_total(product  , cart):

    return product.price * cart_quantity(product , cart)


@register.filter(name='total_cart_price')
def total_cart_price(products , cart):
    if cart:
        sum = 0 ;
        for p in products:
            sum += price_total(p , cart)

        return sum
    else:
        sum = 0
        return sum

