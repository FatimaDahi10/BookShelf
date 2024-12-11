from .favourite import Favourite

# create context processors così i favoriti funzionino in tutte le pagine
def favourite(request):
    # return default data from our Cart
    return {'favourite': Favourite(request)}