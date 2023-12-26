from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import UserProfile
import uuid


def generate_library_id():
    """
    uuid4() 它生成基于随机数的全球唯一标识符。
    :return:
    """
    return str(uuid.uuid4())


class UserRegistrationForm(forms.ModelForm):
    """
    用于创建一个新的 User 对象。它有两个密码字段用于密码和确认密码，并且还有一个手机号码字段。
    """
    password = forms.CharField(label='密码', widget=forms.PasswordInput)
    password2 = forms.CharField(label='确认密码', widget=forms.PasswordInput)
    phone_number = forms.CharField(label='手机号码', max_length=11)

    class Meta:
        model = User
        fields = ('username', 'password', 'password2')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise ValidationError('密码不一致')
        return cd['password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
            library_id = generate_library_id()
            UserProfile.objects.create(user=user, phone_number=self.cleaned_data['phone_number'], library_id=library_id)
        return user

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise ValidationError('用户已存在')
        return username
