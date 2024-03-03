from django import forms
from account.models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import SetPasswordForm

class UserForm(UserCreationForm):
    email = forms.EmailField(label="이메일")

    class meta:
        model=User
        fields = ("username", "password1", "password2", "email")

class RecoveryIdForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput,)
    email = forms.EmailField(widget=forms.EmailInput,)

    class Meta:
        fields = ['name', 'email']

    def __init__(self, *args, **kwargs):
        super(RecoveryIdForm, self).__init__(*args, **kwargs)
        self.fields['name'].label = '이름'
        self.fields['name'].widget.attrs.update({
            'class': 'form-control',
            'id': 'form_name',
        })
        self.fields['email'].label = '이메일'
        self.fields['email'].widget.attrs.update({
            'class': 'form-control',
            'id': 'form_email' 
        })

class RecoveryPwForm(forms.Form):
    id = forms.CharField(
        widget=forms.TextInput,)
    username = forms.CharField(
        widget=forms.TextInput,)
    email = forms.EmailField(
        widget=forms.EmailInput,)

    class Meta:
        fields = ['id', 'username', 'email']

    def __init__(self, *args, **kwargs):
        super(RecoveryPwForm, self).__init__(*args, **kwargs)
        self.fields['id'].label = '아이디'
        self.fields['id'].widget.attrs.update({
            'class': 'form-control',
            'id': 'pw_form_id',
        })
        self.fields['username'].label = '이름'
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'id': 'pw_form_name',
        })
        self.fields['email'].label = '이메일'
        self.fields['email'].widget.attrs.update({
            'class': 'form-control',
            'id': 'pw_form_email',
        })

class CustomSetPasswordForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super(CustomSetPasswordForm, self).__init__(*args, **kwargs)
        self.fields['new_password1'].label = '새 비밀번호'
        self.fields['new_password1'].widget.attrs.update({
            'class': 'form-control',
        })
        self.fields['new_password2'].label = '새 비밀번호 확인'
        self.fields['new_password2'].widget.attrs.update({
            'class': 'form-control',
        })

def save(self, commit=True):
    user = super(UserForm, self).save(commit=False)
    # user.level = '2'
    # user.department = '컴퓨터공학부'
    user.is_active = False
    user.save()

    