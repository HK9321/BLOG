from django import forms
from user.models import User


class RegisterForm(forms.Form):
    """注册表单"""
    username = forms.CharField(
        min_length=3,
        max_length=10,
        required=True,
        error_messages={
        'required': "用户名不能为空",
        'min_length':'用户名不得少于三个字符!',
    })
    email = forms.EmailField(
        required=True,
        error_messages={'required' :"邮箱不能为空", 'invalid':"邮箱格式错误"})
    password_1 = forms.CharField(error_messages={'required': "密码不能为空"})
    password_2 = forms.CharField(error_messages={'required': "验证密码必须与密码一致"})
    icon = forms.FileField(error_messages={'required':"请选择你的用户头像"})

    def clean_username(self):
        username = self.cleaned_data['username']
        is_exist = User.objects.filter(username=username).exists()
        if is_exist:
            raise forms.ValidationError(u'用户名已存在')
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        is_exist = User.objects.filter(email=email).exists()
        if is_exist:
            raise forms.ValidationError(u"这个邮箱已被注册哦,请换个邮箱！")
        return email

    def clean_password_2(self):
        password_1 = self.cleaned_data.get("password_1")
        password_2 = self.cleaned_data.get("password_2")
        if password_1 and password_2 and password_1 != password_2:
            raise forms.ValidationError('密码验证失败')
        return password_2


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()