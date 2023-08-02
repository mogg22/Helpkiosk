from django.urls import path
from .views import *

app_name = "buyers"

urlpatterns = [
    # path('', detail, name='detail'),
    path('add/<int:menu_id>/', add_to_cart, name='add_to_cart'),
    # path('remove/<menu_id>/', remove, name='menu_remove'),
    path('market_list/', market_list, name='market_list'),
    path('market/<int:market_id>/', market_detail, name='market_detail'),
    path('menu_list/<int:pk>/', menu_list, name='menu_list'),
    path('menu_detail/<int:menu_id>/', menu_detail, name='menu_detail'),
    path('cart/', cart, name='cart'),
    path('update_cart/<int:cart_id>/', update_cart, name='update_cart'),
]