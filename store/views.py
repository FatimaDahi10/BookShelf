from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from payment.models import ShippingAddress, Order_P
from .forms import ReviewForm, ProductForm, SignUpFormBuyer, SignUpFormSupplier
from .models import Product, Category, Review, Profile, Review_Supplier
from django.db.models import Q, Avg  # CONCATENARE RICERA
from django.views import View
from braces.views import GroupRequiredMixin
import json
from cart.cart import Cart
from payment.forms import ShippingForm
from .reccomandation import recommend_books, recommend_books_for_user


@login_required()
def supplier_profile(request, supplier_id):
    # id supplier
    supplier = get_object_or_404(User, id=supplier_id)
    # recupera profilo supplier
    profile = Profile.objects.filter(user=supplier).first()
    # product supplier
    products = Product.objects.filter(added_by=supplier)

    # URL per reindirizzare dopo l'operazione
    url = request.META.get('HTTP_REFERER')

    if request.method == "POST":
        # verifica se l'utente ha già lasciato una recensione per questo fornitore

        try:
            reviews = Review_Supplier.objects.get(buyer=request.user, supplier_id=supplier_id)
            form = ReviewForm(request.POST, instance=reviews)
            form.save()
            messages.success(request, "Grazie! La tua valutazione è stata aggiornata.")
            return redirect(url)
        except Review_Supplier.DoesNotExist:
            # nuova recensione
            form = ReviewForm(request.POST)
            if form.is_valid():
                data = Review_Supplier()
                data.rating = form.cleaned_data['rating']
                data.review = form.cleaned_data['review']
                data.ip = request.META.get('REMOTE_ADDR')
                data.supplier = supplier
                data.buyer = request.user
                data.save()
                messages.success(request, "Grazie! La tua valutazione è pubblicata")
                return redirect(url)

    reviews = Review_Supplier.objects.filter(supplier=supplier, status=True)

    return render(request, "supplier_profile.html", {'supplier': supplier, 'profile': profile, 'products': products,
                                                     'reviews':reviews,})


@login_required()
# aggiorna profilo pagamento
def profile(request):
    shipping_user = ShippingAddress.objects.filter(user=request.user).first()
    shipping_form = ShippingForm(request.POST or None, instance=shipping_user)

    # recupera i prodotti se l'utente è un supplier
    products = Product.objects.filter(added_by=request.user)

    if request.method == 'POST':
        if shipping_form.is_valid():
            shipping = shipping_form.save(commit=False)
            shipping.user = request.user
            shipping.save()

            request.session['my_shipping'] = {
                'shipping_name_surname': shipping.shipping_name_surname,
                'shipping_email': shipping.shipping_email,
                'shipping_address': shipping.shipping_address,
                'shipping_city': shipping.shipping_city,
                'shipping_zipcode': shipping.shipping_zipcode,
                'shipping_country': shipping.shipping_country,
                'shipping_phone_number': shipping.shipping_phone_number,
            }
            messages.success(request, "Dati aggiornati con successo!")
            return redirect('profile')
        else:
            messages.error(request, "Whoops, qualcosa è andato storto.. Riprova")
            for field, errors in shipping_form.errors.items():
                for error in errors:
                    messages.error(request, f"Errore in {field}: {error}")
            return redirect('profile')

    return render(request, "profile.html", {"shipping_form": shipping_form, "products": products  # mostra prodotti se è supplier
    })


def home(request):
    # per carousol
    books = Product.objects.annotate(average_rating=Avg('review__rating')).order_by('-average_rating')[:5]

    # paginator (12 libri per pagina)
    products = Product.objects.all()


    # raccomandazioni basate sugli acquisti dell'utente corrente
    recommended_books = None
    if request.user.is_authenticated:
        recommended_books = recommend_books_for_user(request.user)

    # menu tendina ordine
    sort_option = request.GET.get('sort', 'recent')

    # ordinamento in base:
    if sort_option == 'recent':
        products = Product.objects.all().order_by('-created_at')
        paginator = Paginator(products, 12)
        page_number = request.GET.get('page', 1)
        books_home = paginator.get_page(page_number)

    elif sort_option == 'top_rated':
        products = Product.objects.annotate(average_rating=Avg('review__rating')).order_by('-average_rating')
        paginator = Paginator(products, 12)
        page_number = request.GET.get('page', 1)
        books_home = paginator.get_page(page_number)

    elif sort_option == 'price_low':
        products = Product.objects.all().order_by('price')
        paginator = Paginator(products, 12)
        page_number = request.GET.get('page', 1)
        books_home = paginator.get_page(page_number)

    elif sort_option == 'price_high':
        products = Product.objects.all().order_by('-price')
        paginator = Paginator(products, 12)
        page_number = request.GET.get('page', 1)
        books_home = paginator.get_page(page_number)

    else:
        paginator = Paginator(products, 12)
        page_number = request.GET.get('page', 1)
        books_home = paginator.get_page(page_number)

    return render(request, 'home.html', {'products': products, 'books': books, 'recommended_books': recommended_books,
                                         'books_home': books_home})


