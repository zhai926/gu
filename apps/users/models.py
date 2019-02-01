from django.db import models
# 引入 django 中的 AbstractUser 用来继承
from django.contrib.auth.models import AbstractUser
from datetime import datetime


# Create your models here

# 用户表
class UserProfile(AbstractUser):
    image = models.ImageField(upload_to='users/', max_length=200, verbose_name='用户头像', null=True, blank=True)
    nick_name = models.CharField(max_length=20, verbose_name='用户昵称', null=True, blank=True)
    birthday = models.DateTimeField(verbose_name='生日', null=True, blank=True)
    gender = models.CharField(choices=(('girl', '女'), ('boy', '男')), max_length=10, verbose_name='性别', default='boy')
    address = models.CharField(max_length=200, verbose_name='用户地址', null=True, blank=True)
    phone = models.CharField(max_length=11, verbose_name='手机号', null=True, blank=True)
    is_start = models.BooleanField(default=False, verbose_name="是否激活")  # 是否激活
    create_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    # 如果要把一个类的实例变成str，就需要实现特殊方法__str__()
    def __str__(self):
        return self.username

    # 定义一个方法 用来获取用户未读的消息
    def get_msg_counter(self):
        from operations.models import UserMessage
        counter = UserMessage.objects.filter(message_man=self.id, message_status=False).count()
        return counter

    class Meta:
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name


# 轮播图
class BannerInfo(models.Model):
    image = models.ImageField(upload_to='banner/', max_length=200, verbose_name='轮播图')
    url = models.URLField(default="http://192.168.0.198:8080/", verbose_name='图片链接', max_length=200)
    create_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    def __str__(self):
        return str(self.image)

    class Meta:
        verbose_name = '轮播图信息'
        verbose_name_plural = verbose_name


# 邮箱验证
class EmailVerify(models.Model):
    code = models.CharField(max_length=20, verbose_name='验证码')
    email = models.EmailField(max_length=30, verbose_name='邮箱')
    send_type = models.IntegerField(choices=((1, 'register'), (2, 'forget'), (3, 'change')), verbose_name="验证码类型")
    create_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    def __str__(self):
        return self.code

    class Meta:
        verbose_name = '邮箱验证码'
        verbose_name_plural = verbose_name
