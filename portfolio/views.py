from django.shortcuts import get_object_or_404, redirect, render
from .forms import PostForm
from .models import Post


def post_list(request):
    return render(request, "list.html", {"posts": Post.objects.all()})


def post_detail(request, pk):
    return render(request, "detail.html", {"post": get_object_or_404(Post, pk=pk)})


def post_create(request):
    return edit_post(request)


def post_update(request, pk):
    return edit_post(request, get_object_or_404(Post, pk=pk))


def edit_post(request, post=None):
    form = PostForm(request.POST if request.method == "POST" else None, instance=post)
    if request.method == "POST" and form.is_valid():
        saved = form.save()
        return redirect("post_detail", pk=saved.pk)
    return render(request, "form.html", {"form": form, "post": post})


def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        post.delete()
        return redirect("post_list")
    return render(request, "delete.html", {"post": post})

