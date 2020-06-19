from django.contrib import admin
from article.models import *

admin.site.register(Article)
admin.site.register(Author)
admin.site.register(Comment)
admin.site.register(Tag)
