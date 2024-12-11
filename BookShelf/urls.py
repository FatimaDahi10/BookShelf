from django.contrib import admin
from django.urls import path, include #bc we wnat to include urls that point to our store
from . import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('store.urls')),
    path('cart/', include('cart.urls')),
    path('payment/', include('payment.urls')),
    path('favourite/', include('favourite.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) #allow us to upload immage

