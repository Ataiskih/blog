from django.shortcuts import render, redirect
from .models import Article, Author, Comment
from django.contrib.auth.models import User
from .forms import ArticleForm, AuthorForm, CommentForm
from django.db.models import Q      # фильтрация


def homepage(request):
    if "key_word" in request.GET:       # поиск GET запросом
        # получение значение по ключу GET запросом
        key = request.GET.get("key_word")
        articles = Article.objects.filter(
            Q(active=True), Q(title__contains=key) | Q(text__contains=key) |
            Q(tag__name__contains=key) | Q(readers__username__contains=key) |
            Q(picture__contains=key) | Q(comments__text__contains=key)
            # , - и | - или
        )
        articles = articles.distinct()
    else:
        # фильтрация запросов и сортировка
        articles = Article.objects.filter(active=True)
    return render(request, "article/homepage.html", {"articles": articles})


def profile(request, pk):
    author = Author.objects.get(id=pk)
    return render(request, "article/profile.html", {"author": author})


def add_author(request):
    if request.method == "POST":
        form = AuthorForm(request.POST)
        if form.is_valid():          # проверкав валидности в html  AuthorForm
            form.save()
            message = "Автор был добавлен успешно!"
            return render(request, "success.html", {"message": message})
    elif request.method == "GET":
        form = AuthorForm()
        context = {}
        context["form"] = form
        return render(request, 'article/add_author.html', context)


def authors(request):
    authors = Author.objects.all()
    return render(request, "article/authors.html", {"authors": authors})


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
        # привязка удаления к кнопке
        elif "add_comment_btn" in request.POST:
            form = CommentForm(request.POST)        # добавление комментария
            if form.is_valid():
                user = request.user
                comment = Comment(
                    user=user,
                    article=article,
                    # получение значений c html
                    text=form.cleaned_data["text"]
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
            # если запрашевыемый поль-ль нет в списке то добавляем его в список
            # авторов -без добавление авторов в ручную
            if not Author.objects.filter(user=request.user):
                author = Author(
                   user=request.user,
                   name=request.user.username
                )
                author.save()
            else:
                author = Author.objects.get(user=request.user)
            # Добавление статьи
            article.author = author
            # получение значений c html:
            article.title = form.cleaned_data["title"]
            article.text = form.cleaned_data["text"]
            article.picture = form.cleaned_data["picture"]
            article.save()
            # настройка тегов
            tags = form.cleaned_data["tags"]
            for tag in tags.split(","):
                obj, created = Tag.objects.get_or_create(name=tag)
                article.tag.add(obj)
            article.save()
            message = "Статья была добавлена успешно!"
            return render(request, "success.html", {"message": message})
    elif request.method == "GET":
        form = ArticleForm()
        message = "Добавить статью"
        return render(
            request,
            "article/add_article.html",
            {"form": form, "message": message})


def edit_article(request, id):       # редактирование статьи
    if request.method == "POST":
        article = Article.objects.get(id=id)    # получение объекта с БД
        # редактирование + добаление файла:
        form = ArticleForm(request.POST, request.FILES, instance=article)
        if form.is_valid():     # проверкав валидности в html ArticleForm
            # Добавление статьи
            # получение значений c html:
            article.title = form.cleaned_data["title"]
            article.text = form.cleaned_data["text"]
            article.picture = form.cleaned_data["picture"]
            article.save()
            # настройка тегов
            tags = form.cleaned_data["tags"]
            for tag in tags.split(","):
                obj, created = Tag.objects.get_or_create(name=tag)
                article.tag.add(obj)
            article.save()
            context = {}        # GET- запрос:
            context["article"] = article
            context["form"] = CommentForm()
            context["message"] = "Статья была изменена успешно!"
            return render(
                request,
                "article/article.html",
                context
            )
    elif request.method == "GET":
        article = Article.objects.get(id=id)    # получение объекта с БД
        form = ArticleForm(instance=article)        # передача объекта
        message = "Редактировать статью"
        return render(
            request, "article/add_article.html",
            {"form": form, "message": message})


def edit_comment(request, id):       # редактирование комментариев
    if request.method == "POST":
        comment = Comment.objects.get(id=id)    # получение объекта с БД
        # редактирование:
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():     # проверкав валидности в html ArticleForm
            form.save()
            message = "Вы изменили комментарий"
            return render(
                request, "success.html", {"message": message})
    elif request.method == "GET":
        comment = Comment.objects.get(id=id)    # получение объекта с БД
        form = CommentForm(instance=comment)        # передача объекта
        message = "Редактировать комментарий"
        return render(
            request, "article/add_comment.html",
            {"form": form, "message": message})


def delete_comment(request, id):
    Comment.objects.get(id=id).delete()
    message = "Вы удалили комментарий!"
    return render(request, "success.html", {"message": message})
