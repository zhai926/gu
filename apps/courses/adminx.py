import xadmin
from .models import *


class CourseInfoXadmin(object):
    list_display = ['image', 'name', 'study_time', 'study_num', 'level', 'love_num', 'click_num', 'desc', 'detail',
                    'category', 'course_notice',
                    'course_need', 'teacher_tell', 'orgInfo', 'teacherInfo', 'is_banner', 'create_time']
    model_icon = 'fa fa-bars'


# 章节信息
class LessonInfoXadmin(object):
    list_display = ['name', 'courseInfo', 'create_time']
    model_icon = 'fa fa-group'


# 视频信息
class VideoInfoXadmin(object):
    list_display = ['name', 'study_time', 'url', 'lessonInfo']


# 资源信息
class SourceInfoXadmin(object):
    list_display = ['name', 'down_load', 'courseInfo', 'create_time']


xadmin.site.register(CourseInfo, CourseInfoXadmin)

xadmin.site.register(LessonInfo, LessonInfoXadmin)

xadmin.site.register(VideoInfo, VideoInfoXadmin)

xadmin.site.register(SourceInfo, SourceInfoXadmin)
