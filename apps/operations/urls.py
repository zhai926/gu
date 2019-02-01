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
from .views import *

urlpatterns = [
    url(r'^user_ask/$', user_ask, name='user_ask'),  # 用户咨询
    url(r'^user_love/$', user_love, name='user_love'),  # 用户收藏
    url(r'^user_deletelove/$', user_deletelove, name='user_deletelove'),  # 删除收藏
    url(r'^user_comment/$', user_comment, name='user_comment'),  # 用户评论
]
