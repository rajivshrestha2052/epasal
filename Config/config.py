from main.models import Products as product


class cart_totalprice:

    def cart_totalprice(self,product, cart ):
        return product.price * cart_quantity(product , cart)