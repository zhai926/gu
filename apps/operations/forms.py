from django import forms
from .models import *
import re


# 用户咨询
# forms.ModelForm 要 比 forms.Form 的功能更强大
class UserAskForm(forms.ModelForm):
    class Meta:
        model = UserAsk
        fields = ['name', 'course', 'phone']
        # exclude = ['add_time']
        # 如果用到了所有的字段
        # fields = '__all__'

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        print("输入的电话:", phone)
        com = re.compile('^1([358][0-9]|4[579]|66|7[0135678]|9[89])[0-9]{8}$')
        if com.match(phone):
            return phone
        else:
            raise forms.ValidationError('手机号码不合法')


# 用户评论
class UserCommentForm(forms.Form):
    course = forms.IntegerField(required=True)
    content = forms.CharField(required=True, min_length=1, max_length=300)
