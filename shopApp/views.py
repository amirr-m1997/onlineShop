from django.contrib import messages
from .models import Product, Customer, Order, Category, Size,Color,Tedad
from django.shortcuts import render, redirect
from django.shortcuts import render, get_object_or_404


def index(request):
    all_products = Product.objects.all()
    return render(request, 'index.html', {'all_products': all_products})


def product(request, pk):
    product = get_object_or_404(Product, id=pk)
    product_data = Product.objects.filter(id=pk).values()
    sizes = Size.objects.all().values('id', 'name')
    colors = Color.objects.all().values('id', 'name')
    tedads = Tedad.objects.all().values('id', 'name')
    return render(request, 'product.html', {'product': product, 'sizes': sizes, 'colors': colors, 'tedads': tedads})



def about(request):
    return render(request, 'about.html')


def category(request, cat):
    cat=cat.replace('-', ' ')
    try:
        category = Category.objects.get(name=cat)
        all_products = Product.objects.filter(category=category)
        return render(request, 'category.html', {'all_products': all_products, 'category': category})
    except:
        messages.error(request, 'دسته بندی مورد نظر شما موجود نیست.')
        return redirect('index')

