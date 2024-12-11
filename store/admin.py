from django.contrib import admin
from .models import Category, Product, Review, Profile, Review_Supplier
from django.contrib.auth.models import User

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Review)
admin.site.register(Profile)
admin.site.register(Review_Supplier)



# Mix profile info and user info
class ProfileInline(admin.StackedInline):
    model = Profile


# Extend User Model
class UserAdmin(admin.ModelAdmin):
    model = User
    field = ["username", "first_name", "last_name", "email"]
    inlines = [ProfileInline]


admin.site.unregister(User)
admin.site.register(User, UserAdmin)


