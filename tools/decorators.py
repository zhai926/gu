# 装饰器 【用来控制 用户未登录时，从哪里来 登陆后就会哪里去 】
from django.shortcuts import redirect, reverse
from django.http import JsonResponse


def login_decorator(func):  # 将index的地址传递给func
    # 有参装饰器
    def inner(request, *args, **kwargs):
        if request.user.is_authenticated():
            return func(request, *args, **kwargs)  # fun = index  即func保存了外部index函数的地址
        else:
            if request.is_ajax():
                return JsonResponse({'status': 'nologin', "msg": '未登录'})
            # 拿到目前访问的完整url，不只是路径部分
            url = request.get_full_path()
            ret = redirect(reverse('users:users_login'))
            ret.set_cookie('url', url)
            return ret
    return inner
