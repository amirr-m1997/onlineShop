from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import RegisterForm


def login_page(request):
    if request.method == "POST":
        username = request.POST.get('user_name')
        password = request.POST.get('password')
        rememberme = request.POST.get('rememberme', False)
        if not User.objects.filter(username=username).exists():
            messages.error(request, 'نام کاربری اشتباه است !')
            return redirect('login')
        user = authenticate(username=username, password=password)
        if user is None:
            messages.error(request, "رمز عبور اشتباه است!")
            return redirect('login')
        else:
            login(request, user)
            messages.success(request, 'شما با موفقیت وارد شدید!')
            if not rememberme:
                request.session.set_expiry(0)  # Session expires when the browser is closed.  if set_expiry(0)
            return redirect('index')
    return render(request, 'login.html')


def logout_user(request):
    logout(request)
    messages.error(request, 'با موفقیت خارج شدی!')
    return redirect("index")


def register_page(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            if User.objects.filter(username=username).exists():
                messages.error(request, "این نام کاربری از قبل وجود دارد!")
                return redirect('register')
            user = User.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                username=username,
                password=password
            )
            messages.success(request, "مشخصات با موفقیت ذخیره شد.")
            return redirect('login')
    else:
        form = RegisterForm()

    return render(request, 'register.html', {'form': form})
