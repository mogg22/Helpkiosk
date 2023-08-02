from django.db import models
from django.contrib.auth.models import User
from sellers.models import Menu

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    # options = models.ManyToManyField(MenuOption, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.menu.name}'
