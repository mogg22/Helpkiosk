from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from buyers.models import *
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseForbidden
from django.contrib import messages

def is_market_owner(user, market_id):
  if hasattr(user, 'register'):
    return user.is_authenticated and market_id == user.register.pk
  else:
    return False

def seller_detail(request, pk, *args, **kwargs):
  market = get_object_or_404(Market, pk=pk)
  categories = MenuCategory.objects.filter(market=pk)
  
  if is_market_owner(request.user, pk):
    owner = True
  else:
    owner = False
  
  context = {
    'market': market,
    'categories': categories,
    'owner': owner,
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
    else:
      market = get_object_or_404(Market, pk=pk)
      categories = MenuCategory.objects.filter(market=pk)
      context= {
        'categories': categories,
      }
      return render(request, 'sellers/menu_create.html', context)
  else:
    return HttpResponseForbidden("You don't have permission to perform this action.")

# def category_delete(request, pk):
#   if request.method == "POST":
#     category = get_object_or_404(Category, pk=pk)
#     category.delete()
#   return redirect('sellers:menu_create', pk)

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
        messages.success(request, '상품이 성공적으로 추가되었습니다!')

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