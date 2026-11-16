from django.shortcuts import get_object_or_404, redirect, render
from .models import Post


def post_list(request):
    return render(request, "list.html", {"posts": Post.objects.all()})


def post_detail(request, pk):
    return render(request, "detail.html", {"post": get_object_or_404(Post, pk=pk)})


def post_create(request):
    if request.method == "POST":
        post = Post.objects.create(title=request.POST["title"], content=request.POST["content"])
        return redirect("post_detail", pk=post.pk)
    return render(request, "form.html")


def post_update(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        post.title = request.POST["title"]
        post.content = request.POST["content"]
        post.save()
        return redirect("post_detail", pk=pk)
    return render(request, "form.html", {"post": post})


def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        post.delete()
        return redirect("post_list")
    return render(request, "delete.html", {"post": post})
