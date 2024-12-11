from django.urls import path, include
from . import views
from .views import add_product_view

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register, name='register'),
    path('register/register_buyer/', views.register_buyer, name='register_buyer'),
    path('register/register_supplier/', views.register_supplier, name='register_supplier'),
    path('product/<int:pk>/', views.product, name='product'),
    path('search/', views.search, name='search'),
    path('submit_review/<int:product_id>/', views.submit_review, name='submit_review'),
    path('add_product/', add_product_view.as_view(), name='add_product'),
    path('about/', views.about, name='about'),
    path('profile/', views.profile, name='profile'),
    path('supplier/<int:supplier_id>', views.supplier_profile, name='supplier_profile'),

]
#int:pk --> crea un url con number of product

