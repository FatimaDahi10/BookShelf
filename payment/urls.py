from django.urls import path
from . import views

urlpatterns = [
    path('checkout/', views.checkout, name='checkout'),
    path('info_billing/', views.info_billing, name='info_billing'),
    path('process_order/', views.process_order, name='process_order'),
    path('message/', views.message_dash, name='message'),
    path('notifications/mark_as_read/<int:notification_id>/', views.mark_as_read, name='notification_mark_as_read'),

]
