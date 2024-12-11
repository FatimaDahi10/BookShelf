from django.urls import path
from . import views

# add, delete, delete from templates

urlpatterns = [
    path('cart_summary', views.cart_summary, name="cart_summary"), # summary page
    path('add/', views.cart_add, name="cart_add"),
    path('delete/', views.cart_delete, name="cart_delete"),
    path('update/', views.cart_update, name="cart_update"),
]

