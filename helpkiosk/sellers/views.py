from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseForbidden

def is_market_owner(user, market_id):
  return user.is_authenticated and market_id == user.register.pk

@login_required
def seller_detail(request, pk, *args, **kwargs):
  market = get_object_or_404(Market, pk=pk)
  categories = market.categories.all()
  
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
def add_category(request, pk):
  market = get_object_or_404(Market, pk=pk)
  
  if is_market_owner(request.user, pk):
    owner = True
  else:
    return HttpResponseForbidden("You don't have permission to perform this action.")

  
    # 소유주인지 확인
    if market.register.user != request.user:
        return HttpResponseForbidden("You don't have permission to perform this action.")
    
    if request.method == 'POST':
        form = MenuCategoryForm(request.POST)
        if form.is_valid():
            category = form.save()
            market.categories.add(category)
            return redirect('sellers:market_detail', market_id=market_id)
    else:
        form = MenuCategoryForm()
    
    context = {
        'form': form,
    }
    return render(request, 'add_category.html', context)

@login_required
def add_menu(request, market_id):
    market = get_object_or_404(Market, pk=market_id)
    # 소유주인지 확인
    if market.register.user != request.user:
        return HttpResponseForbidden("You don't have permission to perform this action.")
    
    if request.method == 'POST':
        form = MenuForm(request.POST, request.FILES)
        if form.is_valid():
            menu = form.save(commit=False)
            menu.category = form.cleaned_data['category']
            menu.save()
            return redirect('sellers:market_detail', market_id=market_id)
    else:
        form = MenuForm()
    
    context = {
        'form': form,
    }
    return render(request, 'add_menu.html', context)