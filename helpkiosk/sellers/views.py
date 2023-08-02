from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseForbidden

def is_market_owner(user, market_id):
  return user.is_authenticated and market_id == user.register.pk

@login_required
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
def add_category(request, pk):
  if request.method == 'POST':
    category_id = request.POST['category_id']
    menu_name = request.POST['menu_name']
    menu_price = request.POST['menu_price']

    # market user인 경우에만 메뉴 추가
    market = get_object_or_404(Market, pk=pk)
    if is_market_owner(request.user, pk):
      category = get_object_or_404(MenuCategory, pk=category_id)
      menu = Menu.objects.create(category=category, name=menu_name, price=menu_price)
      return JsonResponse({'menu_id': menu.pk, 'menu_name': menu.name, 'menu_price': menu.price})
    else:
      # 권한이 없는 경우 에러 메시지 반환
      return JsonResponse({'error': '권한이 없습니다.'}, status=403)


@login_required
def menu_create(request, pk):
  if is_market_owner(request.user, pk):
    if request.method == 'POST':
      if 'btn1' in request.POST:
        print(request.POST.get('category'))
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
  

def travel_create(request):
  if request.method == 'POST':
    travel_post = TravelPost.objects.create(
      title=request.POST.get('title'),
      content=request.POST.get('content'),
      nation=request.POST.get('nation'),
      city=request.POST.get('city'),
      together=int(request.POST.get('together')),
      start_date=request.POST.get('start_date'),
      end_date=request.POST.get('end_date'),
      author=request.user
    )
    
    image_files = request.FILES.getlist('image_files')
    for image_file in image_files:
      TravelPhoto.objects.create(travel=travel_post, image=image_file)
    return redirect('travels:travel_list')
  
  return render(request, 'travels/travel_create.html')

# def travel_delete(request, pk):
#   if request.method == "POST":
#     travel = get_object_or_404(TravelPost, pk=pk)
#     travel.delete()
#   return redirect('travels:travel_list')