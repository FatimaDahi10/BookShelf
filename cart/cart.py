from store.models import Product, Profile


# Carrello
class Cart():
    def __init__(self, request):
        self.session = request.session
        # get request
        self.request = request
        # session key se esiste
        cart = self.session.get('session_key')

        # Nuovo User. creo session key
        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}

        # il carrello deve essere visibile in tutte le pagine
        self.cart = cart

    def database_add(self, product, quantity):
        product_id = str(product)
        product_qty = str(quantity)

        if product_id in self.cart:
            pass
        else:
            # self.cart[product_id] = {'price': str(product.price)}
            # aggiungi al carrello e salva
            self.cart[product_id] = int(product_qty)

        self.session.modified = True

        # logged user
        if self.request.user.is_authenticated:
            # current user profile, lo prendo
            current_user = Profile.objects.get(user__id=self.request.user.id)
            # get rid of quotation mark in the dictionary, from {'3':1} to {"3":1}
            carty = str(self.cart).replace("\'", "\"")

            # aggiorna il carrello e salvalo
            current_user.old_cart = carty
            current_user.save()

    def add(self, product, quantity):
        product_id = str(product.id)
        product_qty = str(quantity)

        # se il prodotto è già salvato
        if product_id in self.cart:
            pass
        else:
            #self.cart[product_id] = {'price': str(product.price)}
            # aggiungi al carrello e salva
            self.cart[product_id] = int(product_qty)

        self.session.modified = True

        # logged user
        if self.request.user.is_authenticated:
            # current user profile
            current_user = Profile.objects.get(user__id=self.request.user.id)
            # get rid of quotation mark in the dictionary, from {'3':1} to {"3":1}
            carty = str(self.cart).replace("\'", "\"")

            # aggiorna carrello e salva
            current_user.old_cart = carty
            current_user.save()

    def cart_total(self):
        # get product ID
        product_ids = self.cart.keys()
        # lookup those keys in our products DB model
        products = Product.objects.filter(id__in=product_ids)
        # quantità
        quantities = self.cart # return dictionary
        # Count
        total = 0
        # {'4':3} -> 4=key, 3=value(qty of books)
        for key, value in quantities.items():
            # convert key to string into int
            key = int(key)
            for product in products:
                if product.id == key:
                    total = total + (product.price * value)
        return total

    # quantità carrello conta
    def __len__(self):
        return len(self.cart)

    # Cart
    def get_products(self):
        # get ids dal Carrello
        product_ids = self.cart.keys()
        # use ids to lookup products in DB model
        products = Product.objects.filter(id__in=product_ids)

        # return looked up products
        return products

    def get_quants(self):
        quantities = self.cart
        return quantities

    def update(self, product, quantity):
        product_id = str(product)
        product_qty = int(quantity)

        # get carrello
        ourcart = self.cart
        # aggiorna dictionary/carrello
        ourcart[product_id] = product_qty

        self.session.modified = True

        # looged user
        if self.request.user.is_authenticated:
            # current user
            current_user = Profile.objects.get(user__id=self.request.user.id)
            # get rid of quotation mark in the dictionary, from {'3':1} to {"3":1}
            carty = str(self.cart).replace("\'", "\"")

            # aggiorna carrello e salva profilo
            current_user.old_cart = carty
            current_user.save()

        thing = self.cart
        return thing

    def delete(self, product):
        # {'4':3} -> product_id=4
        product_id = str(product)
        if product_id in self.cart:
            del self.cart[product_id]

        self.session.modified = True

        # salva il prodotto eliminato nel database
        # logged in user
        if self.request.user.is_authenticated:
            # current user profile
            current_user = Profile.objects.get(user__id=self.request.user.id)
            # get rid of quotation mark in the dictionary, from {'3':1} to {"3":1}
            carty = str(self.cart).replace("\'", "\"")

            # aggiorna il carrello e salva profilo
            current_user.old_cart = carty
            current_user.save()
