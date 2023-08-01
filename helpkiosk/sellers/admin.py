from django.contrib import admin
from .models import *

# Register your models here.

@admin.register(Register)
class RegisterAdmin(admin.ModelAdmin):
  pass

@admin.register(Market)
class MarketAdmin(admin.ModelAdmin):
  pass

@admin.register(MenuCategory)
class MenuCategoryAdmin(admin.ModelAdmin):
  pass

@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
  pass