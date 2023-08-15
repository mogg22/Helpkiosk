from django.urls import path
from .views import *

app_name = "users"

urlpatterns = [
  path('signup/', signup, name='signup'),
  path('profile_create/', profile_create, name='profile_create'),
  path("login/", log_in, name="login"),
  path("logout/", logout, name="logout"),
  path("mypage/", mypage, name="mypage"),
]