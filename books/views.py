from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .forms import UserRegistrationForm
from .models import UserProfile
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages


# Create your views here.


def register(request):
    # 注册
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            user_form.save()  # 保存表单
            return redirect('books:login')
        else:
            print(user_form.errors)
    else:
        user_form = UserRegistrationForm()
    return render(request, 'books/register.html', {'user_form': user_form})


@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('books:home')
        else:
            messages.error(request, '用户名或密码不正确')
    return render(request, 'books/login.html')


def home(request):
    return render(request, 'books/home.html')
