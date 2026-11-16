from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from .forms import CommentForm
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


@login_required
def comment_create(request, pk):
    post = get_object_or_404(Post, pk=pk)
    form = CommentForm(request.POST if request.method == "POST" else None)
    if request.method == "POST" and form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.author = request.user
        comment.save()
        return redirect("post_detail", pk=pk)
    return render(request, "comment_form.html", {"form": form, "post": post})
