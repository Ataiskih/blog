from django import forms
from .models import *


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'text', 'author']


class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ['name', 'user']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['article', 'text', 'user']