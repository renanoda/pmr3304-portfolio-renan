from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView
from .forms import PostForm
from .models import Post


class PostList(ListView):
    model = Post
    template_name = "list.html"
    context_object_name = "posts"


class PostDetail(DetailView):
    model = Post
    template_name = "detail.html"


class PostCreate(CreateView):
    model = Post
    form_class = PostForm
    template_name = "form.html"

    def get_success_url(self):
        return reverse("post_detail", args=[self.object.pk])


class PostUpdate(UpdateView):
    model = Post
    form_class = PostForm
    template_name = "form.html"

    def get_success_url(self):
        return reverse("post_detail", args=[self.object.pk])


class PostDelete(DeleteView):
    model = Post
    template_name = "delete.html"
    success_url = reverse_lazy("post_list")
