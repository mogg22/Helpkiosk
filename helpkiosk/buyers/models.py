from django.db import models
from django.contrib.auth.models import User
from sellers.models import *
from django.db.models.signals import post_save
from django.dispatch import receiver
# from phonenumber_field.modelfields import PhoneNumberField

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    market = models.ForeignKey(Market, on_delete=models.CASCADE, null=True, blank=True)
    order = models.BooleanField(default=False) # False 포장, True 매장식사
    
    def cart_total_price(self):
        total_price = sum(item.total_price() for item in self.cartitem_set.all())
        return total_price

@receiver(post_save, sender=User)
def create_user_cart(sender, instance, created, **kwargs):
    if created:
        Cart.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_cart(sender, instance, **kwargs):
    instance.cart.save()

    # def get_total_price(self):
    #     return self.menu.price * self.quantity
    
    def __str__(self):
        return f"Cart for {self.user.username}"
    
    

    # def save(self, *args, **kwargs):
    #     if self.menu:
    #         self.market = self.menu.category.market
            
    #         # # 포장 또는 매장식사 선택에 따라 order 값 결정
    #         # if self.option and self.option.is_dine_in_option():
    #         #     self.order = True
    #         # else:
    #         #     self.order = False
                
    #     super().save(*args, **kwargs)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    options = models.ManyToManyField(Option, blank=True)

    # def total_price(self):
    #     return self.menu.price * self.quantity
    
    def total_price(self):
        option_price = sum(option.price for option in self.options.all())
        total_price = (self.menu.price + option_price) * self.quantity
        return total_price
    
    def __str__(self):
        return f"Item: {self.menu.name} (Qty: {self.quantity})"

class Payment(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, default="")
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
    need = models.TextField(null=True, blank=True)
    payment_method = models.CharField(max_length=100, default="픽업시 결제")
    phone_number = models.CharField(max_length=20, default="010-1234-5678")
    order_type = models.CharField(max_length=10, default="매장식사")

    # def __str__(self):
    #     return f"Payment for Cart {self.cart.id}"
    
# class Payment(models.Model):
#     carts = models.ManyToManyField(Cart)
#     total_amount = models.DecimalField(max_digits=10, decimal_places=2)
#     date = models.DateTimeField(auto_now_add=True)
#     need = models.TextField(null=True, blank=True)
#     payment_method = models.CharField(max_length=100, default="픽업시 결제")
#     phone_number = models.CharField(max_length=20, default="010-1234-5678")

#     def __str__(self):
#         cart_ids = ', '.join(str(cart.id) for cart in self.carts.all())
#         return f"Payment for Carts: {cart_ids}"

class PaymentItem(models.Model):
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default="0")
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    options = models.ManyToManyField(Option, blank=True)