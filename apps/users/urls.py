"""Gu URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin

from users.views import *

# 我们的跳转链接 类似java 的 url
urlpatterns = [
    url(r'^users_register/$', users_register, name='users_register'),  # 注册
    url(r'^users_login/$', users_login, name='users_login'),  # 登录
    url(r'^users_logout/$', users_logout, name='users_logout'),  # 登出
    url(r'^users_active/(\w+)/$', users_active, name='users_active'),  # 邮箱激活

    # 忘记密码
    url(r'^users_forget/$', users_forget, name='users_forget'),
    url(r'^users_reset/(\w+)/$', users_reset, name='users_reset'),  # 邮箱激活

    url(r'^users_info/$', users_info, name='users_info'),  # 个人中心

    url(r'^users_change_image/$', users_change_image, name='users_change_image'),  # 个人中心之修改头像
    url(r'^users_change_info/$', users_change_info, name='users_change_info'),  # 个人中心之修改消息
    url(r'^users_change_email/$', users_change_email, name='users_change_email'),  # 个人中心之修改邮箱

    url(r'^users_change_reset_email/$', users_change_reset_email, name='users_change_reset_email'),  # 个人中心之修改邮箱发送邮件

    url(r'^user_course/$', user_course, name='user_course'),  # 我的课程

    url(r'^user_love_org/$', user_love_org, name='user_love_org'),  # 我的收藏之机构
    url(r'^user_love_course/$', user_love_course, name='user_love_course'),  # 我的收藏之课程
    url(r'^user_love_teacher/$', user_love_teacher, name='user_love_teacher'),  # 我的收藏之教师


    url(r'^user_message/$', user_message, name='user_message'),  # 我的消息
    url(r'^update_user_message_status/$', update_user_message_status, name='update_user_message_status'),  #  更改我的消息的 读取状态



]
