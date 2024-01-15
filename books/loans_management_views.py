"""
订阅管理
"""
from django.shortcuts import render, redirect, get_object_or_404
from .models import Book, UserProfile, Loan
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from .forms import BookForm
from django.http import HttpResponseForbidden, HttpResponse
from django.db.models import Q


def my_loans(request):
    # 我的借阅
    loans = Loan.objects.filter(user=request.user)  # 我的订阅
    query = request.GET.get('q')
    if query:
        loans = loans.filter(Q(book__title__icontains=query))
    paginator = Paginator(loans, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'books/my_loans.html', {'loans': loans, 'page_obj': page_obj})


def loans_management(request):
    # 借阅管理
    loans = Loan.objects.all()  # 获取所有
    query = request.GET.get('q')
    if query:
        loans = loans.filter(Q(user__username__icontains=query))
    paginator = Paginator(loans, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'books/loans_management.html', {'loans': loans, 'page_obj': page_obj})
