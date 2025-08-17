from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.exceptions import FieldError
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Post




def home(request):
    return render(request, "blog/home.html")


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your account has been created! You can now log in.")
            return redirect("login")
    else:
        form = UserCreationForm()
    return render(request, "blog/register.html", {"form": form})


@login_required
def profile(request):
    return render(request, "blog/profile.html")


def post_list(request):
    posts = Post.objects.all().order_by("-created_at")   # correct field
    return render(request, "blog/post_list.html", {"posts": posts})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, "blog/post_detail.html", {"post": post})


def search(request):
    query = request.GET.get("q", "").strip()
    posts = Post.objects.none()
    if query:
        base_q = Q(title__icontains=query) | Q(content__icontains=query)
        # If taggit isn't wired yet, skip the tag filter gracefully
        try:
            posts = Post.objects.filter(base_q | Q(tags__name__icontains=query)).distinct()
        except FieldError:
            posts = Post.objects.filter(base_q).distinct()
    return render(request, "blog/search_results.html", {"posts": posts, "q": query})




class PostListView(ListView):
    model = Post
    template_name = "blog/post_list.html"   # use your existing template
    context_object_name = "posts"


class PostDetailView(DetailView):
    model = Post
    template_name = "blog/post_detail.html"  # your existing template
    context_object_name = "post"


class PostCreateView(CreateView):
    model = Post
    template_name = "blog/post_form.html"   # reuse your form template
    fields = ["title", "content", "author"]  # adjust if you have more fields


class PostUpdateView(UpdateView):
    model = Post
    template_name = "blog/post_form.html"   # reuse same form template
    fields = ["title", "content", "author"]


class PostDeleteView(DeleteView):
    model = Post
    template_name = "blog/post_confirm_delete.html"  # existing delete template
    success_url = reverse_lazy("post_list")
