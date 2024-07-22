from django.contrib import messages
from .models import Product, Customer, Order, Category
from django.shortcuts import render, redirect



def index(request):
    all_products = Product.objects.all()
    return render(request, 'index.html', {'all_products': all_products})

def product(request, pk):
    product = Product.objects.get(id=pk)
    return render(request,'product.html', {'product': product})

    

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

