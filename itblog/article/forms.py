from django import forms
from .models import *


class ArticleForm(forms.ModelForm):
    class Meta:     # meta связь с БД валидация
        tagss = forms.CharField(max_length=255)
        model = Article
        fields = ['title', 'text', 'picture', 'tags', 'tagss']


class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ['name', 'user']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']