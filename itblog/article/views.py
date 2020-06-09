from django.shortcuts import render
from .models import Article, Author
from django.contrib.auth.models import User


def homepage(request):
    articles = Article.objects.all()
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
    users = User.objects.all()
    return render(request, "article/users.html",
        {
            "users":users
        }
    )