from django.contrib import admin
from article.models import Article, Author

admin.site.register(Article)
admin.site.register(Author)