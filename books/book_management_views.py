"""
图书管理
"""
from django.shortcuts import render, redirect, get_object_or_404
from .models import Book, UserProfile
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from .forms import BookForm
from django.http import HttpResponseForbidden
from django.db.models import Q


@login_required
def book_list(request):
    # 图书列表
    query = request.GET.get('q')  # 获取搜索查询
    books = Book.objects.all()
    if query:
        books = books.filter(Q(title__icontains=query))  # 搜索匹配书名的图书
    paginator = Paginator(books, 5)  # 分页
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'books/book_list.html', {'page_obj': page_obj, 'books': books})


def add_book(request):
    # 添加图书
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('books:book_list')
    else:
        form = BookForm()

    return render(request, 'books/add_book.html', {'form': form})


def book_detail(request, book_id):
    # 图书详情
    book = get_object_or_404(Book, pk=book_id)
    return render(request, 'books/book_detail.html', {'book': book})


def book_edit(request, book_id):
    # 图书编辑
    book = get_object_or_404(Book, pk=book_id)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('books:book_detail', book_id=book.id)
    else:
        form = BookForm(instance=book)
    return render(request, 'books/book_edit.html', {'form': form, 'book': book})


def book_delete(request, book_id):
    # 删除图书
    try:
        user_profile = request.user.userprofile
    except UserProfile.DoesNotExist:
        return HttpResponseForbidden('您没有权限删除图书')
    if user_profile.membership_type != 1:
        return HttpResponseForbidden('您没有权限删除图书')
    book = get_object_or_404(Book, pk=book_id)
    book.delete()
    return redirect('books:book_list')
