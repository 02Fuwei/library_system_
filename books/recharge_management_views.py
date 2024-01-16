"""
充值管理
"""
from django.shortcuts import render, redirect, get_object_or_404
from .models import UserProfile, User
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, HttpResponse
from django.db.models import Q
from django.contrib import messages
from decimal import Decimal


@login_required
def recharge_management(request):
    # 充值管理
    users = User.objects.exclude(is_superuser=True)
    return render(request, 'books/recharge_management.html', {'users': users})


def recharge(request, user_id):
    # 充值
    user = get_object_or_404(User, pk=user_id)
    profile = user.userprofile
    if request.method == 'POST':
        recharge_amount = request.POST.get('amount')
        if recharge_amount:
            try:
                recharge_amount = Decimal(recharge_amount)
                profile.fines += recharge_amount
                profile.save()
                messages.success(request, '充值成功')
                return redirect('books:recharge', user_id=user_id)
            except ValueError:
                messages.error(request, '请输入有效的充值金额。')
    return render(request, 'books/recharge.html', {'user': user})