# pagina prodotto
def product(request, pk):
    user = request.user

    product = Product.objects.get(id=pk)
    reviews = Review.objects.filter(product_id=product.id, status=True)

    recommended_books = recommend_books(product, user)

    return render(request, 'product.html', {'product': product, 'reviews': reviews, 'recommended_books': recommended_books})


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)

            # carrello
            current_user = Profile.objects.get(user__id=request.user.id)
            # get saved cart from DB
            saved_cart = current_user.old_cart
            # convert DB string to python dictionary
            if saved_cart:
                # convert to dictionary (JSON)
                converted_cart = json.loads(saved_cart)
                # add loaded cart dictionary to session
                cart = Cart(request)
                # loop cart and add items from DB
                for key,value in converted_cart.items():
                    cart.database_add(product=key, quantity=value)


            messages.success(request, "Accesso effettuato con successo!")
            return redirect('home')
        else:
            messages.error(request, "Si è verificato un errore. Username o password non corrette. Riprova! ")

            return redirect('login')
    else:
        return render(request, 'login.html', {})


def logout_user(request):
    logout(request)
    messages.success(request, " Sei stato disconnesso con successo!")
    return redirect('home')


def register(request):
    if request.method == 'POST':
        return redirect('register')
    else:
        return render(request, 'register.html', {})


def register_buyer(request):
    form = SignUpFormBuyer()
    if request.method == "POST":
        form = SignUpFormBuyer(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            if User.objects.filter(username=username).exists():
                messages.error(request, "Il nome utente è già stato preso. Prova un altro.")
                return render(request, 'register_buyer.html', {'form': form})

            # Procedi con la creazione dell'utente e login
            form.save()
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "Registrazione avvenuta con successo!")
            return redirect('home')
        else:
            messages.error(request, "Si è verificato un problema con la registrazione. Per favore riprova..")
            return render(request, 'register_buyer.html', {'form': form})

    else:
        return render(request, 'register_buyer.html', {'form': form})


def register_supplier(request):
    form = SignUpFormSupplier()
    if request.method == "POST":
        form = SignUpFormSupplier(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "Registrazione avvenuta con successo!")
            return redirect('home')
        else:
            messages.error(request, "Si è verificato un problema con la registrazione. Per favore riprova..")
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"Error in {field}: {error}")
            return redirect('register_supplier')
    else:
        return render(request, 'register_supplier.html', {'form': form})


def search(request):
    searched = request.POST.get('searched', '').strip() if request.method == 'POST' else ''
    filter_option = request.POST.get('filter', '') if request.method == 'POST' else ''

    # prodotti
    results = Product.objects.all()

    # Filtra termine cercato
    if searched:
        if filter_option == 'category':
            results = results.filter(category__name__icontains=searched)
        else:
            results = results.filter(Q(name__icontains=searched) | Q(author__icontains=searched))

    # GET per categoria e tipo dalla navbar
    category_id = request.GET.get('category')
    type_value = request.GET.get('type')

    # filtra
    if category_id:
        results = results.filter(category_id=category_id)
    if type_value:
        results = results.filter(type=type_value)

    # ordinamento in base a scelta
    if filter_option == 'price_asc':
        results = results.order_by('price')
    elif filter_option == 'price_desc':
        results = results.order_by('-price')
    elif filter_option == 'reviews':
        results = results.annotate(average_rating=Avg('review__rating')).order_by('-average_rating')

    categories = Category.objects.all()

    return render(request, 'search.html', {'results': results, 'searched': searched, 'filter_option': filter_option,
        'selected_category': category_id, 'selected_type': type_value, 'categories': categories})


@login_required()
def submit_review(request, product_id):
    url = request.META.get('HTTP_REFERER')
    if request.method == "POST":
        try:
            # esiste?
            reviews = Review.objects.get(user__id=request.user.id, product__id=product_id)
            form = ReviewForm(request.POST, instance=reviews)
            form.save()
            messages.success(request, "Grazie! La tua valutazione è stata aggiornata.")
            return redirect(url)
        # non esiste
        except Review.DoesNotExist:
            form = ReviewForm(request.POST)
            if form.is_valid():
                data = Review()
                data.rating = form.cleaned_data['rating']
                data.review = form.cleaned_data['review']
                data.ip = request.META.get('REMOTE_ADDR')
                data.product_id = product_id
                data.user_id = request.user.id
                data.save()
                messages.success(request, "Grazie! La tua valutazione è pubblicata")
                return redirect(url)
            else:
                 messages.error(request, "Whoops.. Si è verificato un problema. Per favore riprova..")
                 for field, errors in form.errors.items():
                     for error in errors:
                         messages.error(request, f"Error in {field}: {error}")
                 return redirect(url)


class add_product_view(GroupRequiredMixin, View):
    group_required = ["Supplier"]

    def get(self, request):
        return render(request, 'add_product.html', {'form': ProductForm()})

    def post(self, request):
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.added_by = request.user
            product.save()

            messages.success(request, 'Grazie! Il tuo prodotto è stato aggiunto')
            return redirect('home')
        else:
            messages.error(request, "Whoops.. Si è verificato un problema. Per favore riprova..")
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"Error in {field}: {error}")
            return render(request, 'add_product.html', {'form': form})


def about(request):
    return render(request, 'about.html', {})


