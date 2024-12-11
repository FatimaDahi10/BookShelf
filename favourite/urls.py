from django.urls import path
from . import views

# add, delete, delete from templates

urlpatterns = [
    path('favourite_summary', views.favourite_summary, name="favourite_summary"), # summary page
    path('add/', views.add_favourite, name="add_favourite"),
    path('delete/', views.remove_favourite, name="remove_favourite"),
]

