from django.contrib import admin
from .models import *

# Register your models here.

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
  pass

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
  pass

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_user', 'total_amount', 'date', 'phone_number', 'cart_items')
    readonly_fields = ('cart_items',)  # Make cart_items field read-only

    def get_user(self, obj):
        return obj.cart.user
    get_user.short_description = 'User'

    def cart_items(self, obj):
        return ", ".join([str(item) for item in obj.cart.cartitem_set.all()])
    cart_items.short_description = 'Cart Items'
