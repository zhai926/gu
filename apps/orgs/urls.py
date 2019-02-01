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
from orgs.views import *

urlpatterns = [
    url(r'^orgs_list/$', orgs_list, name='orgs_list'),  # 获取所有的课程

    url(r'^orgs_detail/(\d+)/$', orgs_detail, name='orgs_detail'),  # 课程详情
    url(r'^orgs_detail_course/(\d+)/$', orgs_detail_course, name='orgs_detail_course'),  # 课程详情的课程
    url(r'^orgs_detail_desc/(\d+)/$', orgs_detail_desc, name='orgs_detail_desc'),  # 课程详情的课程
    url(r'^orgs_detail_teacher/(\d+)/$', orgs_detail_teacher, name='orgs_detail_teacher'),  # 课程详情的讲师

    url(r'^teacher_list/$', teacher_list, name='teacher_list'),  # 获取所有的讲师
    url(r'^teacher_detail/(\d+)/$', teacher_detail, name='teacher_detail'),  # 讲师详情

]
