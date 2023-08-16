from django.shortcuts import render, redirect, get_object_or_404
from datetime import datetime
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
# from django.views.decorators.http import require_POST  # Post로만 접근할 수 있다
from sellers.models import *
from sellers.views import *
from .forms import *
from .models import *
from buyers.models import *
from django.urls import reverse
from django.contrib import messages
from django.db.models import Sum


# @login_required
# def add_to_cart(request, menu_id, market_id):
#     menu = get_object_or_404(Menu, pk=menu_id)

#     if request.method == 'POST':
#         form = AddMenuForm(request.POST)
#         if form.is_valid():

#             quantity = form.cleaned_data['quantity']
#             dine_in_option = request.POST.get('dine_in_option')  # 선택한 주문 옵션 가져오기(매장식사/포장)
#             options = form.cleaned_data
            
#             # 기존에 있는 카트 아이템인지 확인
#             cart_item, created = Cart.objects.get_or_create(user=request.user, menu=menu, defaults={'quantity':quantity})

#             if not created:
#                 cart_item.quantity += quantity
#                 cart_item.save()
                
#             # 매장식사 또는 포장 여부 확인
#             # dine_in_option = request.POST.get('dine_in_option')
#             if dine_in_option == 'dine_in':
#                 cart_item.order = True
#             else:
#                 cart_item.order = False
#             cart_item.save()
            
#             # messages.success(request, '상품이 성공적으로 추가되었습니다!')
#             # else:
#             #     cart_item = Cart.objects.create(user=request.user, menu=menu, quantity=quantity)
#             return redirect('sellers:seller_detail', market_id)
#             # seller_detail_url = reverse('sellers:seller_detail', kwargs={'market_id': market_id})
#             # return redirect(seller_detail_url)

#     else:
#         form = AddMenuForm()

#     context = {
#         'menu': menu,
#         'form': form,
#         'market_id': market_id
#     }
#     return render(request, 'buyers/menu_detail.html', context)

@login_required
def add_cart(request, pk):
    menu = get_object_or_404(Menu, pk=pk)

    if is_market_owner(request.user, pk):
        owner = True
    else:
        owner = False

    if request.method == 'POST':
        cart, _ = Cart.objects.get_or_create(user=request.user)
        quantity = request.POST.get('quantity')

        if cart.market != menu.category.market:
            cart.cartitem_set.all().delete()
            cart_item = CartItem.objects.create(cart=cart, menu=menu, quantity=int(quantity))
            # messages.warning(request, '기존에 있던 다른마켓의 메뉴를 삭제합니다!')
        else:
            if cart.cartitem_set.filter(menu=menu).exists():
                # messages.warning(request, '이미 담겨진 상품입니다.')
                cart_item = cart.cartitem_set.get(menu=menu)
                cart_item.quantity += int(quantity)
                cart_item.save()
            else:
                cart_item = CartItem.objects.create(cart=cart, menu=menu, quantity=int(quantity))
                # messages.success(request, '상품이 성공적으로 추가되었습니다!')

        selected_options = request.POST.getlist('options')  # 선택된 Option들을 받아옴
        cart_item.options.add(*selected_options) 
        cart_item.save()
        
        cart.market = menu.category.market
        cart.save()

        return redirect('sellers:seller_detail', cart.market.pk)

    context = {
        'menu': menu,
        'owner': owner,
    }

    return render(request, 'buyers/menu_detail.html', context)

# def menu_detail(request, pk):
#     menu = get_object_or_404(Menu, pk=pk)

#     if is_market_owner(request.user, pk):
#         owner = True
#     else:
#         owner = False

#     if request.method == 'POST':
#         form = AddMenuForm(request.POST)

#         if form.is_valid():
#             quantity = form.cleaned_data['quantity']
#             options = form.cleaned_data['options']
#             dine_in_option = form.cleaned_data['dine_in_option']  # 매장식사 또는 포장 여부


#             cart_item, created = Cart.objects.get_or_create(
#                 user=request.user,
#                 menu=menu,
#                 defaults={'quantity': quantity}
#             )

#             cart_item.quantity += quantity
#             cart_item.save()
#             cart_item.options.set(options)

