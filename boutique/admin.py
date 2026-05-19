# boutique/admin.py
from django.contrib import admin
from .models import Cart, CartItem, Favorite 

admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Favorite)

