from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.

class Profile(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  nickname = models.CharField(max_length=20)
  number = PhoneNumberField(region='KR')
  seller = models.BooleanField(default=False) # 판매자/구매자
