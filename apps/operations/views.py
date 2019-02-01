from django.shortcuts import render
from .forms import *
from django.http import JsonResponse
from orgs.models import *
from courses.models import *
from tools.decorators import login_decorator


# Create your views here.
# 用户咨询
def user_ask(request):
    user_ask_form = UserAskForm(request.POST)
    if user_ask_form.is_valid():
        user_ask_form.save(commit=True)  # 等价于之前的那种原始写法
        return JsonResponse({'status': 'ok', 'msg': '咨询成功'})
    else:
        return JsonResponse({'status': 'fail', 'msg': '咨询失败'})


# 用户收藏
@login_decorator
def user_love(request):
    # 获取前端传过来的参数
    loveId = request.GET.get('loveid', '')
    loveType = request.GET.get('lovetype', '')
    if loveId and loveType:
        obj = None
        # 根据类型和编号判断是机构还是讲师
        if int(loveType) == 1:
            obj = OrgInfo.objects.filter(id=int(loveId))[0]
        if int(loveType) == 2:
            obj = CourseInfo.objects.filter(id=int(loveId))[0]
        if int(loveType) == 3:
            obj = TeacherInfo.objects.filter(id=int(loveId))[0]
        # 查看数据库中有么有记录
        love = UserLove.objects.filter(love_id=int(loveId), love_type=int(loveType), love_man=request.user)
        if love:
            # 如果本来已经存在收藏这个东西的记录，那么我们需要判断收藏的状态，如果收藏状态为真，代表之前收藏过，# 并且现在的页面上应显示的是取消收藏，代表着这次点击是为了取消收藏
            if love[0].love_status:
                love[0].love_status = False
                love[0].save()
                # 收藏数
                obj.love_num -= 1
                obj.save()
                return JsonResponse({'status': 'ok', 'msg': '收藏成功'})
            else:
                # 如果之前没有收藏过这个东西，那么代表着表当中没有这个记录，所以，我们需要先创建这个记录对象，然后把这个记录的状态改为True
                love[0].love_status = True
                love[0].save()
                # 收藏数
                obj.love_num += 1
                obj.save()
                return JsonResponse({'status': 'ok', 'msg': '取消收藏'})
        else:
            a = UserLove()
            a.love_man = request.user
            a.love_id = int(loveId)
            a.love_type = int(loveType)
            a.love_status = True
            a.save()
            # 收藏数
            obj.love_num += 1
            obj.save()
            return JsonResponse({'status': 'ok', 'msg': '取消收藏'})
    else:
        return JsonResponse({'status': 'fail', 'msg': '收藏失败'})


# 用户评论
def user_comment(request):
    user_comment_form = UserCommentForm(request.POST)
    if user_comment_form.is_valid():
        course = user_comment_form.cleaned_data['course']
        content = user_comment_form.cleaned_data['content']
        print("获取的课程编号:", int(course))
        a = UserComment()
        a.comment_man = request.user
        a.comment_content = content
        a.comment_course_id = course
        a.save()
        return JsonResponse({'status': 'ok', 'msg': '评论成功'})
    else:
        return JsonResponse({'status': 'fail', 'msg': '评论失败'})


# 删除收藏
def user_deletelove(request):
    # 获取前端传过来的参数
    loveId = request.GET.get('loveid', '')
    loveType = request.GET.get('lovetype', '')
    print("获取的数据:" + loveId + ",loveType:" + loveType)
    if loveId and loveType:
        # 查看数据库中有么有记录
        love = UserLove.objects.filter(love_id=int(loveId), love_type=int(loveType), love_man=request.user,
                                       love_status=True)
        if love:
            love[0].love_status = False
            love[0].save()
            return JsonResponse({'status': 'ok', 'msg': '删除成功'})
        else:
            return JsonResponse({'status': 'fail', 'msg': '删除失败'})
    else:
        return JsonResponse({'status': 'fail', 'msg': '删除失败'})
