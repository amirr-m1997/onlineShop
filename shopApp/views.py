import jdatetime
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# from authenticatesUsers.userSessions import UserSession
from cart.cart import Cart
from .models import Product, Customer, Order, Category, Size, Color, Tedad
from django.shortcuts import render, redirect, get_object_or_404
from .models import Order, Product, Customer


def index(request):
    all_products = Product.objects.all()
    return render(request, 'index.html', {'all_products': all_products})


def product(request, pk):
    product = get_object_or_404(Product, id=pk)
    product_data = Product.objects.filter(id=pk).values()
    sizes = Size.objects.all().values('id', 'name')
    colors = Color.objects.all().values('id', 'name')
    tedads = Tedad.objects.all().values('id', 'name')
    product_quantity = product.quantity  # تعداد محصول را از دیتابیس می‌گیریم
    update_product = range(1, product_quantity + 1)
    return render(request, 'product.html',
                  {'product': product,
                   'sizes': sizes,
                   'colors': colors,
                   'tedads': tedads,
                   })


def about(request):
    return render(request, 'about.html')


def category(request, cat):
    cat = cat.replace('-', ' ')
    try:
        category = Category.objects.get(name=cat)
        all_products = Product.objects.filter(category=category)
        return render(request, 'category.html', {'all_products': all_products, 'category': category})
    except:
        messages.error(request, 'دسته بندی مورد نظر شما موجود نیست.')
        return redirect('index')


@login_required
def order_view(request):
    cart = Cart(request)
    sumPrice = cart.get_total_price()
    formatted_sumPrice = "{:,}".format(int(sumPrice))
    sumProduct = cart.__len__()
    customer = request.user  # بدست آوردن نمونه User
    products = cart.get_prods()

    if request.method == 'POST':
        address = request.POST.get('address')
        phone = request.POST.get('phone')

        for product in products:
            order = Order(
                product=product,
                customer=customer,
                quantity=sumProduct,
                address=address,
                phone=phone,
                status=False
            )
            order.save()

        request.session['session_key'] = {}  # خالی کردن سبد خرید
        request.session.modified = True
        orderCustomer=Order.objects.filter(customer=customer).latest('id').customer
        order_id = Order.objects.filter(customer=customer).latest('id').id
        order_date = Order.objects.filter(customer=customer).latest('id').timeOrder
        order_product = Order.objects.filter(customer=customer).latest('id').product
        order_quantity = Order.objects.filter(customer=customer).latest('id').quantity
        order_total = formatted_sumPrice
        order_address = address
        order_phone = phone
        context = {
            'order_id': order_id,
            'order_date': order_date,
            'order_total': order_total,
            'order_address': order_address,
            'order_phone': order_phone,
            'orderCustomer':orderCustomer,
            'order_product': order_product,
            'order_quantity': order_quantity,
        }
        return render(request, 'order_success.html', context)

    context = {
       'sumPrice': formatted_sumPrice,
       'sumProduct': sumProduct,
        'customer': customer,
        'products': products,
    }
    return render(request, 'order.html', context)
