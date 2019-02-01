from django.shortcuts import render
from .models import *
from django.core.paginator import PageNotAnInteger, Paginator, EmptyPage  # 分页
from operations.models import UserLove, UserCourse
from django.db.models import Q
# from django.contrib.auth.decorators import login_required  #登录
# Create your views here.
from tools.decorators import login_decorator   # 导入我们自己的装饰器
# 获取所有的课程
def course_list(request):
    course_all_list = CourseInfo.objects.all().order_by('id')  # 获取所有的课程
    recommend_courses = course_all_list.order_by('-study_time')[:3]

    sort = request.GET.get('sort', '')
    if sort:
        course_all_list = course_all_list.order_by('-' + sort)

    # 全局搜索功能
    search_keywords = request.GET.get('keywords', '')
    if search_keywords:
        course_all_list = course_all_list.filter(Q(name__icontains=search_keywords)| Q(desc__icontains=search_keywords)|Q(
                detail__icontains=search_keywords))

    print("课程列表获取的关键字是:" + search_keywords)
    # 分页
    pageNum = request.GET.get('pagenum', '')
    pa = Paginator(course_all_list, 9)  # 每页显示3个
    try:
        pages = pa.page(pageNum)
    except PageNotAnInteger:
        pages = pa.page(1)
    except EmptyPage:
        pages = pa.page(pa.num_pages)

    return render(request, 'course/course-list.html', {
        'course_all_list': course_all_list,
        'recommend_courses': recommend_courses,
        'pages': pages,
        'sort': sort,
        'search_keywords':search_keywords
    })


# 课程详情
def course_detail(request, course_id):
    print("传过来的编号:" + course_id)
    if course_id:
        print("传过来的编号:" + course_id)
        course = CourseInfo.objects.filter(id=int(course_id))[0]

        # 计算点击量
        course.click_num += 1
        course.save()

        related_course = CourseInfo.objects.filter(category=course.category).exclude(id=int(course_id))[:3]  # 相关课程
        # 在返回页面数据的时候，需要返回收藏这个机构的状态，根据状态让模板页面显示收藏还是取消收藏。而不能让页面固定显示收藏。
        lovestatus1 = False
        lovestatus2 = False
        # 用户是否登录
        if request.user.is_authenticated():
            lovecourse = UserLove.objects.filter(love_man=request.user, love_id=int(course_id), love_type=2,
                                                 love_status=True)
            if lovecourse:
                lovestatus1 = True
            loveorg = UserLove.objects.filter(love_man=request.user, love_id=int(course.orgInfo.id), love_type=1,
                                              love_status=True)
            if loveorg:
                lovestatus2 = True

        return render(request, 'course/course-detail.html', {
            'course': course,
            'related_course': related_course,
            'lovestatus1': lovestatus1,
            'lovestatus2': lovestatus2
        })


# 课程资源
@login_decorator
def course_video(request, course_id):
    if course_id:
        course = CourseInfo.objects.filter(id=int(course_id))[0]
        # 判断当前用户是否学习过当前课程,没有学习就讲其加入到数据库
        user_course_list = UserCourse.objects.filter(study_course=course, study_man=request.user)

        if not user_course_list:
            a = UserCourse()
            a.study_man = request.user
            a.study_course = course
            a.save()
            # 课程的学习计算
            course.study_num += 1
            course.save()
            # ----------------------------------机构学习人数计算 ------------------------------
            # 第一步：从学习课程的表当中查找当前这个人学习的所有的课程,出去新学的这门课程
            user_course_list = UserCourse.objects.filter(study_man=request.user).exclude(study_course=course)
            course_list = [usercourse.study_course for usercourse in user_course_list]
            # 第二步：根据拿到的所有课程，找到这个用户学过课程的机构
            org_list = list(set([course1.orgInfo for course1 in course_list]))
            # 第三步：判断当前所学的课程机构，是不是在这个用户之前所学的机构当中，如果不在，那么机构的学习人数+1
            if course.orgInfo not in org_list:
                course.orgInfo.study_num += 1
                course.orgInfo.save()
            # ----------------------------------机构学习人数计算 ------------------------------

        # 学过该课的同学还学过什么课程
        # 第一步：我们需要从中间表用户课程表当中找到学过该课的所有对象
        user_course_list = UserCourse.objects.filter(study_course=course)

        # 第二步：根据找到的用户学习课程列表，遍历拿到所有学习过这门课程的用户列表
        user_list = [usercourse.study_man for usercourse in user_course_list]

        # 第三步：再根据找到的用户，从中间用户学习课程表当中，找到所有用户学习其它课程的 整个对象,需要用到exclude去除当前学过的这个课程对象
        user_course_list = UserCourse.objects.filter(study_man__in=user_list).exclude(study_course=course)

        # 第四步：从获取到的用户课程列表当中，拿到我们需要的其它课程
        course_list = list(set([usercourse.study_course for usercourse in user_course_list]))

        return render(request, 'course/course-video.html', {
            'course': course,
            'course_list': course_list
        })


# 评论
def course_comment(request, course_id):
    if course_id:
        course = CourseInfo.objects.filter(id=course_id)[0]
        all_comment_lsit = course.usercomment_set.all()[:10]

        # 学过该课的同学还学过什么课程
        # 第一步：我们需要从中间表用户课程表当中找到学过该课的所有对象
        user_course_list = UserCourse.objects.filter(study_course=course)

        # 第二步：根据找到的用户学习课程列表，遍历拿到所有学习过这门课程的用户列表
        user_list = [usercourse.study_man for usercourse in user_course_list]

        # 第三步：再根据找到的用户，从中间用户学习课程表当中，找到所有用户学习其它课程的 整个对象,需要用到exclude去除当前学过的这个课程对象
        user_course_list = UserCourse.objects.filter(study_man__in=user_list).exclude(study_course=course)

        # 第四步：从获取到的用户课程列表当中，拿到我们需要的其它课程
        course_list = list(set([usercourse.study_course for usercourse in user_course_list]))

        return render(request, 'course/course-comment.html', {
            'course': course,
            'all_comment_lsit': all_comment_lsit,
            'course_list': course_list
        })
