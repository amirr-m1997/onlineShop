from django.shortcuts import render, get_object_or_404
from .cart import Cart
from shopApp.models import Product
from django.http import JsonResponse
from shopApp.forms import CartEditForm
from shopApp.models import *
from django.shortcuts import render, redirect, get_object_or_404


def cart_summery(request):
    cart = Cart(request)
    cart_products = cart.get_prods()
    quantities = cart.get_quantity()
    color = cart.get_color()
    size = cart.get_size()
    sizes = Size.objects.all().values('id', 'name')
    colors = Color.objects.all().values('id', 'name')
    tedads = Tedad.objects.all().values('id', 'name')
    return render(request, 'cart_summery.html',
                  {'cart_products': cart_products, 'quantities': quantities, 'color': color, 'size': size,'sizes': sizes, 'colors': colors, 'tedads': tedads})


# def cart_summery(request):
#     cart = Cart(request)
#     cart_products = cart.get_prods()
#     quantities = cart.get_quantity()
#     color_list = [value['color'] for value in cart.get_color().values()]
#     size_list = [value['size'] for value in cart.get_size().values()]
#     return render(request, 'cart_summery.html', {'cart_products': cart_products, 'quantities': quantities, 'color': color_list, 'size': size_list})


def cart_add(request):
    cart = Cart(request)
    if request.method == 'POST' and request.POST.get('action') == 'post':
        product_id = request.POST.get('product_id')
        product_size = request.POST.get('product_size')
        product_color = request.POST.get('product_color')
        product_number = request.POST.get('product_number')
        if not product_id or not product_size or not product_color or not product_number:
            return JsonResponse({'error': 'برخی از فیلدها خالی هستند.'}, status=400)

        try:
            product_number = int(product_number)
            if product_number < 0:
                return JsonResponse({'error': 'محصولی انتخاب نکردید.'}, status=400)
        except ValueError:
            return JsonResponse({'error': 'تعداد محصول باید عدد باشد.'}, status=400)

        product = get_object_or_404(Product, id=int(product_id))
        cart.add(product=product, quantity=product_number, color=product_color, size=product_size)
        cart_quantity = cart.__len__()

        return JsonResponse({'product_name': product.name, 'quantity': cart_quantity})
    return JsonResponse({'error': 'درخواست نامعتبر است.'}, status=400)


# def cart_add(request):
#     cart = Cart(request)
#     if request.POST.get('action') == 'post':
#         product_id = int(request.POST.get('product_id')) #from ajax
#         product_qty = int(request.POST.get('product_qty')) #from ajax
#         product = get_object_or_404(Product, id=product_id)
#         cart.add(product=product, quantity=product_qty)
#         cart_quantity = cart.__len__()
#         print('------>2',cart_quantity)
#         return JsonResponse({'product name': product.name, 'quantity': cart_quantity})


def cart_delete(request):
    pass


from django.contrib import messages


def cart_edit(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        form = CartEditForm(request.POST)
        if form.is_valid():
            quantity = form.cleaned_data['quantity']
            size = get_object_or_404(Size, id=form.cleaned_data['size'])
            color = get_object_or_404(Color, id=form.cleaned_data['color'])
            cart.update(product=product, quantity=quantity, size=size, color=color)

            # افزودن پیام موفقیت
            messages.success(request, 'سبد خرید شما با موفقیت ویرایش شد.')

            # هدایت کاربر به صفحه قبلی (سبد خرید)
            return redirect('cart_summery')

    # اگر فرم معتبر نبود، هدایت به صفحه سبد خرید
    return redirect('cart_summery')

from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .cart import Cart

@require_POST
def cart_update(request):
    cart = Cart(request)
    product_id = request.POST.get('product_id')
    quantity = request.POST.get('quantity')
    size = request.POST.get('size')
    color = request.POST.get('color')

    if product_id and quantity and size and color:
        try:
            cart.update(product_id, quantity, size, color)
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    else:
        return JsonResponse({'success': False, 'error': 'Invalid data'})
