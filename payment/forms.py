from django import forms
from .models import ShippingAddress


# Form informazioni aggiuntive per l'utente
class ShippingForm(forms.ModelForm):
    shipping_name_surname = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control',
                                                                                'placeholder':'Nome e Cognome'}))
    shipping_phone_number = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control',
                                                                                                'placeholder': 'Telefono'}))
    shipping_email = forms.EmailField(label="", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'
        , 'placeholder':'Email'}), required=True)
    shipping_address = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':
                                                            'form-control', 'placeholder':'Indirizzo'}))
    shipping_city = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control',
                                                                            'placeholder':'Città'}))
    shipping_country = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':
                                                    'form-control', 'placeholder':'Paese'}))
    shipping_zipcode = forms.CharField(label="", max_length=5, widget=forms.TextInput(attrs={'class': 'form-control'
                                                                                , 'placeholder':'Codice Postale'}))
    class Meta:
        model = ShippingAddress
        fields = ['shipping_name_surname', 'shipping_email', 'shipping_address', 'shipping_city', 'shipping_country',
                  'shipping_zipcode', 'shipping_phone_number',
]
        exclude = ['user',]


# informazioni bancarie
class PaymentForm(forms.Form): # we don't save credit card information ILLEGAL :)
    card_name = forms.CharField(label="", max_length=200, widget=forms.TextInput(attrs={'class': 'form-control'
                                                                                , 'placeholder':'Nome titolare'}))
    card_number = forms.CharField(label="", max_length=16, widget=forms.TextInput(attrs={'class': 'form-control'
                                                                                , 'placeholder':'Numero Carta'}))
    card_exp_date = forms.CharField(label="", max_length=5, widget=forms.TextInput(attrs={'class': 'form-control'
                                                                                , 'placeholder':'Data di scadenza'}))
    card_cvv_number = forms.CharField(label="", max_length=5, widget=forms.TextInput(attrs={'class': 'form-control'
                                                                                , 'placeholder':'CVV'}))

