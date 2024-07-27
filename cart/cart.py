from django.contrib.sessions.models import Session
from shopApp.models import Product

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import models


# def cart_add(request):
#     cart = Cart(request)
#     if request.POST.get('action') == 'post':
#         product_id = int(request.POST.get('product_id'))
#         product_size = request.POST.get('product_size')
#         product_color = request.POST.get('product_color')
#         product_number = request.POST.get('product_number')
#
#         if not product_size or not product_color or not product_number:
#             return JsonResponse({'error': 'برخی از فیلدها خالی هستند.'}, status=400)
#
#         product = get_object_or_404(Product, id=product_id)
#         cart.add(product=product, quantity=int(product_number), size=product_size, color=product_color)
#         cart_quantity = cart.__len__()
#
#         return JsonResponse({'product_name': product.name, 'quantity': cart_quantity})
#
#
# class Cart:
#     def __init__(self, request):
#         self.session = request.session
#         cart = self.session.get('session_key')
#         if 'session_key' not in request.session:
#             cart = self.session['session_key'] = {}
#         self.cart = cart
#
#     def add(self, product, quantity, size, color):
#         product_id = str(product.id)
#         product_key = f'{product_id}_{size}_{color}'
#         if product_key in self.cart:
#             self.cart[product_key]['quantity'] += quantity
#         else:
#             self.cart[product_key] = {'quantity': quantity, 'size': size, 'color': color}
#         self.session.modified = True
#
#     def __len__(self):
#         return sum(item['quantity'] for item in self.cart.values())
#
#     def get_prods(self):
#         product_ids = [key.split('_')[0] for key in self.cart.keys()]
#         products = Product.objects.filter(id__in=product_ids)
#         return products
#
#     def get_quantity(self):
#         return self.cart

    # def add(self, product, quantity):
    #     product_id = str(product.id)  # تبدیل شناسه محصول به رشته
    #     product_qty = str(quantity)  # تبدیل شناسه محصول به رشته
    #     if product_id in self.cart:  # اگر محصول از قبل در سبد خرید وجود دارد
    #         pass  # هیچ کاری انجام نده
    #     else:
    #         self.cart[product_id] = int(product_qty)  # افزودن محصول به سبد خرید
    #     self.session.modified = True  # اصلاح سبد خرید بعد از هر تغییرگو


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('session_key')
        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}
        self.cart = cart

    def add(self, product, quantity, color, size):
        product_id = str(product.id)
        if product_id in self.cart:
            self.cart[product_id]['quantity'] += quantity
            self.cart[product_id]['color'] = color
            self.cart[product_id]['size'] = size
        else:
            self.cart[product_id] = {
                'quantity': quantity,
                'color': color,
                'size': size
            }
        self.session.modified = True

    def __len__(self):
        return len(self.cart.values())

    def get_prods(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        return products

    def get_quantity(self):#tedad
        quantities = self.cart
        return quantities
    def get_color(self):
        color = self.cart
        return color

    def get_size(self):
        size = self.cart
        return size
    def save(self):
        self.session.modified = True

    def update(self, product_id, quantity, size, color):
        product = get_object_or_404(Product, id=product_id)
        cart_item = self.cart.get(str(product_id))

        if cart_item:
            cart_item['quantity'] = quantity
            cart_item['size'] = size
            cart_item['color'] = color
        else:
            cart_item = {
                'product_id': product_id,
                'name': product.name,
                'price': str(product.price),
                'quantity': quantity,
                'size': size,
                'color': color,
            }

        self.cart[str(product_id)] = cart_item
        self.save()



# ساخت سشن
# class Cart:
#     def __init__(self, request):
#         self.session = request.session  # دسترسی به شیء جلسه (session)
#         cart = self.session.get('session_key')  # دریافت سبد خرید از جلسه
#         if 'session_key' not in request.session:  # اگر سبد خرید در جلسه وجود ندارد
#             cart = self.session['session_key'] = {}  # ایجاد یک سبد خرید جدید در جلسه
#         self.cart = cart  # ذخیره سبد خرید در شیء
#
#     def add(self, product, quantity, size, color):
#         product_id = str(product.id)  # تبدیل شناسه محصول به رشته
#         product_key = f'{product_id}_{size}_{color}'  # کلید منحصربه‌فرد برای محصول بر اساس شناسه، سایز و رنگ
#         if product_key in self.cart:  # اگر محصول از قبل در سبد خرید وجود دارد
#             self.cart[product_key]['quantity'] += quantity  # افزایش تعداد محصول
#         else:
#             self.cart[product_key] = {'quantity': quantity, 'size': size, 'color': color}  # افزودن محصول به سبد خرید
#         self.session.modified = True  # اصلاح سبد خرید بعد از هر تغییر
#
#     # def add(self, product, quantity):
#     #     product_id = str(product.id)  # تبدیل شناسه محصول به رشته
#     #     product_qty = str(quantity)  # تبدیل شناسه محصول به رشته
#     #     if product_id in self.cart:  # اگر محصول از قبل در سبد خرید وجود دارد
#     #         pass  # هیچ کاری انجام نده
#     #     else:
#     #         self.cart[product_id] = int(product_qty)  # افزودن محصول به سبد خرید
#     #     self.session.modified = True  # اصلاح سبد خرید بعد از هر تغییرگو
#
#     def __len__(self):
#         return len(self.cart)
#
#     def get_prods(self):
#         product_ids = self.cart.keys() # ایدی همه محصولاتی که داخل سبد خرید هستند
#         products=Product.objects.filter(id__in=product_ids)
#         return products
#
#     def get_quantity(self):
#         quantitities = self.cart
#         return quantitities
#



