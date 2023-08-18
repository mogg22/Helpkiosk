from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from .models import *
from sellers.models import *
from buyers.models import *


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
      return redirect('users:start_page') 
    
    else:
      error = '정보를 모두 입력해주세요.'
      context = {
        'error': error,
      }
      return render(request, 'users/profile_create.html', context)
  return render(request, 'users/profile_create.html')

def log_in(request, *args, **kwargs):
  if request.method == 'POST':
    username=request.POST['username']
    password=request.POST['password']
    user = authenticate(username=username, password=password)
    if user:
      login(request, user, backend='django.contrib.auth.backends.ModelBackend')
      return redirect('users:start_page')
    else:
      context={'error':'로그인 정보가 맞지 않습니다! \n 아이디 또는 비밀번호를 확인해주세요',}
      return render(request, 'users/login.html',context)
  return render(request, 'users/login.html')

def logout(request, *args, **kwargs):
  auth.logout(request)
  return redirect('users:start_page')

@login_required
def mypage(request, *args, **kwargs):
  user = request.user
  if user.profile.seller:
    # 판매자일 경우
    register = Register.objects.get(user=request.user)
    market = get_object_or_404(Market, register=register)
    context = {
      'user': user,
      'register': register,
      'market': market,
    }
    return render(request, 'users/mypage.html', context)
  else:
    try:
      lapay = Payment.objects.filter(cart__user=request.user).latest('date')
      lapay_items = lapay.paymentitem_set.all()
      itemstitle = ''
      
      for idx, item in enumerate(lapay_items):
        itemstitle += item.menu.name
        
        if idx < len(lapay_items) - 1:
          itemstitle += ', '
      
      payments = Payment.objects.filter(cart__user=request.user)
      payment_items = PaymentItem.objects.filter(payment__in=payments).select_related('menu')
  
      payment_item_dict = {}  # 각 Payment에 대한 PaymentItem을 담을 딕셔너리
      for payment_item in payment_items:
        if payment_item.payment_id not in payment_item_dict:
          payment_item_dict[payment_item.payment_id] = payment_item
    except Payment.DoesNotExist:
      payments = None
      lapay = None
      itemstitle = ''
      payment_item_dict = None
      
    context = {
      'itemstitle': itemstitle,
      'user': user,
      'paymentitems': payment_item_dict,
      'payments': payments,
      'lapay': lapay,
    }

    return render(request, 'users/mypage.html', context)

def start_page(request):
  return render(request, 'users/startpage.html')