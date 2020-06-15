from django.shortcuts import render, redirect
from .models import Article, Author
from django.contrib.auth.models import User
from .forms import *


def homepage(request):
    articles = Article.objects.filter(active=True)      # фильтрация запросов
    lst_authour = Author.objects.get(id=1)
    return render(request, "article/homepage.html",
        {
            "articles": articles, 
            "lst_authour": lst_authour
        }
    )

def profile(request, pk):
    author = Author.objects.get(id=pk)
    return render(request, "article/profile.html", 
        {
            "author": author
        }
    )

def add_author(request):
    if request.method == "POST":
        form = AuthorForm(request.POST)
        if form.is_valid():          # проверкав валидности в html  AuthorForm
            form.save()
            return render(request, "success.html")
    elif request.method == "GET":
        form = AuthorForm()
        context = {}
        context["form"] = form
        return render(request, 'article/add_author.html', context)

def authors(request):
    authors = Author.objects.all()
    return render(request, "article/authors.html", 
        {
            "authors": authors
        }
    )

def users(request):
    context = {}
    context["users_all"] = User.objects.all()
    return render(request, "article/users.html", context)

def article(request, id):
    if request.method == "POST":        # удалание 
        article = Article.objects.get(id=id)        # получение
        article.active = False      # удалание со страницы но не с базы
        article.save()
        return redirect(homepage)
    elif request.method == "GET":
        article = Article.objects.get(id=id)
        return render(
            request,
            "article/article.html",
            {
                "article": article
            }
        )

def edit_article(request,id):       # редактирование статьи
    if request.method == "POST":
        article = Article.objects.get(id=id)    # получение объекта с БД
        form = ArticleForm(request.POST, instance=article)      # редактирование
        if form.is_valid():     # проверкав валидности в html ArticleForm
            form.save()
            return render(request, "success.html")
    elif request.method == "GET":
        article = Article.objects.get(id=id)    # получение объекта с БД
        form = ArticleForm(instance=article)        # передача объекта
        return render(request, "article/add_article.html",
        {
            "form": form
        }
        )

def add_article(request):
    if request.method == "POST":
        form = ArticleForm(request.POST)
        if form.is_valid():     # проверкав валидности в html ArticleForm
            form.save()
            return render(request, "success.html")
    elif request.method == "GET":
        form = ArticleForm()
        return render(request, "article/add_article.html",
            {
                "form": form
            }
        )

def add_comment(request):
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, "success.html")
    elif request.method == "GET":
        form = CommentForm()
        return render(request, "article/add_comment.html",
            {
                "form": form
            }
        )