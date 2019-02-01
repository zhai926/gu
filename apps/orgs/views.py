from django.shortcuts import render
from .models import *
from django.core.paginator import PageNotAnInteger, Paginator, EmptyPage  # 分页
from operations.models import UserLove
from django.db.models import Q


# Create your views here.


# 获取所有的机构
def orgs_list(request):
    orgs_list_all = OrgInfo.objects.all().order_by('cityInfo_id')  # 获取所有的机构
    city_list_all = CityInfo.objects.all()  # 获取所有的城市
    sort_orgs_list = orgs_list_all.order_by('-love_num')[:3]  # 授课机构排名 根据收藏数进行排序 筛选出前三名

    # 根据培训机构进行查询【筛选】
    category = request.GET.get('category', '')
    if category:
        orgs_list_all = orgs_list_all.filter(category=category)

    # 根据城市进行查询 【筛选】
    cityId = request.GET.get('cityId', '')
    if cityId:
        orgs_list_all = orgs_list_all.filter(cityInfo_id=int(cityId))

    # 根据学习人数和课程数进行排序
    sort = request.GET.get('sort', '')
    if sort:
        orgs_list_all = orgs_list_all.order_by('-' + sort)

    # 全局搜索功能
    search_keywords = request.GET.get('keywords', '')
    print("机构列表获取的关键字是:" + search_keywords)
    if search_keywords:
        orgs_list_all = orgs_list_all.filter(
            Q(name__icontains=search_keywords) | Q(desc__icontains=search_keywords) | Q(
                detail__icontains=search_keywords))
    # 分页
    pageNum = request.GET.get('pagenum', '')
    pa = Paginator(orgs_list_all, 3)  # 每页显示3个
    try:
        pages = pa.page(pageNum)
    except PageNotAnInteger:
        pages = pa.page(1)
    except EmptyPage:
        pages = pa.page(pa.num_pages)

    return render(request, 'orgs/org-list.html', {
        'orgs_list_all': orgs_list_all,
        'city_list_all': city_list_all,
        'sort_orgs_list': sort_orgs_list,
        'pages': pages,
        'category': category,
        'cityId': cityId,
        'sort': sort,
        'search_keywords': search_keywords
    })


# 获取课程详情页
def orgs_detail(request, org_id):
    print("传过来的Id:", org_id)
    if org_id:
        org = OrgInfo.objects.filter(id=int(org_id))[0]

        # 计算点击量
        org.click_num += 1
        org.save()

        # 在返回页面数据的时候，需要返回收藏这个机构的状态，根据状态让模板页面显示收藏还是取消收藏。而不能让页面固定显示收藏。
        lovestatus = False
        # 用户是否登录
        if request.user.is_authenticated():
            love = UserLove.objects.filter(love_man=request.user, love_id=int(org_id), love_type=1, love_status=True)
            if love:
                lovestatus = True
        if org:
            return render(request, 'orgs/org-detail-homepage.html', {
                'org': org,
                'detail_type': 'home',
                'lovestatus': lovestatus
            })
        else:
            print("课程不存在")
            pass
    else:
        print("编号不能为空")
        pass


# 机构详情中的课程
def orgs_detail_course(request, org_id):
    print("传过来的Id:", org_id)
    if org_id:
        org = OrgInfo.objects.filter(id=int(org_id))[0]
        org_course_all = org.courseinfo_set.all().order_by('id')
        # 分页
        pageNum = request.GET.get('pagenum', '')
        pa = Paginator(org_course_all, 3)  # 每页显示3个
        try:
            pages = pa.page(pageNum)
        except PageNotAnInteger:
            pages = pa.page(1)
        except EmptyPage:
            pages = pa.page(pa.num_pages)
        if org:
            # 在返回页面数据的时候，需要返回收藏这个机构的状态，根据状态让模板页面显示收藏还是取消收藏。而不能让页面固定显示收藏。
            lovestatus = False
            # 用户是否登录
            if request.user.is_authenticated():
                love = UserLove.objects.filter(love_man=request.user, love_id=int(org_id), love_type=1,
                                               love_status=True)
                if love:
                    lovestatus = True
            return render(request, 'orgs/org-detail-course.html', {
                'org': org,
                'pages': pages,
                'detail_type': 'course',
                'lovestatus': lovestatus
            })
        else:
            print("课程不存在")
            pass
    else:
        print("编号不能为空")
        pass


