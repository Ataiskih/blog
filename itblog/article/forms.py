from django import forms
from .models import Author, Article, Comment, Tag


class ArticleForm(forms.ModelForm):
        # кастомное добавления столбца в артикл
    tags = forms.CharField(max_length=255, required=False)

    class Meta:     # meta связь с БД валидация
        model = Article
        fields = ['title', 'text', 'picture', 'tags']


class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ['name', 'user']


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ['text']
