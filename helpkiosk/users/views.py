from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from .models import *


# def login(request, *args, **kwargs):
  
def signup(request):
  if request.method == 'POST':
    if not request.POST['username'] or not request.POST['password1'] or not request.POST['password2']:
      error = '모든 값을 입력해주세요.'
      context = {
        'error': error,
      }
      return render(request, 'users/signup.html', context)

    if User.objects.filter(username=request.POST['username']):
      error = '이미 존재하는 아이디입니다.'
      context = {
        'error': error,
      }
      return render(request, 'users/signup.html', context)

    
    elif request.POST['password1'] == request.POST['password2']:
      user = User.objects.create_user(
        username=request.POST['username'],
        password=request.POST['password1'],
      )
      auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')
      return redirect('users:profile_create')

    else:
      error = '정확한 값을 입력해주세요'
      context = {
        'error': error,
      }
      return render(request, 'users/signup.html', context)
  return render(request, 'users/signup.html')

@login_required
def profile_create(request, *args, **kwargs):
  if request.method == 'POST':
    nickname = request.POST.get('nickname')
    number = request.POST.get('number')
    seller = request.POST.get('seller')

    seller = True if seller == 'on' else False

    if nickname and number:
      profile = Profile.objects.create(
        user=request.user,
        nickname=nickname,
        number=number,
        seller=seller
      )
      profile.save()
      return redirect('sellers:seller_list') 
    
    else:
      error = '정보를 모두 입력해주세요.'
      context = {
        'error': error,
      }
      return render(request, 'users/profile_create.html', context)
  return render(request, 'users/profile_create.html')

def login(request, *args, **kwargs):
  if request.method == 'POST':
    username=request.POST['username']
    password=request.POST['password']
    user = authenticate(username=username, password=password)
    if user:
      login(request, user, backend='django.contrib.auth.backends.ModelBackend')
      return redirect('sellers:seller_list')
    else:
      context={'error':'로그인 정보가 맞지 않습니다! 아이디 또는 비밀번호를 확인해주세요',}
      return render(request, 'users/login.html',context)
  return render(request, 'users/login.html')

def logout(request, *args, **kwargs):
  auth.logout(request)
  return redirect('main:main')
