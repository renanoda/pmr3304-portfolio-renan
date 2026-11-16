from django.conf import settings


def can_manage_posts(user):
    return user.is_active and user.is_superuser and user.get_username() == settings.PORTFOLIO_ADMIN_USERNAME


def portfolio_permissions(request):
    return {"can_manage_posts": can_manage_posts(request.user)}
