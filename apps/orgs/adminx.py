import xadmin
from .models import *


# 城市信息
class CityInfoXadmin(object):
    list_display = ['name', 'create_time']  # 管理页面显示列
    model_icon = 'fa fa-gift'


# 机构信息
class OrgInfoXadmin(object):
    list_display = ['image', 'name', 'course_num', 'study_num', 'address', 'desc', 'love_num', 'click_num', 'category',
                    'cityInfo', 'create_time']  # 管理页面显示列
    model_icon = 'fa fa-gift'
    style_fields = {'detail': 'ueditor'}  # 配置富文本编辑器插件


# 教师信息
class TeacherInfoXadmin(object):
    list_display = ['image', 'name', 'work_year', 'work_position', 'click_num', 'age', 'gender', 'love_num']  # 管理页面显示列
    model_icon = 'fa fa-gift'


xadmin.site.register(CityInfo, CityInfoXadmin)

xadmin.site.register(OrgInfo, OrgInfoXadmin)

xadmin.site.register(TeacherInfo, TeacherInfoXadmin)
