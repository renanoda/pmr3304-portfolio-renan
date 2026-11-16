from django.contrib import admin
from django.urls import path
from portfolio import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.PostList.as_view(), name="post_list"),
    path("projetos/novo/", views.PostCreate.as_view(), name="post_create"),
    path("projetos/<int:pk>/", views.PostDetail.as_view(), name="post_detail"),
    path("projetos/<int:pk>/editar/", views.PostUpdate.as_view(), name="post_update"),
    path("projetos/<int:pk>/excluir/", views.PostDelete.as_view(), name="post_delete"),
]

