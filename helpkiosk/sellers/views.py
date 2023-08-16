from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseForbidden
from buyers.models import *
from django.db.models import F
from django.contrib import messages

def is_market_owner(user, market_id):
  if hasattr(user, 'register'):
    return user.is_authenticated and market_id == user.register.pk
  else:
    return False

def register(request):
  if request.method == 'POST':
    Register.objects.create(
      user=request.user,
      representative=request.POST.get('representative'),
      name=request.POST.get('name'),
      location=request.POST.get('location'),
      number=request.POST.get('number'),
      business_file=request.FILES.get('business_file'),
      registration_file=request.FILES.get('registration_file'),
      logo=request.FILES.get('img'),
      info_file=request.FILES.get('info_file'),
    )
    return redirect('sellers:seller_list')
  else:
    return render(request, 'sellers/register.html')

def seller_detail(request, pk, *args, **kwargs):
  print('seller_dtail!!!')
  market = get_object_or_404(Market, pk=pk)
  categories = MenuCategory.objects.filter(market=pk)

  cart_list = CartItem.objects.filter(cart__user=request.user)
  # total_price = request.session.get('total_price', 0)

  if is_market_owner(request.user, pk):
    owner = True
  else:
    owner = False
  
  context = {
    'market': market,
    'categories': categories,
    'owner': owner,
    'cart_list': cart_list,
    # 'total_price': total_price
  }
  
  return render(request, 'sellers/seller_detail.html', context)

@login_required
def menu_create(request, pk):
  if is_market_owner(request.user, pk):
    if request.method == 'POST':
      if 'btn1' in request.POST:
        MenuCategory.objects.create(
          market=Market.objects.get(pk=pk),
          category=request.POST.get('category')
        )
        return redirect('sellers:menu_create', pk)
      
      elif 'btn2' in request.POST:
        category_pk = request.POST.get('category')
        Menu.objects.create(
          category = MenuCategory.objects.get(pk=category_pk),
          name=request.POST.get('name'),
          price=request.POST.get('price'),
          img=request.FILES.get('img'),
          exp=request.POST.get('exp')
        )
        return redirect('sellers:seller_detail', pk)
      
      # elif 'btn3' in request.POST:
      #   MenuCategory.objects.create(
      #     menu=Menu.objects.get(pk=pk),
      #     name=request.POST.get('option'),
      #     price=request.POST.get('price'),
      #   )
      #   return redirect('sellers:menu_create', pk)
    else:
      market = get_object_or_404(Market, pk=pk)
      categories = MenuCategory.objects.filter(market=pk)
      context= {
        'market': market,
        'categories': categories,
      }
      return render(request, 'sellers/menu_create.html', context)
  else:
    return HttpResponseForbidden("You don't have permission to perform this action.")

@login_required
def menu_update(request, pk):
  menu = get_object_or_404(Menu, pk=pk)
  market = menu.category.market
  categories = MenuCategory.objects.filter(market=market.pk)
  options = Option.objects.filter(menu=menu)

  if not is_market_owner(request.user, market.pk):
    return HttpResponseForbidden("You don't have permission to perform this action.")

  if request.method == 'POST':
    if 'btn1' in request.POST:
      MenuCategory.objects.create(
        market=Market.objects.get(pk=pk),
        category=request.POST.get('category')
      )
      return redirect('sellers:menu_update', pk)

    elif 'btn2' in request.POST:
      menu.name = request.POST['name']
      menu.price = request.POST['price']
      if request.FILES.get('img'):
        menu.img = request.FILES.get('img')
      menu.exp = request.POST.get('exp')
      menu.save()
      return redirect('sellers:seller_detail', pk)

    elif 'btn3' in request.POST:
      Option.objects.create(
        menu=Menu.objects.get(pk=pk),
        name=request.POST.get('option'),
        price=request.POST.get('option_price'),
      )
      return redirect('sellers:menu_update', pk)

  context= {
    'menu': menu,
    'market': market,
    'categories': categories,
    'options': options,
  }
  return render(request, 'sellers/menu_update.html', context)

# def category_delete(request, pk):
#   if request.method == "POST":
#     category = get_object_or_404(Category, pk=pk)
#     category.delete()
#   return redirect('sellers:menu_create', pk)

# def option_delete(request, pk):
#   if request.method == "POST":
#     option = get_object_or_404(Option, pk=pk)
#     option.delete()
#   return redirect('sellers:menu_update', pk)

def menu_detail(request, pk):
  menu = get_object_or_404(Menu, pk=pk)

  if is_market_owner(request.user, pk):
    owner = True
  else:
    owner = False

  if request.method == 'POST':
    cart, _ = Cart.objects.get_or_create(user=request.user)

    if cart.market != menu.category.market:
      cart.cartitem_set.all().delete()
      cart_item = CartItem.objects.create(cart=cart, menu=menu)
      messages.warning(request, '기존에 있던 다른마켓의 메뉴를 삭제합니다!')
    else:
      if cart.cartitem_set.filter(menu=menu).exists():
        messages.warning(request, '이미 담겨진 상품입니다.')
        cart_item = cart.cartitem_set.get(menu=menu)
        cart_item.quantity += 1
        cart_item.save()
      else:
        cart_item = CartItem.objects.create(cart=cart, menu=menu)
        # messages.success(request, '상품이 성공적으로 추가되었습니다!')

    cart.market = menu.category.market
    cart.save()

  context = {
    'menu': menu,
    'owner': owner,
  }

  return render(request, 'sellers/menu_detail.html', context)


def seller_list(request, *args, **kwargs):
  sellers = Market.objects.all()
  context = {
    'sellers': sellers,
  }
  
  return render(request, 'sellers/seller_list.html', context)

def order_list(request, pk, *args, **kwargs):
  if is_market_owner(request.user, pk):
    market = get_object_or_404(Market, pk=pk)
    payments = Payment.objects.filter(cart__market=market)
    context = {
      'market': market,
      'payments': payments,
    }
    return render(request, 'sellers/order_list.html', context)

  else:
    return HttpResponseForbidden("You don't have permission to perform this action.")

def order_detail(request, pk, *args, **kwargs):
  payment = get_object_or_404(Payment, pk=pk)
  
  # if is_market_owner(request.user, pk):
  #   owner = True
  # else:
  #   owner = False

  context = {
    'payment': payment,
    # 'owner': owner,
  }
  
  return render(request, 'sellers/order_detail.html', context)

def seller_info(request, pk, *args, **kwargs):
  if not is_market_owner(request.user, pk):
    return HttpResponseForbidden("You don't have permission to perform this action.")
  
  market = get_object_or_404(Market, pk=pk)
  
  if request.method == 'POST':
    market.time = request.POST['time']
    market.close = request.POST['close']
    market.save()
    return redirect('sellers:seller_info', pk)
  
  context = {
    'market': market,
  }
  
  return render(request, 'sellers/seller_info.html', context)
  