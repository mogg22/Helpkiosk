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
  pass