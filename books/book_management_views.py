"""
图书管理
"""
from django.shortcuts import render, redirect
from .models import Book
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from .forms import BookForm


@login_required
def book_list(request):
    # 图书列表
    books = Book.objects.all()
    paginator = Paginator(books, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'books/book_list.html', {'page_obj': page_obj})


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
