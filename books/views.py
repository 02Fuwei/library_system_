from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .forms import UserRegistrationForm
from .models import UserProfile
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm


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


@login_required
def home(request):
    return render(request, 'books/home.html')


@login_required
def profile_view(request):
    #  个人资料
    user = request.user  # user属性，它表示当前用户的实例
    profile = user.userprofile
    context = {
        'user': user,
        'profile': profile
    }
    return render(request, 'books/profile.html', context)


def logout_view(request):
    #  登出
    logout(request)
    return redirect('books:login')


@login_required
def change_password(request):
    """
    修改密码
    """
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # 用于在用户更改密码后更新其会话，以防止用户被登出。
            return redirect('books:home')
        # else:
        #     messages.error(request, '请修改以下错误')
    else:
        form = PasswordChangeForm(user=request.user)
    return render(request, 'books/change_password.html', {'form': form})
