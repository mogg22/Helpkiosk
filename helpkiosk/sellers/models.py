from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField
from django.urls import reverse
import qrcode
from django.core.files import File
from io import BytesIO
from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys


class Register(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  representative = models.CharField(max_length=30)
  name = models.CharField(max_length=50)
  location = models.CharField(max_length=50)
  number = PhoneNumberField(region='KR')
  business_file = models.FileField(upload_to='business/')
  registration_file = models.FileField(upload_to='registration/')
  logo = models.ImageField(upload_to='logo/')
  info_file = models.FileField(upload_to='info/')
  public = models.BooleanField(default=True) # 등록 완료 여부
  
  def save(self, *args, **kwargs):
    super().save(*args, **kwargs)
    
    if self.public:
      market = Market.objects.create(register=self)
      market.save()

class Market(models.Model):
  register = models.OneToOneField(Register, on_delete=models.CASCADE, null=True, blank=True)
  qr = models.ImageField(upload_to='qrcode/', blank=True, null=True)
  order = models.BooleanField(default=False) # True면 매장도 가능
  time = models.TextField(default='연중무휴')
  start = models.BooleanField(default=True) # 매장 열었는지
  close = models.TextField(null=True, blank=True)
  
  def save(self, *args, **kwargs):
    if self.pk:      
      url = reverse('sellers:seller_detail', args=[str(self.pk)])
      
      qrc = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
      )
      
      qrc.add_data(url)
      img = qrc.make_image()
      
      # QR 코드를 파일로 저장
      buffer = BytesIO()
      img.save(buffer, format='PNG')
      
      file_name = f'qrcode-{self.pk}.png'  
      image_file = InMemoryUploadedFile(buffer, None, file_name, 'image/png', sys.getsizeof(buffer), None)

      # 이미지 파일을 qr 필드에 저장
      self.qr.save(file_name, image_file, save=False)
    
    super().save(*args, **kwargs)

class MenuCategory(models.Model):
  market = models.ForeignKey(Market, on_delete=models.CASCADE)
  category = models.CharField(max_length=15)

class Menu(models.Model):
  category = models.ForeignKey(MenuCategory, on_delete=models.CASCADE)
  name = models.CharField(max_length=50)
  price = models.DecimalField(max_digits=8, decimal_places=0, default=0)
  img = models.ImageField(upload_to='menu_img/', null=True, blank=True)
  exp = models.TextField()

class Option(models.Model):
  menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
  name = models.CharField(max_length=50)
  price = models.DecimalField(max_digits=8, decimal_places=0, default=0)