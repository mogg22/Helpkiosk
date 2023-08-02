from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
# from django.views.decorators.http import require_POST  # Post로만 접근할 수 있다
from sellers.models import *
from .forms import *
from .models import *
# from .cart import *

@login_required
def add_to_cart(request, menu_id):
    menu = get_object_or_404(Menu, pk=menu_id)

    if request.method == 'POST':
        form = AddMenuFrom(request.POST)
        if form.is_valid():
            quantity = form.cleaned_data['quantity']
            # options = form.cleaned_data['options']

            cart_item, created = Cart.objects.get_or_create(
                user=request.user,
                menu=menu,
                defaults={'quantity': quantity}
            )

            cart_item.quantity += quantity
            cart_item.save()
            # cart_item.options.set(options)
            return redirect('buyers:cart')
    else:
        form = AddMenuFrom()

    context = {
        'menu': menu,
        'form': form,
    }
    return render(request, 'buyers/menu_detail.html', context)

def market_list(request):
    markets = Market.objects.all()
    context = {
        'markets': markets,
    }
    return render(request, 'buyers/market_list.html', context)

def market_detail(request, market_id):
    market = Market.objects.get(pk=market_id)
    categories = MenuCategory.objects.all()

    context = {
        'market': market,
        'categories': categories,
    }

    return render(request, 'buyers/market_detail.html', context)

def menu_list(request, pk):
    market = get_object_or_404(Market, pk=pk)
    menus = market.menu.all()
    context = {
        'market': market,
        'menus': menus,
    }
    return render(request, 'buyers/menu_list.html', context)

def menu_detail(request, menu_id):
    menu = get_object_or_404(Menu, pk=menu_id)

    if request.method == 'POST':
        form = AddMenuFrom(request.POST)
        if form.is_valid():
            quantity = form.cleaned_data['quantity']
            options = form.cleaned_data['options']

            cart_item, created = Cart.objects.get_or_create(
                user=request.user,
                menu=menu,
                defaults={'quantity': quantity}
            )

            cart_item.quantity += quantity
            cart_item.save()
            cart_item.options.set(options)
            return redirect('buyers:cart')
    else:
        form = AddMenuFrom()

    context = {
        'menu': menu,
        'form': form,
    }
    return render(request, 'buyers/menu_detail.html', context)

# def cart(request):
#     cart = Cart(request)
#     return render(request, 'buyers/cart.html', {'cart': cart})
@login_required
def cart(request):
    cart_items = Cart.objects.filter(user=request.user)
    context = {
        'cart_items': cart_items,
    }
    return render(request, 'buyers/cart.html', context)

# def cart_detail(request):
#     cart = Cart(request)
#     cart_items = cart.get_items()

#     return render(request, 'buyers/cart.html', {'cart_items': cart_items})

def update_cart(request, cart_id):
    cart_item = get_object_or_404(Cart, pk=cart_id)

    if request.method == 'POST':
        form = AddMenuFrom(request.POST)
        if form.is_valid():
            quantity = form.cleaned_data['quantity']

            if quantity <= 0:
                cart_item.delete()
            else:
                cart_item.quantity = quantity
                cart_item.save()

            return redirect('buyers:cart')
    else:
        form = AddMenuFrom()

    context = {
        'menu': cart_item.menu,
        'form': form,
    }
    return render(request, 'buyers/menu_detail.html', context)