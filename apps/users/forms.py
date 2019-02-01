from django import forms  # Form :一系列Field对象的集合，负责验证和显示HTML元素
from captcha.fields import CaptchaField
from .models import UserProfile, EmailVerify


#  注册表单类
class UsersRegisterForms(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True, min_length=6, max_length=20, error_messages={
        'required': '密码不能为空',
        'min_length': '密码的最小长度为6位',
        'max_length': '密码的最大长度为20位'
    })
    captcha = CaptchaField()  # 验证码


# 用户登录
class UserLoginForms(forms.Form):
    username = forms.CharField(required=True, error_messages={
        'required': '用户名不能为空'
    })
    password = forms.CharField(required=True, min_length=6, max_length=20, error_messages={
        'required': '密码不能为空',
        'min_length': '密码的最小长度为6位',
        'max_length': '密码的最大长度为20位'
    })


# 忘记密码
class UserForgetPwdForms(forms.Form):
    email = forms.EmailField(required=True)
    captcha = CaptchaField()  # 验证码


# 忘记密码之点击邮箱链接
class UserResetForms(forms.Form):
    password = forms.CharField(required=True, min_length=6, max_length=20, error_messages={
        'required': '密码不能为空',
        'min_length': '密码的最小长度为6位',
        'max_length': '密码的最大长度为20位'
    })
    password1 = forms.CharField(required=True, min_length=6, max_length=20, error_messages={
        'required': '密码不能为空',
        'min_length': '密码的最小长度为6位',
        'max_length': '密码的最大长度为20位'
    })


# 修改个人头像
class UserChangeImageForms(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['image']


# 修改个人信息
class UserChangeInfoForms(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['nick_name', 'birthday', 'gender', 'address', 'phone']


# 修改个人邮箱
class UserChangeEmailForms(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['email']


# 修改个人邮箱
class UserChangeResSetEmailForms(forms.ModelForm):
    class Meta:
        model = EmailVerify
        fields = ['email', 'code']
