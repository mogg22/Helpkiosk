from django.urls import path
from .views import *

app_name = "sellers"

urlpatterns = [
  # path('', sellers_list, name='sellers_list'),
  path('<int:pk>/', seller_detail, name='seller_detail'),
  path('<int:pk>/menu_create/', menu_create, name='menu_create'),
  path('add_category/<int:pk>/', add_category, name='add_category'),
]