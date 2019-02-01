# 注册各个app中的model类


import xadmin
from .models import EmailVerify, BannerInfo

from xadmin import views


# 配置xadmin主题,注册的时候要用到专用的view去注册
class BaseXadminSetting(object):
    enable_themes = True
    use_bootswatch = True


# 配置列表头 列表尾
class CommXadminSetting(object):
    site_title = '谷粒教育后台管理系统'  # 设置页头
    site_footer = '翟氏集团'   # 设置页尾
    menu_style = 'accordion'  # 设置菜单收缩


class BannerInfoXadmin(object):
    list_display = ['image', 'url', 'create_time']  # 管理页面显示列
    search_fields = ['url', 'create_time']  # 管理页面搜索列
    list_filter = ['url', 'create_time']  # 筛选列
    model_icon = 'fa fa-envelope-o'


# 邮箱验证
class EmailVerifyXadmin(object):
    list_display = ['code', 'email', 'send_type', 'create_time']  # 管理页面显示列
    search_fields = ['code', 'email', 'send_type', 'create_time']  # 管理页面搜索列
    list_filter = ['code', 'email', 'send_type', 'create_time']  # 筛选列
    model_icon = 'fa fa-envelope-o'


xadmin.site.register(BannerInfo, BannerInfoXadmin)

xadmin.site.register(EmailVerify, EmailVerifyXadmin)

# 注册主题类
xadmin.site.register(views.BaseAdminView, BaseXadminSetting)

# 注册全局样式
xadmin.site.register(views.CommAdminView, CommXadminSetting)
