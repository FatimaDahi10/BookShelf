from datetime import timezone
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import models
from django.db.models import Avg, Count
from django.contrib.auth.models import User
from django.db.models.signals import post_save


# Customer Profile
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_modified = models.DateTimeField(User, auto_now=True)
    phone = models.CharField(max_length=20, blank=True)
    address = models.CharField(max_length=200, blank=True)
    # not saving python dictionary in the DB, instead convert dictionary in string (using JSON)
    old_cart = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.user.username


# Create user profile by default, create a profile automatically
def create_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = Profile(user=instance)
        user_profile.save()


# automate the profile
post_save.connect(create_profile, sender=User)


# Categoria per Prodotti
class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'categories'


class Type(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


# Prodotti
class Product(models.Model):
    TYPE_CHOICES = (
        ("book", "Libri"),
        ("children_teenagers", "Bambini e Ragazzi"),
        ("manga_comics", "Manga"),
        ("vintage_book", "Libri Vintage"),
        ("ebook_audiobook", "eBook e Audiolibri"),
    )

    # Foreign Key
    added_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="added_products")

    name = models.CharField(max_length=100)
    author = models.CharField(max_length=100, default='')
    price = models.DecimalField(default=0, decimal_places=2, max_digits=6)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    type = models.CharField(max_length=50, choices=TYPE_CHOICES)
    description = models.CharField(max_length=1000, default='', blank=True, null=True)
    image = models.ImageField(upload_to='product/')
    created_at = models.DateTimeField(auto_now_add=True)


    def averagereview(self):
        review = Review.objects.filter(product=self).aggregate(avarage=Avg('rating'))
        avg = 0
        if review["avarage"] is not None:
            avg = float(review["avarage"])
        return avg

    def countreview(self):
        reviews = Review.objects.filter(product=self).aggregate(count=Count('id'))
        cnt = 0
        if reviews["count"] is not None:
            cnt = int(reviews["count"])
        return cnt

    def __str__(self):
        return str(self.name)  #!!!! CAMBIATOOO


class Review(LoginRequiredMixin, models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='supplier_reviews')
    review = models.TextField(max_length=500, blank=True)
    rating = models.FloatField()
    ip = models.CharField(max_length=20, blank=True)
    status = models.BooleanField(default=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product.name


class Review_Supplier(LoginRequiredMixin, models.Model):
    supplier = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ratings')
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ratings_given')
    rating = models.FloatField()
    review = models.TextField(blank=True, null=True)
    ip = models.CharField(max_length=20, blank=True)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['supplier', 'buyer']  # Un utente può votare solo una volta per fornitore

    def __str__(self):
        return f"{self.buyer.username} rated {self.supplier.username} {self.rating} stars"







