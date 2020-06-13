from django.shortcuts import render, redirect
from .models import Article, Author
from django.contrib.auth.models import User
from .forms import ArticleForm


def homepage(request):
    articles = Article.objects.filter(active=True)
    lst_authour = Author.objects.get(id=1)
    return render(request, "article/homepage.html",
        {
            "articles": articles, 
            "lst_authour":lst_authour
        })

def authors(request):
    authors = Author.objects.all()
    return render(request, "article/authors.html", 
        {
            "authors":authors
        }
    )

def users(request):
    context = {}
    context["users_all"] = User.objects.all()
    return render(request, "article/users.html", context)

def article(request, id):
    if request.method == "POST":
        article = Article.objects.get(id=id)
        article.active = False
        article.save()
        return redirect(homepage)

    article = Article.objects.get(id=id)
    return render(
        request,
        "article/article.html",
        {"article": article}
    )

def add_article(request):
    if request.method == "POST":
        article = Article()
        article.title = request.POST.get("title")
        article.text = request.POST.get("text")
        author_id = request.POST.get("author")
        author = Author.objects.get(id=author_id)
        article.author = author
        article.save()
        return render(request, "success.html")

    form = ArticleForm()
    return render(request, "article/add_article.html", {"form": form})