from django.contrib import messages
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.decorators.http import require_POST
from shopApp.forms import CartEditForm
from shopApp.models import *
from .cart import Cart
import locale
locale.setlocale(locale.LC_ALL, '')

def cart_summery(request):
    cart = Cart(request)
    cart_products = cart.get_prods()
    quantities = cart.get_quantity()
    color = cart.get_color()
    size = cart.get_size()
    sizes = Size.objects.all().values('id', 'name')
    colors = Color.objects.all().values('id', 'name')
    tedads = Tedad.objects.all().values('id', 'name')
    total_products = int(cart.__len__())
    total_price = int(cart.get_total_price())
    total_price = locale.format_string("%d", total_price, grouping=True)
    return render(request, 'cart_summery.html', {
        'cart_products': cart_products,
        'quantities': quantities,
        'color': color,
        'size': size,
        'sizes': sizes,
        'colors': colors,
        'tedads': tedads,
        'total_price': total_price,
        'total_products':total_products
    })


def cart_add(request):
    cart = Cart(request)
    if request.method == 'POST' and request.POST.get('action') == 'post':
        product_id = request.POST.get('product_id')
        product_size = request.POST.get('product_size')
        product_color = request.POST.get('product_color')
        product_number = int(request.POST.get('product_number'))

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

        return JsonResponse({'product_name': product.name, 'cart_quantity': cart_quantity})

    return JsonResponse({'error': 'درخواست نامعتبر است.'}, status=400)


def cart_edit(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        form = CartEditForm(request.POST)
        if form.is_valid():
            quantity = form.cleaned_data['quantity']
            size = get_object_or_404(Size, id=form.cleaned_data['size'])
            color = get_object_or_404(Color, id=form.cleaned_data['color'])
            cart.update(product_id=product.id, quantity=quantity, size=size.name, color=color.name)
            messages.success(request, 'سبد خرید شما با موفقیت ویرایش شد.')
            return redirect('cart_summery')
    return redirect('cart_summery')


@require_POST
def cart_update(request):
    cart = Cart(request)
    product_id = request.POST.get('product_id')
    quantity = request.POST.get('quantity')
    size = request.POST.get('size')
    color = request.POST.get('color')

    if product_id and quantity and size and color:
        try:
            product_id = int(product_id)
            quantity = int(quantity)
            cart.update(product_id, quantity, size, color)
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    else:
        return JsonResponse({'success': False, 'error': 'Invalid data'})


def cart_delete(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        cart = Cart(request)
        cart.remove(product_id)
        return HttpResponseRedirect(reverse('cart_summery'))
    return redirect('cart_summery')
