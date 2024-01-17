from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.core.paginator import Paginator  # 处理分页
from .forms import UserRegistrationForm
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
    users_list = User.objects.exclude(is_superuser=True)
    query = request.GET.get('q')
    if query:
        users_list = users_list.filter(Q(username__contains=query))
    paginator = Paginator(users_list, 10)
    page_number = request.GET.get('page')
    users = paginator.get_page(page_number)
    return render(request, 'books/user_management.html', {'users': users})
