from django.urls import path
from .views import *

app_name = "sellers"

urlpatterns = [
  # path('', sellers_list, name='sellers_list'),
  path('<int:pk>/', seller_detail, name='seller_detail'),
  path('<int:pk>/menu_create/', menu_create, name='menu_create'),
  path('menu_update/<int:pk>/', menu_update, name='menu_update'),
  path('register/', register, name='register'),
  path('menu_detail/<int:pk>/', menu_detail, name='menu_detail'),
  path('seller_list/', seller_list, name='seller_list'),
  # path('add_category/<int:pk>/', add_category, name='add_category'),
]