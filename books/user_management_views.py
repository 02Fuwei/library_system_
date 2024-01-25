from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.core.paginator import Paginator  # 处理分页
from .forms import UserRegistrationForm, UserProfileForm
from .models import UserProfile
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.db.models import Q


# Create your views here.


def user_management(request):
    """
    用户管理
    :param request:
    :return:
    """
    # users_list = User.objects.all().prefetch_related('userprofile')
    users = User.objects.exclude(is_superuser=True).order_by('id')
    query = request.GET.get('q')
    if query:
        users = users.filter(Q(username__contains=query))
    paginator = Paginator(users, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'books/user_management.html', {'users': users, 'page_obj': page_obj})


def user_profile(request, user_id):
    # 用户详情

    user = get_object_or_404(User, pk=user_id)
    profile = user.userprofile
    if request.user != user and not request.user.userprofile.membership_type:
        return HttpResponseForbidden("您没有权限查看这个页面")
    return render(request, 'books/user_profile.html', {'user': user, 'profile': profile})


def user_edit(request, user_id):
    # 用户编辑
    # 如果没有提供 user_id，表示编辑当前登录用户
    if user_id is None:
        user = request.user
    else:
        user = get_object_or_404(User, pk=user_id)

    # 如果 UserProfile 是扩展 User 模型的模型，确保获取正确的实例
    profile = user.userprofile

    if request.method == 'POST':
        user_form = UserProfileForm(request.POST, instance=profile)
        if user_form.is_valid():
            user.first_name = user_form.cleaned_data['first_name']
            user.last_name = user_form.cleaned_data['last_name']
            user.email = user_form.cleaned_data['email']
            user.save()
            user_form.save()
            context = {
                'user': user,
                'profile': profile,
                'form': user_form,
            }
            messages.success(request, '保存成功')
            return render(request, 'books/user_edit.html', context)
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
    return render(request, 'books/user_edit.html', context)