#             cart = cart_item.cart
#             if cart.market != menu.category.market:
#                 cart_item.delete()
#                 messages.warning(request, '기존에 있던 다른마켓의 메뉴를 삭제합니다!')
#             else:
#                 if cart.cartitem_set.filter(menu=menu).exists():
#                     messages.warning(request, '이미 담겨진 상품입니다.')
#                 else:
#                     messages.success(request, '상품이 성공적으로 추가되었습니다!')

#             cart.market = menu.category.market
#             cart.save()
#             return redirect('buyers:cart')
#     else:
#         form = AddMenuForm()

#     options = Option.objects.filter(menu=menu)
#     print(options)
#     context = {
#         'menu': menu,
#         'owner': owner,
#         'form': form,
#         'options': options
#     }

#     return render(request, 'buyers/menu_detail.html', context)

# def menu_detail(request, menu_id):
#     menu = get_object_or_404(Menu, pk=menu_id)

#     if request.method == 'POST':
#         form = AddMenuForm(request.POST)
#         if form.is_valid():
#             quantity = form.cleaned_data['quantity']
#             options = form.cleaned_data['options']

#             cart_item, created = Cart.objects.get_or_create(
#                 user=request.user,
#                 menu=menu,
#                 defaults={'quantity': quantity}
#             )

#             cart_item.quantity += quantity
#             cart_item.save()
#             cart_item.options.set(options)
#             return redirect('buyers:cart')
#     else:
#         form = AddMenuForm()

#     context = {
#         'menu': menu,
#         'form': form,
#     }
#     return render(request, 'buyers/menu_detail.html', context)

# def cart(request):
#     cart = Cart(request)
#     return render(request, 'buyers/cart.html', {'cart': cart})


@login_required
def cart(request):
    cart_items = CartItem.objects.filter(cart__user=request.user)

    total_price = 0

    for data in cart_items:
        if data.menu:
            data.total_price = data.menu.price * data.quantity
            total_price += data.total_price

    # request.session['total_price'] = total_price

    context = {
        'cart_items': cart_items,
        'total_price': total_price
    }
    return render(request, 'buyers/cart.html', context)

@csrf_exempt
def item_ajax(request, item_id, *args, **kwargs):
    data = json.loads(request.body)
    item = CartItem.objects.get(pk=item_id)

    quan = data.get('quanType')
    
    if quan == "plus":
        item.quantity += 1
        # item.total_price 
    elif quan == "minus":
        if item.quantity > 1:
            item.quantity -= 1

    item.save()

    context = {
        'id' : item_id,
        'item' : item.quantity,
    }
    
    return JsonResponse(context)

def update_cart(request, cart_id):
    
    if request.method == 'POST':
        
        quantity = request.POST.get("item_" + str(cart_id)) 
        #quantity = form.cleaned_data['quantity']   
        cart_item = get_object_or_404(Cart, pk=cart_id)
        cart_item.quantity = quantity
        cart_item.save()    

        return redirect('buyers:cart')
        
# def update_cart(request, cart_id):
#     if request.method == 'POST':
#         try:
#             quantity = int(request.POST.get(f"item_{cart_id}"))
#             if quantity > 0:
#                 cart_item = get_object_or_404(Cart, pk=cart_id)
#                 cart_item.quantity = quantity
#                 cart_item.save()

#                 updated_item = {
#                     'id': cart_id,
#                     'quantity': quantity,
#                     'total_price': cart_item.total_price,
#                 }
#                 return JsonResponse(updated_item)
#             else:
#                 return HttpResponseBadRequest("Quantity must be greater than 0.")
#         except Exception as e:
#             return HttpResponseBadRequest(str(e))

@login_required
def delete_cart_item(request, cart_id):
    cart_item = get_object_or_404(Cart, pk=cart_id)

    if cart_item.user != request.user:
        return redirect('buyers:cart')

    # if request.method == 'POST':
    cart_item.delete()

    return redirect('buyers:cart')

# 일괄 삭제
# @login_required
# def clear_cart(request):
#     cart = get_object_or_404(Cart, user=request.user)
#     cart_items = CartItem.objects.filter(cart=cart)
#     cart_items.delete()
    
#     seller_detail_url = reverse('sellers:seller_detail', kwargs={'pk': request.user.pk})

