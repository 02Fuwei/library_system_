"""
图书管理
"""
from django.shortcuts import render, redirect, get_object_or_404
from .models import Book, UserProfile, Loan
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from .forms import BookForm
from django.http import HttpResponseForbidden
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
            # 库存大于等于1
            books_borrowed_count = Loan.objects.filter(user=request.user, return_date__isnull=True).count()
            print("借书数量：===", books_borrowed_count)
            if books_borrowed_count <= user_profile.loan_limit:
                # 已借的数等于或超出限制数量
                print('限额')
                Loan.objects.create(book=book, user=request.user)  # 创建借书记录
                book.in_stock -= 1  # 更新款存
                print('request.method == POST')
                book.save()
                return render(request, 'books/book_detail.html', {'book': book, 'messages': '您已达到借书限额'})
        else:
            print('库存不足了')
            return render(request, 'books/book_detail.html', {'book': book, 'messages': '该书库存不足'})
    print('走到这里了')
    return render(request, 'books/book_detail.html', {'book': book})


def return_book(request, loan_id):
    loan = get_object_or_404(Loan, pk=loan_id)
    if request.method == 'POST':
        loan.return_date = timezone.now().date()
        loan.book.in_stock += 1
        loan.save()
        return redirect('books:book_list')
    return render(request, 'books/book_detail.html', {'loan': loan})
