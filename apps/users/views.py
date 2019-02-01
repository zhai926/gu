from django.shortcuts import render, reverse, redirect, HttpResponse
from users.forms import *
from .models import *
from django.db.models import Q
from django.contrib.auth import logout, login, authenticate
from tools.send_mail_tool import send_email_code
from courses.models import *
from django.http.response import JsonResponse
from orgs.models import *
from operations.models import *
from django.core.paginator import PageNotAnInteger, Paginator, EmptyPage  # 分页


# from django.views.generic import View   # 可以将 方法更改为 类

# Q对象(django.db.models.Q)可以对关键字参数进行封装，从而更好地应用多个查询。可以组合使用 &（and）,|（or），~（not）操作符，
# 当一个操作符是用于两个Q的对象,它产生一个新的Q对象。

# Create your views here.

# 首页
def index(request):
    all_banners = BannerInfo.objects.all().order_by('-create_time')[:5]
    banner_courses = CourseInfo.objects.filter(is_banner=True)[:3]
    all_courses = CourseInfo.objects.filter(is_banner=False)[:6]
    all_orgs = OrgInfo.objects.all()[:15]
    return render(request, 'index.html', {
        'all_banners': all_banners,
        'banner_courses': banner_courses,
        'all_courses': all_courses,
        'all_orgs': all_orgs
    })


# 注册
def users_register(request):
    if request.method == 'GET':
        # 此处的forms只是为了使用验证码
        users_register_form = UsersRegisterForms()
        return render(request, 'users/register.html', {
            'users_register_form': users_register_form
        })
    else:
        # pass  # Python pass是空语句，是为了保持程序结构的完整性。 pass 不做任何事情，一般用做占位语句。
        users_register_form = UsersRegisterForms(request.POST)  # 用户提交表单，我们通过request.post拿到数据，然后封装到Form（数据）里面
        if users_register_form.is_valid():  # obj.is_valid方法，来检查用户输入的内容，跟Form（）定义的，是否匹配。
            email = users_register_form.cleaned_data['email']
            password = users_register_form.cleaned_data['password']
            # 根据邮箱或者用户名去获取用户对象
            user_list = UserProfile.objects.filter(Q(username=email) | Q(email=email))
            if user_list:
                return render(request, 'users/register.html', {
                    'msg': '用户已存在'
                })
            else:
                # 注册
                user = UserProfile()
                user.email = email
                user.username = email
                user.set_password(password)
                user.save(user)
                # 发送邮箱验证码,通知用户激活
                send_email_code(email, 1)
                return HttpResponse('邮件已发送到你的邮箱，请尽快激活！否则无法登陆!')
                # return redirect(reverse('index'))  # 重定向
        else:
            return render(request, 'users/register.html', {
                'users_register_form': users_register_form
            })


# 登录
def users_login(request):
    if request.method == 'GET':
        return render(request, 'users/login.html')
    else:
        users_login_form = UserLoginForms(request.POST)
        if users_login_form.is_valid():
            username = users_login_form.cleaned_data['username']
            password = users_login_form.cleaned_data['password']
            print("1获取的用户名:", username + "----密码:", password)
            # 验证
            user = authenticate(username=username, password=password)
            if user:
                print("2获取的用户名:", username + "密码:", password)
                # 判断是否激活
                if user.is_start:
                    login(request, user)  # 登录

                    # 记录用户信息【日志】
                    a = UserMessage()
                    a.message_man = int(user.id)
                    a.message_content = '欢迎！登录成功'
                    a.save()

                    # 获取 url
                    url = request.COOKIES.get('url', '/')
                    ret = redirect(url)
                    ret.delete_cookie('url')  # 避免出现第二次未登录的一个操作 进到了第一次未登录的操作
                    return redirect(url)
                else:
                    return HttpResponse('未激活！请去邮箱进行激活再使用...')
            else:
                return render(request, 'users/login.html', {
                    'msg': '用户名或密码不正确',
                    'username': username
                })
        else:
            return render(request, 'users/login.html', {
                'users_login_form': users_login_form

            })


# 登出
def users_logout(request):
    logout(request)
    return redirect(reverse('index'))


