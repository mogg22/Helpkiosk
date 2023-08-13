from django.db import models
from django.contrib.auth.models import User
from sellers.models import *
from phonenumber_field.modelfields import PhoneNumberField

# class Cart(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
#     # options = models.ManyToManyField(MenuOption, blank=True)
#     quantity = models.PositiveIntegerField(default=1)
#     date_added = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f'{self.user.username} - {self.menu.name}'


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    market = models.ForeignKey(Market, on_delete=models.CASCADE, null=True, blank=True)
    order = models.BooleanField(default=False) # False 포장, True 배달
    

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
    # 결제 수단 필드