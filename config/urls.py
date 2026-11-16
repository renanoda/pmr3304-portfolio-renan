from django.contrib.auth.views import LoginView
from django.contrib import admin
from django.urls import path
from portfolio import views

urlpatterns = [
    path("categorias/", views.CategoryList.as_view(), name="category_list"),
    path("categorias/<int:pk>/", views.category_detail, name="category_detail"),
    path("accounts/login/", LoginView.as_view(template_name="login.html"), name="login"),
    path("projetos/<int:pk>/comentar/", views.comment_create, name="comment_create"),
    path("admin/", admin.site.urls),
    path("", views.PostList.as_view(), name="post_list"),
    path("projetos/novo/", views.PostCreate.as_view(), name="post_create"),
    path("projetos/<int:pk>/", views.PostDetail.as_view(), name="post_detail"),
    path("projetos/<int:pk>/editar/", views.PostUpdate.as_view(), name="post_update"),
    path("projetos/<int:pk>/excluir/", views.PostDelete.as_view(), name="post_delete"),
]


