from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
from django import forms
from django.contrib.auth.models import User
from store.models import Review, Product, Category


# registrazione acquirente
class SignUpFormBuyer(UserCreationForm):
    email = forms.EmailField(label="",
                             widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'}))
    first_name = forms.CharField(label="", max_length=50,
                                 widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}))
    last_name = forms.CharField(label="", max_length=50,
                                widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(SignUpFormBuyer, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'User Name'
        self.fields['username'].label = ''
        # mi dice come deve essere il nome username
        self.fields['username'].help_text = '<span class="form-text text-muted"><small>Required. ' \
                                            '150 characters or fewer. Letters, digits and @/./+/-/_ only.' \
                                            '</small></span>'

        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password1'].label = ''
        # come deve essere la password
        self.fields['password1'].help_text = '<ul class="form-text text-muted small"><li>' \
                                             'Your password can\'t be too similar to your other personal information.' \
                                             '</li><li>Your password must contain at least 8 characters.' \
                                             '</li><li>Your password can\'t be a commonly used password.' \
                                             '</li><li>Your password can\'t be entirely numeric.</li></ul>'

        # quando devi riscrivere la password, per controllare la correttezza
        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
        self.fields['password2'].label = ''
        self.fields['password2'].help_text = '<span class="form-text text-muted"><small>' \
                                             'Enter the same password as before, for verification.</small></span>'

    def save(self, commit=True):
        user = super().save(commit)
        g = Group.objects.get(name="Buyer")
        g.user_set.add(user)
        return user


# fornitore
class SignUpFormSupplier(UserCreationForm):
    email = forms.EmailField(label="",
                             widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'}))
    first_name = forms.CharField(label="", max_length=50,
                                 widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}))
    last_name = forms.CharField(label="", max_length=50,
                                widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(SignUpFormSupplier, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'User Name'
        self.fields['username'].label = ''
        # mi dice come deve essere il nome username
        self.fields['username'].help_text = '<span class="form-text text-muted"><small>Required. ' \
                                            '150 characters or fewer. Letters, digits and @/./+/-/_ only.' \
                                            '</small></span>'

        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password1'].label = ''
        # come deve essere la password
        self.fields['password1'].help_text = '<ul class="form-text text-muted small"><li>' \
                                             'Your password can\'t be too similar to your other personal information.' \
                                             '</li><li>Your password must contain at least 8 characters.' \
                                             '</li><li>Your password can\'t be a commonly used password.' \
                                             '</li><li>Your password can\'t be entirely numeric.</li></ul>'

        # quando devi riscrivere la password, per controllare la correttezza
        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
        self.fields['password2'].label = ''
        self.fields['password2'].help_text = '<span class="form-text text-muted"><small>' \
                                             'Enter the same password as before, for verification.</small></span>'

    def save(self, commit=True):
        user = super().save(commit)
        g = Group.objects.get(name="Supplier")
        g.user_set.add(user)
        return user


# sia review prodotti che review fornitori
class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['review', 'rating']


class ProductForm(forms.ModelForm):
    name = forms.CharField(label="Name", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    author = forms.CharField(label="Author", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    price = forms.DecimalField(label="Price", decimal_places=2, max_digits=6,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    description = forms.CharField(label="Description", max_length=1000,
                                  widget=forms.Textarea(attrs={'class': 'form-control'}))
    category = forms.ModelChoiceField(queryset=Category.objects.all(), label='Category', required=False,
                                      widget=forms.Select(attrs={'class': 'form-control'}))

    TYPE_CHOICES = (
        ("book", "Libri"),
        ("children_teenagers", "Bambini e Ragazzi"),
        ("manga_comics", "Manga"),
        ("vintage_book", "Libri Vintage"),
        ("ebook_audiobook", "eBook e Audiolibri"),
    )

    type = forms.ChoiceField(choices=TYPE_CHOICES, label='Type',
                             widget=forms.Select(attrs={'class': 'form-control'}))

    new_category = forms.CharField(label='New Category', required=False,
                                   widget=forms.TextInput(attrs={'class': 'form-control'}))

    image = forms.ImageField(label="product", widget=forms.ClearableFileInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Product
        fields = ['name', 'author', 'price', 'description', 'category', 'type', 'new_category', 'image']

    def clean(self):
        cleaned_data = super().clean()
        category = cleaned_data.get('category')
        new_category = cleaned_data.get('new_category')

        if not category and not new_category:
            raise forms.ValidationError("Please select an existing category or enter a new one.")

        return cleaned_data

    def save(self, commit=True):
        product = super().save(commit=False)
        new_category_name = self.cleaned_data.get('new_category')

        if new_category_name:
            new_category = Category.objects.create(name=new_category_name)
            product.category = new_category

        product.type = self.cleaned_data.get('type')

        if commit:
            product.save()

        return product
