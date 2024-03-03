from django import forms
from bbs.models import *

class BoardForm(forms.ModelForm):
    class Meta:
        model = Board
        fields=['name', 'title', 'contents', 'url', 'email']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: 100%;',
                'placeholder': '이름',
                'label': "이름"
            }),
            'title': forms.TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: 100%;',
                'placeholder': '제목'
            }),
            'contents': forms.TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: 100%;height:300px',
                'placeholder': '내용'
            }),
            'url': forms.TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: 100%;',
                'placeholder': 'Url'
            }),
            'email': forms.TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: 100%;',
                'placeholder': 'Email'
            }),
        }