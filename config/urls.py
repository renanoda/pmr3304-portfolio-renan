from django.contrib import admin
from django.urls import path
from portfolio import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.post_list, name="post_list"),
    path("projetos/novo/", views.post_create, name="post_create"),
    path("projetos/<int:pk>/", views.post_detail, name="post_detail"),
    path("projetos/<int:pk>/editar/", views.post_update, name="post_update"),
    path("projetos/<int:pk>/excluir/", views.post_delete, name="post_delete"),
]
