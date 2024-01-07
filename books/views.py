from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from .forms import UserRegistrationForm
from .models import UserProfile
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from .forms import UserProfileForm


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
    user = request.user
    profile = UserProfile.objects.get(user=user)
    return render(request, 'books/home.html', {'profile': profile})


@login_required
# def profile_view(request, user_id):
#     #  个人资料
#     user = get_object_or_404(User, pk=user_id)
#     profile = user.userprofile
#     context = {
#         'user': user,
#         'profile': profile
#     }
#     return render(request, 'books/profile.html', context)
def profile_view(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    profile = user.userprofile
    # 检查当前登录用户是否有权查看这个页面
    if request.user != user and not profile.membership_type:
        return HttpResponseForbidden("您没有权限查看这个页面")
    if request.method == 'POST':
        user_form = UserProfileForm(request.POST, instance=profile)
        if user_form.is_valid():
            user.first_name = user_form.cleaned_data['first_name']
            user.last_name = user_form.cleaned_data['last_name']
            user.email = user_form.cleaned_data['email']
            user.save()
            user_form.save()
            return redirect('books:home')
    else:
        user_form = UserProfileForm(instance=profile, initial={
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email
        })
    context = {
        'user': user,
        'profile': profile,
        'form': user_form,
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