# 激活
def users_active(request, code):
    if code:
        print('获取的验证码:', code)
        email_ver_list = EmailVerify.objects.filter(code=code)  # 根据code 获取
        if email_ver_list:
            email_ver = email_ver_list[0]
            email = email_ver.email  # 获取 email
            # 根据邮箱查询 用户
            user_list = UserProfile.objects.filter(email=email)
            if user_list:
                user = user_list[0]
                user.is_start = True
                user.save()
                return redirect(reverse('users:users_login'))
            else:
                print('激活失败.....')
                pass

        else:
            print('激活失败.....')
            pass
    else:
        print('激活失败.....')
        pass


# 忘记密码
def users_forget(request):
    if request.method == 'GET':
        # 此处的forms只是为了使用验证码
        users_forget_form = UserForgetPwdForms()
        return render(request, 'users/forgetpwd.html', {
            'users_forget_form': users_forget_form
        })
    else:
        users_forget_form = UserForgetPwdForms(request.POST)
        if users_forget_form.is_valid():
            email = users_forget_form.cleaned_data['email']
            users_list = UserProfile.objects.filter(email=email)
            if users_list:
                send_email_code(email, 2)  # 发送邮件
                return HttpResponse('邮件已发送到你的邮箱！请尽快去重置你的密码！')
            else:
                return render(request, 'users/forgetpwd.html', {
                    'msg': '该邮箱不存在',
                    'users_forget_form': users_forget_form
                })
        else:
            return render(request, 'users/forgetpwd.html', {
                'users_forget_form': users_forget_form
            })


# 忘记密码之点击邮箱链接
def users_reset(request, code):
    if code:
        if request.method == 'GET':
            return render(request, 'users/password_reset.html', {
                'code': code
            })
        else:
            user_reset_form = UserResetForms(request.POST)
            if user_reset_form.is_valid():
                password = user_reset_form.cleaned_data['password']
                password1 = user_reset_form.cleaned_data['password1']
                if password == password1:
                    email_ver_list = EmailVerify.objects.filter(code=code)  # 根据code 获取
                    if email_ver_list:
                        email_ver = email_ver_list[0]
                        email = email_ver.email  # 获取 email
                        # 根据邮箱查询 用户
                        user_list = UserProfile.objects.filter(email=email)
                        if user_list:
                            user = user_list[0]
                            user.set_password(password1)
                            user.save()
                            return redirect(reverse('users:users_login'))
                        else:
                            pass
                    else:
                        pass
                else:
                    return render(request, 'users/password_reset.html', {
                        'msg': '两次密码不一致！',
                        'code': code
                    })
            else:
                return render(request, 'users/password_reset.html', {
                    'user_reset_form': user_reset_form,
                    'code': code
                })


# 进到个人中心
def users_info(request):
    return render(request, 'users/usercenter-info.html')


# 修改头像
def users_change_image(request):
    # instance  指明实例是什么，做修改的时候，我们需要知道是给哪个对象实例进行修改
    # 如果不指明，那么就会被当作创建对象去执行，而我们只有一个图片，就一定会报错。
    users_change_image_form = UserChangeImageForms(request.POST, request.FILES, instance=request.user)
    if users_change_image_form.is_valid():
        # 记录用户信息【日志】
        a = UserMessage()
        a.message_man = request.user.id
        a.message_content = '进到修改头像'
        a.save()
        users_change_image_form.save(commit=True)
        return JsonResponse({'status': 'ok'})
    else:
        return JsonResponse({'status': 'fail'})


# 修改个人信息
def users_change_info(request):
    user_change_info_forms = UserChangeInfoForms(request.POST, instance=request.user)
    if user_change_info_forms.is_valid():
        user_change_info_forms.save(commit=True)
        return JsonResponse({'status': 'ok', 'msg': '修改成功'})
    else:
        return JsonResponse({'status': 'fail', 'msg': '修改失败'})


# 修改个人邮箱
def users_change_reset_email(request):
    user_change_email_reset_forms = UserChangeResSetEmailForms(request.POST)
    if user_change_email_reset_forms.is_valid():
        email = user_change_email_reset_forms.cleaned_data['email']
        code = user_change_email_reset_forms.cleaned_data['code']
        email_ver_list = EmailVerify.objects.filter(code=code, email=email)
        if email_ver_list:
            email_ver = email_ver_list[0]
            if (datetime.now() - email_ver.add_time).seconds < 60:
                request.user.username = email
                request.user.email = email
                request.user.save()

                a = UserMessage()
                a.message_man = request.user.id
                a.message_content = '修改了个人的邮箱'
                a.save()

                return JsonResponse({'status': 'ok', 'msg': '邮箱修改成功'})
            else:
                return JsonResponse({'status': 'fail', 'msg': '验证码失效，请重新发送验证码'})
        else:
            return JsonResponse({'status': 'fail', 'msg': '邮箱或者验证码有误'})
    else:
        return JsonResponse({'status': 'fail', 'msg': '邮箱或者验证码不合法'})


