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

# def register_page(request):
#     # Check if the HTTP request method is POST (form submission)
#     if request.method == 'POST':
#         first_name = request.POST.get('first_name')
#         last_name = request.POST.get('last_name')
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#
#         # Check if a user with the provided username already exists
#         user = User.objects.filter(username=username)
#
#         if user.exists():
#             # Display an information message if the username is taken
#             messages.info(request, "این نام کاربری از قبل وجود دارد!")
#             return redirect('register')
#
#         # Create a new User object with the provided information
#         user = User.objects.create_user(
#             first_name=first_name,
#             last_name=last_name,
#             username=username
#         )
#
#         # Set the user's password and save the user object
#         user.set_password(password)
#         user.save()
#
#         # Display an information message indicating successful account creation
#         messages.info(request, "مشخصات با موفقیت ذخیره شد.")
#         return redirect('/register/')
#
#     # Render the registration page template (GET request)
#     return render(request, 'register.html')


# def login_user(request):
#     if request.method == 'POST':
#         user_name = request.POST['user_name']
#         password = request.POST['password']
#         rememberme = request.POST.get('rememberme', False)
#         user = authenticate(request, username=user_name, password=password)
#         if user is not None:
#             login(request, user)
#             messages.success(request, 'شما با موفقیت وارد شدید!')
#             if not rememberme:
#                 request.session.set_expiry(1)  # Session expires when the browser is closed.
#             return redirect('index')
#         else:
#             messages.error(request, 'نام کاربری یا رمز عبور اشتباه است.')
#             return redirect('login')
#     else:
#         return render(request, 'login.html')
