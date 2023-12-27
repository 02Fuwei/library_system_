from django.urls import path
from . import views

app_name = 'books'
urlpatterns = [
    path('register/', views.register, name='register'),  # 注册
    path('login/', views.login_view, name='login'),  # 登录
    path('home/', views.home, name='home'),  # 主页
    path('logout/', views.logout_view, name='logout_view'),
    path('profile/', views.profile_view, name='profile'),
    path('change_password/', views.change_password, name='change_password')
]
