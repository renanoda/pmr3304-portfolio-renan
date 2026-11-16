from django.http import HttpResponse
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import RedirectURLMixin
from django.views.generic.edit import FormView
from django.contrib.auth.mixins import UserPassesTestMixin
from .permissions import can_manage_posts
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from .forms import CommentForm
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView
from .forms import PostForm
from .models import Category, Post, PostCover


class SignUp(RedirectURLMixin, FormView):
    template_name = "signup.html"
    form_class = UserCreationForm
    next_page = "home"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(self.get_success_url())
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        return super().get_context_data(next=self.get_redirect_url(), **kwargs)

    def form_valid(self, form):
        login(self.request, form.save())
        return super().form_valid(form)


class PostList(ListView):
    model = Post
    template_name = "list.html"
    context_object_name = "posts"


class Home(PostList):
    template_name = "home.html"

    def get_queryset(self):
        return super().get_queryset()[:3]


class CategoryList(ListView):
    queryset = Category.objects.prefetch_related("posts")
    template_name = "categories.html"
    context_object_name = "categories"


def category_detail(request, pk):
    category = get_object_or_404(Category, pk=pk)
    return render(request, "list.html", {"category": category, "posts": category.posts.all()})


class PostDetail(DetailView):
    model = Post
    template_name = "detail.html"


class ProjectAdminRequired(UserPassesTestMixin):
    def test_func(self):
        return can_manage_posts(self.request.user)


class PostCreate(ProjectAdminRequired, CreateView):
    model = Post
    form_class = PostForm
    template_name = "form.html"

    def get_success_url(self):
        return reverse("post_detail", args=[self.object.pk])


class PostUpdate(ProjectAdminRequired, UpdateView):
    model = Post
    form_class = PostForm
    template_name = "form.html"

    def get_success_url(self):
        return reverse("post_detail", args=[self.object.pk])


class PostDelete(ProjectAdminRequired, DeleteView):
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





def post_cover(request, pk):
    cover = get_object_or_404(PostCover, post_id=pk)
    return HttpResponse(bytes(cover.data), content_type=cover.content_type)
