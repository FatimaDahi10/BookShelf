from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from store.models import Product
from .favourite import Favourite


def add_favourite(request):
    favourite = Favourite(request)

    if request.method == "POST":
        product_id = request.POST.get('product_id')
        product = get_object_or_404(Product, id=product_id)

        # Aggiungi
        favourite.add(product)

        messages.success(request, "Prodotto aggiunto nei preferiti")

        response = JsonResponse({'status': 'success'}, status=200)
        return response


def remove_favourite(request):
    favourite = Favourite(request)

    if request.method == "POST":
        product_id = request.POST.get('product_id')
        product = get_object_or_404(Product, id=product_id)

        # rimuovi
        favourite.remove(product)

        response = JsonResponse({'status': 'success'}, status=200)
        messages.success(request, "Prodotto rimosso dai preferiti")
        return response
    return redirect('cart_summary')


def favourite_summary(request):
    # get prodotti preferiti
    favourite = Favourite(request)
    favourite_products = favourite.get_favourites()
    return render(request, "favourite/favourite_summary.html", {"favourite_products": favourite_products})
