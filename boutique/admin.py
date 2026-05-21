# boutique/admin.py
from django.contrib import admin
from .models import Women, Men, Kids, Accessory, Cart, CartItem, Favorite 

admin.site.register(Women)
admin.site.register(Men)
admin.site.register(Kids)
admin.site.register(Accessory)

admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Favorite)

