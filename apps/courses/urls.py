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
    url(r'^course_list/$', course_list, name='course_list'),  # 获取所有的课程
    url(r'^course_detail/(\d+)/$', course_detail, name='course_detail'),  # 获取课程详情
    url(r'^course_video/(\d+)/$', course_video, name='course_video'),  # 视频

    url(r'^course_comment/(\d+)/$', course_comment, name='course_comment'),  # 评论
]
