from django.urls import path
from . import views, user_management_views,book_management_views

app_name = 'books'
urlpatterns = [
    path('register/', views.register, name='register'),  # 注册
    path('login/', views.login_view, name='login'),  # 登录
    path('home/', views.home, name='home'),  # 主页
    path('logout/', views.logout_view, name='logout_view'),
    path('profile/<str:user_id>/', views.profile_view, name='profile'),
    path('change_password/', views.change_password, name='change_password'),
    path('user_management/', user_management_views.user_management, name='user_management'),
    path('book_management/', book_management_views.book_list, name='book_list'),
    path('add_book/', book_management_views.add_book, name='add_book'),
    path('add_book/<int:book_id>/', book_management_views.book_detail, name='book_detail'),
    path('add_book/<int:book_id>/edit', book_management_views.book_edit, name='book_edit'),
    path('add_book/<int:book_id>/delete', book_management_views.book_delete, name='book_delete'),
]
