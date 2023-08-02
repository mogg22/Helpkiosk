from django.conf import settings
from sellers.models import Menu

class Cart(object):
    # 초기화 작업
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_ID)
        if not cart:
            cart = self.session[settings.CART_ID] = {}
        self.cart = cart
    
    # 몇 개가 들어있는지 알기 위해 
    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values()) # 제품 안의 수량 다 더하기
    
    # 어떤 요소들을 줄건지 
    def __iter__(self):
        menu_ids = self.cart.keys() # 카트에 메뉴들 번호 가져오기
        
        menus = Menu.objects.filter(id__in=menu_ids)  # 싹 다 데이터베이스에서 가져옴, id가 menu_ids안에 들어가 있는 것(장바구니 안에 들어있는 것에 해당하는 것) 달라고, 장바구니에 들어있는 정보들만 디비에서 빼온다
        
        for menu in menus:
            self.cart[str(menu.id)]['menu'] = menu
            
        for item in self.cart.values():  # 장바구니 안에 들어 있는 거 item
            item['price'] = int(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            
            yield item
        
    def add(self, menu, quantity=1, is_update=False):
        menu_id = str(menu.id)
        if menu_id not in self.cart:
            self.cart[menu_id] = {'quantity':0, 'price':menu.price}
            
        if is_update:
            self.cart[menu_id]['quantity'] = quantity
        else:
            self.cart[menu_id]['quantity'] +=quantity
            
        self.save()
        
    def save(self):
        self.session[settings.CART_ID] = self.cart
        # 제품 정보 중간 중간 변경 됐을 때 True로 해서 업데이트
        self.session.modified = True
        
    def remove(self, menu):
        menu_id = str(menu.id)
        if menu_id in self.cart:
            del(self.cart[menu_id])  # 카트 안에 있으면 지워!
            self.save()
            
    def clear(self):  # 장바구니 비우기
        self.session[settings.CART_ID] = {}
        self.session.modified = True  # save 호출 대신
        
    def get_menu_total(self):
        return sum(item['price'] * item['quantity'] for item in self.cart.values())