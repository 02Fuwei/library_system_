"""
订阅管理
"""
from django.shortcuts import render, redirect, get_object_or_404
from .models import Book, UserProfile, Loan
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from .forms import BookForm
from django.http import HttpResponseForbidden, HttpResponse


def my_loans(request):
    # 我的借阅
    loans = Loan.objects.filter(user=request.user)  # 我的订阅
    return render(request, 'books/my_loans.html', {'loans': loans})


def loans_management(request):
    # 借阅管理
    loans = Loan.objects.all()  # 获取所有
    return render(request, 'books/loans_management.html', {'loans': loans})
