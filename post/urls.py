from django.conf.urls import url
from django.contrib.auth.views import LoginView
from django.urls import path
from .views import (
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    SignUpView,
    GratitudePostListView, QuestionPostListView)
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.landing, name='home'),
    path('posts/', PostListView.as_view(), name='post-list'),
    path('posts/<int:pk>', PostDetailView.as_view(), name='post-detail'), #pk primary key, int integer
    path('posts/new/', PostCreateView.as_view(), name='post-create'),
    path('posts/<int:pk>/edit/', PostUpdateView.as_view(), name='post-edit'),
    path('posts/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('gratitude/', GratitudePostListView.as_view(), name='post-gratitude'),
    path('question/', QuestionPostListView.as_view(), name='post-gratitude'),
    path('about/', views.about, name='post-about'),

    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    # path('logout/', auth_views.logout, {'template_name': 'logged_out.html'}, name='logout'),

    path('search', views.search, name='search'),

    path('reset', views.reset)
]