# 修改个人邮箱并发送邮箱
def users_change_email(request):
    user_change_email_forms = UserChangeEmailForms(request.POST)
    if user_change_email_forms.is_valid():
        # 判断这个邮箱是否使用过 是否合法
        email = user_change_email_forms.cleaned_data['email']
        print("1获取的邮箱是:", email)
        user_list = UserProfile.objects.filter(Q(email=email) | Q(username=email))
        if user_list:
            print("2获取的邮箱是:", email)
            return JsonResponse({'status': 'fail', 'msg': '该邮箱已在使用中'})
        else:
            # 限制邮箱的发送时间 避免用户狂点击
            email_ver_list = EmailVerify.objects.filter(send_type=3, email=email)
            if email_ver_list:
                email_ver = email_ver_list.order_by('-add_time')[0]
                # 判断当前时间和最近发送的验证码添加时间之差
                if (datetime.now() - email_ver.add_time).seconds > 60:
                    # 如果我们重新发送了新的验证码，那么以前最近发的就被清了
                    send_email_code(email, 3)
                    email_ver.delete()
                    return JsonResponse({'status': 'ok', 'msg': '邮件已发送到你邮箱,请尽快请查看'})
    else:
        return JsonResponse({'status': 'fail', 'msg': '邮箱格式有误'})


# 我的课程
def user_course(request):
    usercourse_list = request.user.usercourse_set.all()
    course_list = [usercourse.study_course for usercourse in usercourse_list]
    return render(request, 'users/usercenter-mycourse.html', {
        'course_list': course_list
    })


# 我的收藏之机构
def user_love_org(request):
    love_org_list = UserLove.objects.filter(love_type=1, love_man=request.user, love_status=True)
    org_ids = [love_org.love_id for love_org in love_org_list]
    orgs_list = OrgInfo.objects.filter(id__in=org_ids)
    return render(request, 'users/usercenter-fav-org.html', {
        'love_org_list': love_org_list,
        'orgs_list': orgs_list
    })


# 我的收藏之课程
def user_love_course(request):
    love_course_list = UserLove.objects.filter(love_type=2, love_man=request.user, love_status=True)
    course_ids = [love_course.love_id for love_course in love_course_list]
    course_list = CourseInfo.objects.filter(id__in=course_ids)
    return render(request, 'users/usercenter-fav-course.html', {
        'course_list': course_list
    })


# 我的收藏之教师
def user_love_teacher(request):
    love_teacher_list = UserLove.objects.filter(love_type=3, love_man=request.user, love_status=True)
    teacher_ids = [love_teacher.love_id for love_teacher in love_teacher_list]
    teacher_list = TeacherInfo.objects.filter(id__in=teacher_ids)
    return render(request, 'users/usercenter-fav-teacher.html', {
        'teacher_list': teacher_list
    })


# 我的信息
def user_message(request):
    user_message_list = UserMessage.objects.filter(message_man=request.user.id).order_by('id')
    # 分页
    pageNum = request.GET.get('pagenum', '')
    pa = Paginator(user_message_list, 10)  # 每页显示10个
    try:
        pages = pa.page(pageNum)
    except PageNotAnInteger:
        pages = pa.page(1)
    except EmptyPage:
        pages = pa.page(pa.num_pages)
    return render(request, 'users/usercenter-message.html', {
        'user_message_list': user_message_list,
        'pages': pages
    })


# 更改我的消息的 读取状态
def update_user_message_status(request):
    messageId = request.GET.get('messageId', '')
    print("获取的编号是:", messageId)
    if messageId:
        message = UserMessage.objects.filter(id=int(messageId))[0]
        if message:
            message.message_status = True
            message.save()
            return JsonResponse({"status": 'ok', 'msg': '已读'})
        else:
            return JsonResponse({"status": 'fail', 'msg': '未读'})
    else:
        return JsonResponse({"status": 'fail', 'msg': '参数有误'})


# 报错跳转
def handler_404(request):
    return render(request, 'handler_404.html')


def handler_500(request):
    return render(request, 'handler_500.html')
