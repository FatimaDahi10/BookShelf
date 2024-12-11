import datetime
from django.shortcuts import render, redirect
from notifications.models import Notification
from notifications.signals import notify
from cart.cart import Cart
from .forms import ShippingForm, PaymentForm
from .models import ShippingAddress, Order_P, OrderItem
from django.contrib.auth.models import User
from django.contrib import messages
from store.models import Product, Profile


# notifiche lette
def mark_as_read(request, notification_id):
    try:
        notification = Notification.objects.get(id=notification_id)

        # notifiche sue?
        if notification.recipient == request.user:
            notification.unread = False
            notification.save()
    except Notification.DoesNotExist:
        pass

    return redirect('message')


# stato ordine
def message_dash(request):
    if request.user.is_authenticated:
        user = request.user

        # non lette
        unread_notifications = Notification.objects.filter(recipient=user, unread=True)
        unread_notifications.update(unread=False)  # Segna tutte le notifiche non lette come lette

        # ordini buyer/supplier
        orders_buyer = OrderItem.objects.filter(buyer=user).order_by('-update_at')
        orders_supplier = OrderItem.objects.filter(supplier=user).order_by('-update_at')

        if request.method == 'POST':
            order_item_id = request.POST.get('order_item_id')
            shipping_status = request.POST.get('shipping_status')

            try:
                order_item = OrderItem.objects.get(id=order_item_id)

                # update stato spedizione
                if shipping_status == "true":
                    order_item.shipped = True
                else:
                    order_item.shipped = False

                order_item.save()

                # la notifica arriva solo se tutti gli Item sono stati spediti
                order = order_item.order
                order_shipped = all(item.shipped for item in order.order_items.all())

                if order_shipped:
                    # aggiorna l'ordine, item tutti spediti
                    order.shipped = True
                    order.date_shipped = datetime.datetime.now().date()
                    order.save()

                    # messaggio
                    if order_item.buyer:
                        # buyer
                        notify.send(
                            sender=request.user,
                            recipient=order_item.buyer,  # Acquirente
                            verb="Il tuo ordine è stato spedito!",
                            target=order,
                            description=f"Il tuo ordine {order.id} è stato spedito. Grazie per il tuo acquisto!"
                        )


                else:
                    # aggiorna lo stato dell'ordine, non tutti gli item spediti
                    order.shipped = False
                    order.date_shipped = None
                    order.save()

                messages.success(request, "Stato dell'ordine aggiornato!")
            except OrderItem.DoesNotExist:
                messages.error(request, "Ordine non trovato.")

            return redirect('message')

        return render(request, "payment/message.html", {"orders_buyer": orders_buyer, "orders_supplier": orders_supplier, "unread_notifications":unread_notifications})
    else:
        messages.error(request, "Accesso negato!")
        return redirect('home')


# si occupa di tutta la logica del pagamento/notifica
def process_order(request):
    if request.POST:
        # carrello
        cart = Cart(request)
        cart_products = cart.get_products
        quantities = cart.get_quants
        totals = cart.cart_total()

        # billing info
        payment_form = PaymentForm(request.POST or None)
        # shipping Session Data
        my_shipping = request.session.get('my_shipping')
        print("my_shipping:", my_shipping)

        # ORDER_P info
        name_surname = my_shipping['shipping_name_surname']
        email = my_shipping['shipping_email']
        # Create shipping address from session info
        shipping_address = f"{my_shipping['shipping_address']}\n{my_shipping['shipping_city']}\n" \
                           f"{my_shipping['shipping_country']}\n{my_shipping['shipping_zipcode']}"
        amount_paid = totals

        # crea Order_P
        if request.user.is_authenticated:
            # logged in
            user =  request.user
            # create order
            create_order = Order_P(user=user, name_surname=name_surname, email=email, shipping_address=shipping_address,
                                   amount_paid=amount_paid)
            create_order.save()

            # aggiunti OrderItem
            # get ID ordine
            order_id = create_order.pk
            # get prodotto
            for product in cart_products():
                # prodott ID
                product_id = product.id
                # prezzo prodotto
                price = product.price
                # quantità (per fare il totale)
                for (key,value) in quantities().items():
                    if int(key) == product.id:
                        # order item
                        product = Product.objects.get(id=product_id)
                        supplier = product.added_by

                        order_item = OrderItem(order_id=order_id, product_id=product_id, buyer_id=user.id,
                                               supplier_id=supplier.id, quantity=value, price=price)
                        order_item.save()
                        notify.send(
                            sender=request.user,
                            recipient=order_item.supplier,
                            verb="Un ordine è stato spedito!",
                            target=order_item,
                            description=f"L'ordine {order_item.id} che hai fornito è stato spedito."
                        )

                # cancella carrello dopo ordine
                for key in list(request.session.keys()):
                    if key == "session_key":
                        # cancella key
                        del request.session[key]

                # cancella dal DataBase
                current_user = Profile.objects.filter(user__id=request.user.id)
                current_user.update(old_cart="")

            messages.success(request, "Ordine Effettuato")
            return redirect('home')

        # user not logged
        else:
            messages.success(request, "Accedi / Iscriviti")
            return redirect('login')
    else:
        messages.success(request, "Accesso negato")
        return redirect('home')


# checkout carrello con ordini e prodotti
def checkout(request):
    # passa carrello
    cart = Cart(request)
    cart_products = cart.get_products
    quantities = cart.get_quants
    totals = cart.cart_total()

    # LOGGED
    if request.user.is_authenticated:

        shipping_user = ShippingAddress.objects.filter(user=request.user).first()
        shipping_form = ShippingForm(request.POST or None, instance=shipping_user)

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

                return redirect('info_billing')

        return render(request, "payment/checkout.html", {"cart_products": cart_products, "quantities": quantities,
                                                        "totals": totals, "shipping_form": shipping_form})
    else:
        # not LOGGED
        messages.success(request, "Accedi / Iscriviti")
        return redirect('login')


# si occupa del pagamento
def info_billing(request):
    if request.user.is_authenticated:
        # carrello
        cart = Cart(request)
        cart_products = cart.get_products
        quantities = cart.get_quants
        totals = cart.cart_total()

        my_shipping = request.session.get('my_shipping', {})

        billing_form = PaymentForm()

        return render(request, "payment/info_billing.html", {"cart_products": cart_products, "quantities": quantities,
                                       "totals": totals, "info_shipping": my_shipping, "billing_form": billing_form})

    else:
        messages.success(request, "Accesso negato")
        return redirect('home')