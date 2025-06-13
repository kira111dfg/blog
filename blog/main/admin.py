
from django.contrib import admin

from .models import Category, LikeDislike, Plant, Tag,Comment

admin.site.register(Plant)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Comment)
admin.site.register(LikeDislike)