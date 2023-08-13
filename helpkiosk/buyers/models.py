from django.db import models
from django.contrib.auth.models import User
from sellers.models import *
# from phonenumber_field.modelfields import PhoneNumberField

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, null=True)
    option = models.ForeignKey(Option, on_delete=models.CASCADE, null=True, blank=True)
    market = models.ForeignKey(Market, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    order = models.BooleanField(default=False) # False 포장, True 매장식사

    def get_total_price(self):
        return self.menu.price * self.quantity

    def save(self, *args, **kwargs):
        if self.menu:
            self.market = self.menu.category.market
            
            # 선택된 옵션에 따라 매장식사 여부 결정
            if self.option and self.option.is_dine_in_option():
                self.order = True
            else:
                self.order = False
                
        super().save(*args, **kwargs)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def total_price(self):
        return self.menu.price * self.quantity

class Payment(models.Model):
    cart = models.OneToOneField(Cart, on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
    need = models.TextField(null=True, blank=True)
    payment_method = models.CharField(max_length=100, default="픽업시 결제")
    phone_number = models.CharField(max_length=20, default="010-1234-5678")

    def __str__(self):
        return f"Payment for Cart {self.cart.id}"