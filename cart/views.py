from django.shortcuts import render, get_object_or_404, redirect
from .cart import Cart
from store.models import Product
from django.http import JsonResponse
from django.contrib import messages



def cart_summary(request):
    # Carrello
    cart = Cart(request)
    cart_products = cart.get_products
    quantities = cart.get_quants
    totals = cart.cart_total()
    return render(request, "cart/cart_summary.html", {"cart_products":cart_products, "quantities":quantities,
                                                      "totals":totals})


def cart_add(request):
    # get Carrello
    cart = Cart(request)
    # test for POST
    if request.POST.get('action') == 'post':
        # get product
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))
        # look up product in database
        product = get_object_or_404(Product, id=product_id)

        # salva sessione
        cart.add(product=product, quantity=product_qty)

        # get cart quantity
        cart_quantity = cart.__len__()

        # return una risposta, a dictionary
        response = JsonResponse({'qty': cart_quantity})

        messages.success(request, "Prodotto aggiunto nel carrello")
        return response


def cart_delete(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        # get prodotti
        product_id = int(request.POST.get('product_id'))

        cart.delete(product=product_id)

        response = JsonResponse({'product':product_id})
        messages.success(request, "Prodotto rimosso dal carrello")
        return response
    return redirect('cart_summary')


def cart_update(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        # get prodotti
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))

        cart.update(product=product_id, quantity=product_qty)

        response = JsonResponse({'qty':product_qty})
        messages.success(request, "Quantità prodotto aggiornata")
        return response
    return redirect('cart_summary')

