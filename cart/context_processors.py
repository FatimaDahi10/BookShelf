from .cart import Cart

# crea context processors cosiché il carrello è visisibile in tutte le schede
def cart(request):
    # return default data from our Cart
    return {'cart': Cart(request)}