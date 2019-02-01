import xadmin

from .models import *


# 操作用户咨询信息
class UserAskXadmin(object):
    list_display = ['name', 'phone', 'course', 'create_time']  # 管理页面显示列
    model_icon = 'fa fa-envelope-o'


# 用户收藏
class UserLoveXadmin(object):
    list_display = ['love_man', 'love_id', 'love_type', 'love_status', 'create_time']
    model_icon = 'fa fa-heart-o'


# 用户课程
class UserCourseXadmin(object):
    list_display = ['study_man', 'study_course', 'create_time']


# 用户评价
class UserCommentXadmin(object):
    list_display = ['comment_man', 'comment_content', 'comment_course', 'create_time']
    model_icon = 'fa fa-thumbs-o-up'


# 用户消息
class UserMessageXadmin(object):
    list_display = ['message_man', 'message_content', 'message_status', 'create_time']


xadmin.site.register(UserAsk, UserAskXadmin)
xadmin.site.register(UserLove, UserLoveXadmin)
xadmin.site.register(UserCourse, UserCourseXadmin)
xadmin.site.register(UserComment, UserCommentXadmin)
xadmin.site.register(UserMessage, UserMessageXadmin)
