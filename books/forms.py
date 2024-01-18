from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import UserProfile, Book
import uuid
from django.contrib.auth.forms import PasswordChangeForm


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
    # phone_number = forms.CharField(label='手机号码', max_length=11)
    USER_TYPE_CHOICES = {
        (0, '用户'),
        (1, '管理员'),
    }
    user_type = forms.ChoiceField(choices=USER_TYPE_CHOICES, label='用户类型')

    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'user_type')

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
            user_type = self.cleaned_data['user_type']
            UserProfile.objects.create(user=user, library_id=library_id,
                                       membership_type=user_type)
        return user

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise ValidationError('用户已存在')
        return username


class CustomPasswordChangeFrom(PasswordChangeForm):
    old_password = forms.CharField(label='旧密码', widget=forms.PasswordInput)
    new_password1 = forms.CharField(label='新密码', widget=forms.PasswordInput)
    new_password2 = forms.CharField(label='确认新密码', widget=forms.PasswordInput)


class UserProfileForm(forms.ModelForm):
    # 用户资料表单
    first_name = forms.CharField(max_length=30, label='名字')
    last_name = forms.CharField(max_length=30, label='姓氏')
    email = forms.EmailField()

    class Meta:
        model = UserProfile
        fields = ['address', 'phone_number']


class BookForm(forms.ModelForm):
    # 添加图书
    class Meta:
        model = Book
        fields = ['title', 'author', 'isbn', 'publication_date', 'category', 'in_stock']
