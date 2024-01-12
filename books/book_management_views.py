"""
图书管理
"""
from django.shortcuts import render, redirect, get_object_or_404
from .models import Book, UserProfile, Loan
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from .forms import BookForm
from django.http import HttpResponseForbidden, HttpResponse
from django.db.models import Q
from django.utils import timezone


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


def borrow_book(request, book_id):
    # 借书
    book = get_object_or_404(Book, pk=book_id)
    user_profile = request.user.userprofile
    if request.method == 'POST':
        if book.in_stock > 0:
            # 库存大于等于0
            # 已借书总数
            books_borrowed_count = Loan.objects.filter(user=request.user, return_date__isnull=True).count()
            if books_borrowed_count < user_profile.loan_limit:
                # 借书总数<=限额
                if not Loan.objects.filter(book_id=book_id, user=request.user, return_date__isnull=True).exists():
                    # 该书未借
                    Loan.objects.create(book=book, user=request.user)  # 创建借书记录
                    book.in_stock -= 1  # 更新库存
                    book.save()
                    return render(request, 'books/book_detail.html', {'book': book, 'messages': '借书成功'})
                else:
                    return render(request, 'books/book_detail.html', {'book': book, 'messages': '该书已借'})
            else:
                # 借书总数>限额
                return render(request, 'books/book_detail.html', {'book': book, 'messages': '您已达到借书限额'})
        else:
            return render(request, 'books/book_detail.html', {'book': book, 'messages': '该书库存不足'})
    return render(request, 'books/book_detail.html', {'book': book})


def return_book(request, book_id):
    # 还书
    book = get_object_or_404(Book, pk=book_id)
    try:
        # 匹配book_id和user
        loan = Loan.objects.get(book_id=book_id, user=request.user, return_date__isnull=True)
    except Loan.DoesNotExist:
        return render(request, 'books/book_detail.html', {'book': book, 'messages': '您未该借书或已还书'})
    if request.method == 'POST':
        loan.return_date = timezone.now().date()
        book.in_stock += 1
        book.save()
        loan.save()
    return render(request, 'books/book_detail.html', {'book': book, 'messages': '还书成功'})
