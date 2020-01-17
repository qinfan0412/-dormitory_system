from django.urls import path, re_path
from student import views

urlpatterns = [
    path('register/', views.register),  # 注册路由
    path('login/', views.login),  # 登陆路由
    re_path('^$', views.login),  # 登陆路由
    path('forget_password/', views.forget_password),  # 忘记密码路由
    path('logout/', views.logout),  # 登出路由
    path('index/', views.index),  # 主页路由
    path('update_password/', views.update_password),  # 更新个人密码页
    path('user_info/', views.user_info),  # 个人中心页
]
