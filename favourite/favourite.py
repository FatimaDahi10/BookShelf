from store.models import Product, Profile

# Pagina Preferiti
class Favourite:
    def __init__(self, request):
        self.session = request.session
        self.request = request
        # Recupera i preferiti dalla sessione
        favourites = self.session.get('favourites')

        # inizializza una lista vuota, nuovo user
        if 'favourites' not in request.session:
            favourites = self.session['favourites'] = {}

        self.favourites = favourites

    def add(self, product):
        product_id = str(product.id)

        # Aggiungi il prodotto ai preferiti
        if product_id not in self.favourites:
            self.favourites[product_id] = 1

        self.session.modified = True

        # user loggin
        if self.request.user.is_authenticated:
            current_user = Profile.objects.get(user__id=self.request.user.id)
            favourites = str(self.favourites).replace("\'", "\"")  # Rimuove gli apostrofi
            current_user.favourites = favourites  # Salva nel profilo
            current_user.save()

    def remove(self, product):
        product_id = str(product.id)

        # Rimuovi il prodotto dai preferiti
        if product_id in self.favourites:
            del self.favourites[product_id]

        self.session.modified = True

        # loggin user
        if self.request.user.is_authenticated:
            current_user = Profile.objects.get(user__id=self.request.user.id)
            favourites = str(self.favourites).replace("\'", "\"")
            current_user.favourites = favourites  # Salva nel profilo
            current_user.save()

    def get_favourites(self):
        # id favourite
        product_ids = self.favourites.keys()
        # get product in favourite
        products = Product.objects.filter(id__in=product_ids)
        return products

    def __len__(self):
        return len(self.favourites)

    def clear(self):
        # clear
        self.favourites.clear()
        self.session.modified = True

        # Se l'utente è loggato, aggiorna il profilo
        if self.request.user.is_authenticated:
            current_user = Profile.objects.get(user__id=self.request.user.id)
            current_user.favourites = "{}"  # Svuota il campo nel profilo
            current_user.save()
