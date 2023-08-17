from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import json
from sellers.models import *
from sellers.views import *
from .models import *
from buyers.models import *
from django.urls import reverse
from django.contrib import messages
from django.db.models import Sum

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
        option_ids = request.POST.getlist('options')
        # options = Option.objects.filter(menu=menu)
        options = Option.objects.filter(id__in=option_ids, menu=menu)
        
        if cart.market != menu.category.market:
            cart.cartitem_set.all().delete()
            cart_item = CartItem.objects.create(cart=cart, menu=menu, quantity=int(quantity))
            
            # 옵션 추가
            if options:
                cart_item.options.add(*options)
                
            # messages.warning(request, '기존에 있던 다른마켓의 메뉴를 삭제합니다!')
        else:
            if cart.cartitem_set.filter(menu=menu).exists():
                messages.warning(request, '이미 담겨진 상품입니다.')
                cart_item = cart.cartitem_set.get(menu=menu)
                cart_item.quantity += int(quantity)
                # cart_item.save()
            else:
                cart_item = CartItem.objects.create(cart=cart, menu=menu, quantity=int(quantity))
                
                # 옵션 추가
                if options:
                    cart_item.options.add(*options)
                
                # messages.success(request, '상품이 성공적으로 추가되었습니다!')
        

        cart_item.save()
        cart.market = menu.category.market
        cart.save()
        
        return redirect('sellers:seller_detail', cart.market.pk)

    context = {
        'menu': menu,
        'owner': owner,
    }

    return render(request, 'buyers/menu_detail.html', context)

@login_required
def cart(request):
    cart_items = CartItem.objects.filter(cart__user=request.user)
    cart = get_object_or_404(Cart, user=request.user)

    context = {
        'cart_items': cart_items,
        'cart': cart,
    }
    return render(request, 'buyers/cart.html', context)

@csrf_exempt
def item_ajax(request, item_id, *args, **kwargs):
    data = json.loads(request.body)
    item = CartItem.objects.get(pk=item_id)
    cart = get_object_or_404(Cart, user=request.user)

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
        'quantity' : item.quantity,
        'price' : item.total_price(),
        'total' : cart.cart_total_price(),
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

@login_required
def delete_cart_item(request, pk):
    cart_item = get_object_or_404(CartItem, pk=pk)
    cart_item.delete()

    return redirect('buyers:cart')

# @login_required
# def clear_cart(request):
#     market_id = request.POST.get('market_id', '1')
#     cart_items = Cart.objects.filter(user=request.user)

#     if cart_items.exists():
#         cart_items.delete()

#     return redirect('sellers:seller_detail', pk=market_id)

@login_required
def clear_cart(request):
    market_id = request.POST.get('market_id', '1')
    user_cart = get_object_or_404(Cart, user=request.user)

    cart_items = user_cart.cartitem_set.all()

    if cart_items.exists():
        cart_items.delete()

    return redirect('sellers:seller_detail', pk=market_id)

@login_required
def payment(request):
    if request.method == 'POST':
        total_amount = int(request.POST.get('total_price'))
        phone_number = request.POST.get('phone_number', '')
        request_text = request.POST.get('request_text')
        payment_method = request.POST.get('payment_method')
        order_type = request.POST.get('order_type')

        user_cart = Cart.objects.filter(user=request.user).first()
        
        if user_cart:
            payment = Payment.objects.create(
                cart=user_cart,
                total_amount=total_amount,
                need=request_text,
                phone_number=phone_number,
                payment_method=payment_method,
                order_type=order_type
            )

            for cart_item in user_cart.cartitem_set.all():
                item_total_price = cart_item.total_price()
                payment_item = PaymentItem.objects.create(
                    payment=payment,
                    total_amount=item_total_price,
                    menu=cart_item.menu,
                    quantity=cart_item.quantity
                )
                payment_item.options.set(cart_item.options.all())

            user_cart.cartitem_set.all().delete()

            return render(request, 'buyers/payment.html', {
                'total_amount': total_amount,
                'phone_number': phone_number,
                'request_text': request_text,
                'payment_method': payment_method,
                'order_type': order_type,
                'payment': payment,
            })

    return redirect('buyers:cart')











# @login_required
# def complete_payment(request):
#     if request.method == 'POST':
#         user_cart = Cart.objects.filter(user=request.user).first()
#         if user_cart:
#             user_cart.cart_items.all().delete()
        
#         return redirect('users:mypage')





# @login_required
# def payment_order_detail(request, payment_id):
#     payment = get_object_or_404(Payment, id=payment_id, cart__buyer=request.user)
#     selected_carts = Cart.objects.filter(payment=payment)

#     context = {
#         'payment': payment,
#         'selected_carts': selected_carts,
#     }
#     return render(request, 'buyers/payment_order_detail.html', context)


# @login_required
# def buyer_mypage(request):
#     user = request.user
#     payments = Payment.objects.filter(cart__buyer=request.user).order_by('-order_date')
    
#     context = {
#         'user': user,
#         'payments':payments,
#     }
#     return render(request, 'buyers/buyer_mypage.html', context)





