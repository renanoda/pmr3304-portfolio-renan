from .permissions import can_manage_posts
from django.contrib import admin
from .models import Category, Comment, Post

admin.site.register(Category)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return can_manage_posts(request.user)

    def has_change_permission(self, request, obj=None):
        return can_manage_posts(request.user)

    def has_delete_permission(self, request, obj=None):
        return can_manage_posts(request.user)


admin.site.register(Comment)

