from django.urls import path
from . import views, user_management_views, book_management_views, loans_management_views,recharge_management_views

app_name = 'books'
urlpatterns = [
    path('', views.login_view, name='login'),
    path('register/', views.register, name='register'),  # 注册
    path('login/', views.login_view, name='login'),  # 登录
    path('home/', views.home, name='home'),  # 主页
    path('logout/', views.logout_view, name='logout_view'),
    path('profile', views.profile_view, name='profile'),
    path('user_profile/<str:user_id>/', user_management_views.user_profile, name='user_profile'),
    path('user_profile/<str:user_id>/user_edit', user_management_views.user_edit, name='user_edit'),
    path('change_password/', views.change_password, name='change_password'),
    path('user_management/', user_management_views.user_management, name='user_management'),
    path('book_management/', book_management_views.book_list, name='book_list'),
    path('add_book/', book_management_views.add_book, name='add_book'),
    path('book_detail/<int:book_id>/', book_management_views.book_detail, name='book_detail'),
    path('book_edit/<int:book_id>/', book_management_views.book_edit, name='book_edit'),
    path('book_delete/<int:book_id>/', book_management_views.book_delete, name='book_delete'),
    path('borrow_book/<int:book_id>/', book_management_views.borrow_book, name='borrow_book'),
    path('return_book/<int:book_id>/', book_management_views.return_book, name='return_book'),
    path('my_loans/', loans_management_views.my_loans, name='my_loans'),
    path('loans_management/', loans_management_views.loans_management, name='loans_management'),
    path('recharge/<int:user_id>/', recharge_management_views.recharge, name='recharge'),
    path('recharge_management/', recharge_management_views.recharge_management, name='recharge_management'),
]
