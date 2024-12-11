from django.db.models import Count, Avg, Q, F
from django.utils.timezone import now
from datetime import timedelta
from payment.models import OrderItem
from store.models import Product


# raccomanda in bae a acquisti simili o popolarietà
def recommend_books_for_user(user):
    # libri acquistati dall'utente loggato
    user_books = OrderItem.objects.filter(buyer=user).values_list('product', flat=True)

    if user_books.exists():
        # utenti che acquistato gli stessi libri
        similar_users = OrderItem.objects.filter(product__in=user_books).exclude(buyer=user).values_list('buyer',
                                                                                                         flat=True)

        # libri acquistati dagli utenti simili
        recommendations = Product.objects.filter(
            id__in=OrderItem.objects.filter(buyer__in=similar_users).exclude(product__in=user_books).values_list(
                'product', flat=True)
        )

        # Se non ci sono raccomandazioni, passa alla popolarità
        if not recommendations.exists():
            recommendations = Product.objects.annotate(popularity=Count('orderitem')).order_by('-popularity')
    else:
        # popolarità se l'utente non ha acquistato nulla
        recommendations = Product.objects.annotate(popularity=Count('orderitem')).order_by('-popularity')

    return rank_books(recommendations)[:5]


# ranking basato su popolarità e recenti attività
def rank_books(queryset, weight_popularity=0.7, weight_recent=0.3, recent_days=30):
    recent_threshold = now() - timedelta(days=recent_days)
    return queryset.annotate(
        popularity=Count('orderitem'),
        recent_activity=Count('orderitem', filter=Q(orderitem__update_at__gte=recent_threshold)),
        ranking_score=weight_popularity * F('popularity') + weight_recent * F('recent_activity')
    ).order_by('-ranking_score')



# Raccomanda libri basati su contenuto, acquisti e valutazioni.
def recommend_books(product, user=None):

    # Content-Based Filtering
    content_books = Product.objects.filter(
        Q(type=product.type) | Q(author=product.author)
    ).exclude(pk=product.pk)[:5]

    # Collaborative Filtering
    orders_with_product = OrderItem.objects.filter(product=product).values_list('order', flat=True)
    collaborative_books = Product.objects.filter(
        id__in=OrderItem.objects.filter(order__in=orders_with_product).exclude(product=product).values_list('product', flat=True)
    )[:5]

    # Rating-Based Recommendations
    rating_books = Product.objects.annotate(average_rating=Avg('review__rating')).exclude(pk=product.pk).order_by('-average_rating')[:5]

    # Combina e rimuove duplicati
    all_books = list(content_books) + list(collaborative_books) + list(rating_books)
    unique_books = Product.objects.filter(pk__in={book.pk for book in all_books})

    # ranking
    return rank_books(unique_books)[:5]


