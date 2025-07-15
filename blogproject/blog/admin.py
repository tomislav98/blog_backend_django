from django.contrib import admin

from .models import (
    User,
    Post,
    Comment,
    Category,
    PostCategory,
    Tag,
    PostTag,
    PostView
)
# Register your models here.


admin.site.register(User)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Category)
admin.site.register(PostCategory)
admin.site.register(Tag)
admin.site.register(PostTag)
admin.site.register(PostView)
