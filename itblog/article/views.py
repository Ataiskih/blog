from django.shortcuts import render, redirect
from .models import Article, Author, Comment
from django.contrib.auth.models import User
from .forms import *


def homepage(request):
    if request.method == "POST":        # поиск POST запросом
        key = request.POST.get("key_word")
        articles = Article.objects.filter(active=True).filter(
            title__contains=key) | Article.objects.filter(active=True).filter(
                text__contains=key) | Article.objects.filter(active=True).filter(
                    tags__name__contains=key) | Article.objects.filter(active=True).filter(
                        readers__username__contains=key) | Article.objects.filter(active=True).filter(
                            picture__contains=key) | Article.objects.filter(active=True).filter(
                                comments__text__contains=key)
        articles = articles.distinct()
    else:       #GET
        if "key_word" in request.GET:       # поиск GET запросом
            key = request.GET.get("key_word")   # получение значение по ключу GET запросом
            articles = Article.objects.filter(active=True).filter(
                title__contains=key) | Article.objects.filter(active=True).filter(
                    text__contains=key) | Article.objects.filter(active=True).filter(
                        tags__name__contains=key) | Article.objects.filter(active=True).filter(
                            readers__username__contains=key) | Article.objects.filter(active=True).filter(
                                picture__contains=key) | Article.objects.filter(active=True).filter(
                                    comments__text__contains=key)       
            articles = articles.distinct()
        else:
            articles = Article.objects.filter(active=True)     # фильтрация запросов и сортировка
    return render(request, "article/homepage.html",
        {
            "articles": articles
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
    article = Article.objects.get(id=id)     # получение
    article.views += 1
    user = request.user     # получение пользователя
    if not user.is_anonymous:       # если не анонимный
        article.readers.add(user)       # добавление пользователя в читатели
    article.save()  
    if request.method == "POST":        # удалание статьи
        if "delete_btn" in request.POST:        # привязка удаления к кнопке  
            article.active = False      # удалание со страницы но не с базы
            article.save()
            return redirect(homepage)
        elif "add_comment_btn" in request.POST:        # привязка удаления к кнопке
            form = CommentForm(request.POST)        # добавление комментария
            if form.is_valid():
                user  = request.user
                comment = Comment(
                    user=user,
                    article=article,
                    text=form.cleaned_data["text"]      # получение значений
                )
                comment.save()

    context = {}        # GET- запрос:
    context["article"] = Article.objects.get(id=id)
    context["form"] = CommentForm()
    return render(
            request, "article/article.html", context
        )

def add_article(request):       # добавление статьи
    if request.method == "POST":
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():     # проверкав валидности в html ArticleForm
            article = Article()
            # Запрашиваемый пользователь становится автором
            if not Author.objects.filter(user=request.user):        # если запрашевыемый поль-ль нет в списке то добавляем его в список авторов -без добавление авторов в ручную
                author = Author(
                    user = request.user,
                    name = request.user.username
                )
                author.save()
            else:
                author = Author.objects.get(user=request.user)
            # Добавление статьи 
            article.author = author
            article.title = form.cleaned_data["title"]
            article.text = form.cleaned_data["text"]
            article.picture = form.cleaned_data["picture"]
            article.save()
            # настройка тегов
            tagss = form.cleaned_data["tagss"]
            for tag in tagss.split(","):
                obj, created = Tag.objects.get_or_create(name=tag)
                article.tag.add(obj)
            article.save()
            return render(request, "success.html")
    elif request.method == "GET":
        form = ArticleForm()
        message = "Добавить статью"
        return render(request, "article/add_article.html",
            {
                "form": form,
                "message": message
            }
        )

def edit_article(request,id):       # редактирование статьи
    if request.method == "POST":
        article = Article.objects.get(id=id)    # получение объекта с БД
        form = ArticleForm(request.POST, request.FILES, instance=article)      # редактирование + добаление файла
        if form.is_valid():     # проверкав валидности в html ArticleForm
            form.save()
            return render(request, "success.html")
    elif request.method == "GET":
        article = Article.objects.get(id=id)    # получение объекта с БД
        form = ArticleForm(instance=article)        # передача объекта
        message = "Редактировать статью"
        return render(request, "article/add_article.html",
            {
                "form": form,
                "message": message
            }
        )

def edit_comment(request,id):       # редактирование комментариев
    if request.method == "POST":
        comment = Comment.objects.get(id=id)    # получение объекта с БД
        form = CommentForm(request.POST, instance=comment)      # редактирование
        if form.is_valid():     # проверкав валидности в html ArticleForm
            form.save()
            return render(request, "success.html")
    elif request.method == "GET":
        comment = Comment.objects.get(id=id)    # получение объекта с БД
        form = CommentForm(instance=comment)        # передача объекта
        message = "Редактировать комментарий"
        return render(request, "article/add_comment.html",
            {
                "form": form,
                "message": message
            }
        )

def delete_comment(request, id):
    Comment.objects.get(id=id).delete()
    return render(request, "success.html")
