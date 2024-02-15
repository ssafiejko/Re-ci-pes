from django.contrib import admin

# Register your models here.
from .models import Recipe, Topic, Comment, User
admin.site.register(Recipe)
admin.site.register(Topic)
admin.site.register(Comment)
admin.site.register(User)

