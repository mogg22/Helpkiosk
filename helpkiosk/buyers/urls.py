from django.urls import path
from .views import *

app_name = "buyers"

urlpatterns = [
    # path('', detail, name='detail'),
    # path('add/<int:menu_id>/<int:market_id>/', add_to_cart, name='add_to_cart'),
    path('add/<int:pk>/', add_cart, name='add_to_cart'),
    # path('remove/<menu_id>/', remove, name='menu_remove'),
    path('cart/', cart, name='cart'),
    path('cart/item-quan/<int:item_id>/', item_ajax, name='item_ajax'),
    path('update_cart/<int:cart_id>/', update_cart, name='update_cart'),
    path('delete_cart_item/<int:cart_id>/', delete_cart_item, name='delete_cart_item'),
    path('clear_cart/', clear_cart, name='clear_cart'),
    path('payment/', payment, name='payment'),
    path('buyer_mypage/', buyer_mypage, name='buyer_mypage'),
    # path('set_dining_option/', set_dining_option, name='set_dining_option'),
]