#     return redirect(seller_detail_url)
@login_required
def clear_cart(request):
    market_id = request.POST.get('market_id', '1')
    cart_items = Cart.objects.filter(user=request.user)
    print(f"Total cart items to delete: {cart_items.count()}")  # 디버깅 메시지

    if cart_items.exists():
        cart_items.delete()
        print("카트 다 삭제 완")  # 디버깅 메시지
    else:
        print("삭제할 카트 아이템이 없다")  # 디버깅 메시지

    return redirect('sellers:seller_detail', pk=market_id)

# @login_required
# def order_list(request):
#     user_payments = Payment.objects.filter(cart__user=request.user)
#     return render(request, 'buyers/payment.html', {'user_payments':user_payments})


@login_required
def payment(request):
    if request.method == 'POST':
        total_amount = int(request.POST.get('total_price'))
        phone_number = request.POST.get('phone_number', '')
        items = request.POST.getlist('items[]')
        request_text = request.POST.get('request_text')

        item_info_list = []
        for item in items:
            item_name, item_quantity, item_price = item.split('|')
            item_info = {
                'name': item_name,
            }
            item_info_list.append(item_info)

        user_cart = Cart.objects.filter(user=request.user).first()
        payment = None

        if user_cart:
            existing_payment = Payment.objects.filter(cart=user_cart).first()

            if existing_payment:
                existing_payment.total_amount = total_amount
                existing_payment.need = request_text
                existing_payment.phone_number = phone_number
                existing_payment.save()
                payment = existing_payment
            else:
                payment = Payment.objects.create(
                    cart=user_cart,
                    total_amount=total_amount,
                    need=request_text,
                    phone_number=phone_number
                )

        return render(request, 'buyers/payment.html', {
            'total_amount': total_amount,
            'item_info_list': item_info_list,
            'phone_number': phone_number,
            'request_text': request_text,
            'payment': payment,
        })

    return redirect('buyers:cart')

# 결합된 카트 하나를 생성해서 이걸 넘겨줄지 위에 걸 쓸지
# @login_required
# def payment(request):
#     if request.method == 'POST':
#         total_amount = int(request.POST.get('total_price'))
#         phone_number = request.POST.get('phone_number', '')
#         items = request.POST.getlist('items[]')
#         request_text = request.POST.get('request_text')

#         item_info_list = []
#         for item in items:
#             item_name, item_quantity, item_price = item.split('|')
#             item_info = {
#                 'name': item_name,
#             }
#             item_info_list.append(item_info)

#         user_carts = Cart.objects.filter(user=request.user)
#         combined_items = []  # 모든 카트의 아이템을 담을 리스트
#         total_price = 0  # 모든 카트의 총 금액

#         for user_cart in user_carts:
#             combined_items.extend(user_cart.cartitem_set.all())  # 해당 카트의 아이템들을 리스트에 추가
#             total_price += user_cart.get_total_price()  # 해당 카트의 총 금액을 전체 총 금액에 추가

#         combined_cart = Cart.objects.create(user=request.user)  # 새로운 결합된 카트 생성

#         for item in combined_items:
#             CartItem.objects.create(cart=combined_cart, menu=item.menu, quantity=item.quantity)

#         payment = Payment.objects.create(
#             cart=combined_cart,
#             total_amount=total_price,
#             need=request_text,
#             phone_number=phone_number
#         )

#         return render(request, 'buyers/payment.html', {
#             'total_amount': total_price,
#             'item_info_list': item_info_list,
#             'phone_number': phone_number,
#             'request_text': request_text,
#             'payment': payment,
#         })

#     return redirect('buyers:cart')




# @login_required
# def payment_order_detail(request, payment_id):
#     payment = get_object_or_404(Payment, id=payment_id, cart__buyer=request.user)
#     selected_carts = Cart.objects.filter(payment=payment)

#     context = {
#         'payment': payment,
#         'selected_carts': selected_carts,
#     }
#     return render(request, 'buyers/payment_order_detail.html', context)


@login_required
def buyer_mypage(request):
    user = request.user
    payments = Payment.objects.filter(cart__buyer=request.user).order_by('-order_date')
    
    context = {
        'user': user,
        'payments':payments,
    }
    return render(request, 'buyers/buyer_mypage.html', context)





