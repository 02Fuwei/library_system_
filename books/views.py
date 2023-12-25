from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .forms import UserRegistrationForm
import uuid
from .models import UserProfile


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


def login(request):
    return render(request, 'books/login.html')
