from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import (
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
)
from django.urls import path
from .views import CommentCreateView, CommentUpdateView, CommentDeleteView


    


urlpatterns = [
    path("", views.home, name="home"),
    path("login/", auth_views.LoginView.as_view(template_name="blog/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(next_page="home"), name="logout"),
    path("register/", views.register, name="register"),
    path("profile/", views.profile, name="profile"),
    path("posts/", views.post_list, name="post_list"),
    path("posts/<int:pk>/", views.post_detail, name="post_detail"),
    path("search/", views.search, name="search"),
     # Post CRUD
    path("", PostListView.as_view(), name="post_list"),   
    path("post/<int:pk>/", PostDetailView.as_view(), name="post_detail"),
    path("post/new/", PostCreateView.as_view(), name="post_new"),
    path("post/<int:pk>/update/", PostUpdateView.as_view(), name="post_update"),
    path("post/<int:pk>/delete/", PostDeleteView.as_view(), name="post_delete"),

    # Comment CRUD (nested under posts)
    path("post/<int:pk>/comments/new/", CommentCreateView.as_view(), name="comment_new"),
    path("comments/<int:pk>/update/", CommentUpdateView.as_view(), name="comment_update"),
    path("comments/<int:pk>/delete/", CommentDeleteView.as_view(), name="comment_delete"),
]