# 机构详情中的机构简介
def orgs_detail_desc(request, org_id):
    print("传过来的Id:", org_id)
    if org_id:
        org = OrgInfo.objects.filter(id=int(org_id))[0]
        if org:
            # 在返回页面数据的时候，需要返回收藏这个机构的状态，根据状态让模板页面显示收藏还是取消收藏。而不能让页面固定显示收藏。
            lovestatus = False
            # 用户是否登录
            if request.user.is_authenticated():
                love = UserLove.objects.filter(love_man=request.user, love_id=int(org_id), love_type=1,
                                               love_status=True)
                if love:
                    lovestatus = True
            return render(request, 'orgs/org-detail-desc.html', {
                'org': org,
                'detail_type': 'desc',
                'lovestatus': lovestatus
            })
        else:
            print("课程不存在")
            pass
    else:
        print("编号不能为空")
        pass


def orgs_detail_teacher(request, org_id):
    print("传过来的Id:", org_id)
    if org_id:
        org = OrgInfo.objects.filter(id=int(org_id))[0]
        if org:
            # 在返回页面数据的时候，需要返回收藏这个机构的状态，根据状态让模板页面显示收藏还是取消收藏。而不能让页面固定显示收藏。
            lovestatus = False
            # 用户是否登录
            if request.user.is_authenticated():
                love = UserLove.objects.filter(love_man=request.user, love_id=int(org_id), love_type=1,
                                               love_status=True)
                if love:
                    lovestatus = True
            return render(request, 'orgs/org-detail-teachers.html', {
                'org': org,
                'detail_type': 'teacher',
                'lovestatus': lovestatus
            })
        else:
            print("课程不存在")
            pass
    else:
        print("编号不能为空")
        pass


# 获取所有的讲师
def teacher_list(request):
    teacher_list = TeacherInfo.objects.all().order_by('id')

    # 讲师排行榜
    sort_teacher_list = teacher_list.order_by('-love_num')[:3]

    # 根据学习人数和课程数进行排序
    sort = request.GET.get('sort', '')
    if sort:
        teacher_list = teacher_list.order_by('-' + sort)

    # 全局搜索功能
    search_keywords = request.GET.get('keywords', '')
    print("老师列表获取的关键字是:" + search_keywords)
    if search_keywords:
        teacher_list = teacher_list.filter(Q(name__icontains=search_keywords))

    # 分页
    pageNum = request.GET.get('pagenum', '')
    pa = Paginator(teacher_list, 3)  # 每页显示3个
    try:
        pages = pa.page(pageNum)
    except PageNotAnInteger:
        pages = pa.page(1)
    except EmptyPage:
        pages = pa.page(pa.num_pages)

    return render(request, 'orgs/teachers-list.html', {
        'teacher_list': teacher_list,
        'pages': pages,
        'sort_teacher_list': sort_teacher_list,
        'sort': sort,
        'search_keywords': search_keywords
    })


# 讲师详情
def teacher_detail(request, teacher_id):
    if teacher_id:
        teacher = TeacherInfo.objects.filter(id=int(teacher_id))[0]

        # 计算点击量
        teacher.click_num += 1
        teacher.save()

        teacher_list = TeacherInfo.objects.all().order_by('id')
        # 讲师排行榜
        sort_teacher_list = teacher_list.order_by('-love_num')[:3]
        # 获取讲师所有的课程
        teacher_course_list = teacher.courseinfo_set.all().order_by('id')
        # 对讲师的课程进行分页
        pageNum = request.GET.get('pagenum', '')
        pa = Paginator(teacher_course_list, 8)  # 每页显示3个

        # 在返回页面数据的时候，需要返回收藏这个机构的状态，根据状态让模板页面显示收藏还是取消收藏。而不能让页面固定显示收藏。
        loveteacherstatus = False
        loveorgstatus = False
        # 用户是否登录
        if request.user.is_authenticated():
            loveteacher = UserLove.objects.filter(love_man=request.user, love_id=int(teacher_id), love_type=3,
                                                  love_status=True)
            if loveteacher:
                loveteacherstatus = True

            loveorg = UserLove.objects.filter(love_man=request.user, love_id=int(teacher.work_company.id), love_type=1,
                                              love_status=True)
            if loveorg:
                loveorgstatus = True
        try:
            pages = pa.page(pageNum)
        except PageNotAnInteger:
            pages = pa.page(1)
        except EmptyPage:
            pages = pa.page(pa.num_pages)

        if teacher:
            return render(request, 'orgs/teacher-detail.html', {
                'teacher': teacher,
                'teacher_list': teacher_list,
                'sort_teacher_list': sort_teacher_list,
                'pages': pages,
                'loveteacherstatus': loveteacherstatus,
                'loveorgstatus': loveorgstatus
            })
