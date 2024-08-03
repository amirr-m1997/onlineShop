from django.shortcuts import get_object_or_404
from shopApp.models import Product

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
        self.save()

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())
    # def get_total_items(self):
    #     return sum(item['quantity'] for item in self.cart.values())


    def get_prods(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        return products

    def get_quantity(self):
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
        product_id = str(product_id)
        if product_id in self.cart:
            self.cart[product_id]['quantity'] = quantity
            self.cart[product_id]['size'] = size
            self.cart[product_id]['color'] = color
        else:
            self.cart[product_id] = {
                'quantity': quantity,
                'size': size,
                'color': color
            }
        self.save()

    def clear(self):
        self.session['cart'] = {}
        self.save()
        self.session.modified = True

    def remove(self, product_id):
        product_id = str(product_id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def get_total_price(self):
        #print("Cart:", self.cart)  # Cart: {'3': {'quantity': 2, 'color': 'قرمز', 'size': '16.7'}, '4': {'quantity': 1, 'color': 'قرمز', 'size': '16.7'}}
        product_ids = self.cart.keys()  # دریافت ایدی ها محصولات
        products = Product.objects.filter(id__in=product_ids)
        total_price = 0
        for key, value in self.cart.items():  # key = {'2': ,'3': ,'4': ,'5': } شامل این دیکشنری هست که بصورت رشته هس و باید به عدد تبدیل کنیم
            key = int(key)
            quantity = value['quantity']  # استخراج مقدار quantity # تبدیل value به عدد صحیح
            for product in products:
                if product.id == key:
                    if product.is_sale:
                        total_price += product.sale_price * quantity
                    else:
                        total_price += product.price * quantity
        return total_price


