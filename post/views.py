import random
import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)

from .anonlist import rand_anon_author
from .forms import SignUpForm
from .models import Post, UserPostOptions
from django.contrib.auth.models import User
from django.core.management import call_command
from django.db.models import Q
from mood.models import Mood
from django.utils import timezone
import os

# ==============HOME PAGE================
# Landing Page
def landing(request):
    number_of_posts = 0
    entered_mood_today = None
    if request.user.is_authenticated:
        number_of_posts = Post.objects.filter(date_posted__day=timezone.now().day).filter(author_id=request.user.id).count()
        entered_mood_today = Mood.objects.filter(author=request.user).filter(date_posted__day=timezone.now().day).first

    return render(request, 'landing.html', {'title': 'Home', 'post_count': number_of_posts, 'mood_today': entered_mood_today})

# ==============HELPER FUNCTIONS================
# Helper class, requires login and displays Permission denied error
class CustomLoginRequiredMixin(LoginRequiredMixin):
    """ The LoginRequiredMixin extended to add a relevant message to the
    messages framework by setting the ``permission_denied_message``
    attribute. """
    permission_denied_message = 'You have to be logged in to perform that action'
    user_permission_denied_message = 'You do not have permission to perform that action'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.add_message(request, messages.WARNING,
                                 self.permission_denied_message)
            return self.handle_no_permission()
        return super(CustomLoginRequiredMixin, self).dispatch(
            request, *args, **kwargs
        )

# Posts within 24 hours
class RecentListView(ListView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["rand_name"] = rand_anon_author()
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.is_superuser:
            queryset = queryset.filter(date_posted__gt=timezone.now() - datetime.timedelta(days=1))
            # yes, bad admin bad, no hiding
            hide_set = UserPostOptions.objects.filter(user=self.request.user, option_type="Hide").values('post')
            queryset = queryset.exclude(pk__in=hide_set)
        return queryset

# Reset the DB
def reset(request):
    DJANGO_ENV = os.environ.get('DJANGO_ENV')
    if DJANGO_ENV == "production":
        raise ValueError("Unable to reset database in production")

    print("reset db", DJANGO_ENV)
    call_command("truncate", "--apps", "post", "mood")
    call_command("loaddata", "db/fixtures/moods.json")
    call_command("loaddata", "db/fixtures/posts.json")
    return render(request, 'reset.html', {'title': 'Reset DB'})

# ==============STANDARD POSTS LIST VIEW================
# My Posts page, lists all recent posts
class PostListView(CustomLoginRequiredMixin, RecentListView):
    model = Post
    login_url = '/login/'

    template_name = 'post/home.html'  # <app>/<model>_<viewtype>/html
    context_object_name = 'posts'
    ordering = ['-date_posted']

# My Gratitude Posts page, lists all recent gratitude type posts
class GratitudePostListView(CustomLoginRequiredMixin, RecentListView):
    model = Post
    login_url = '/login/'

    template_name = 'post/home.html'  # <app>/<model>_<viewtype>/html
    context_object_name = 'posts'
    ordering = ['-date_posted']

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post_type'] = "Gratitude"
        # This chonker returns a tuple of post ids that the user has saved
        context['saved_posts'] = list(UserPostOptions.objects.filter(user=self.request.user, option_type="Save").values_list('post', flat=True))
        context['save_str'] = "Save"
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(post_type="Gratitude")
        return queryset

# My Reflective Question Posts page, lists all recent gratitude type posts
class QuestionPostListView(CustomLoginRequiredMixin, RecentListView):
    model = Post
    login_url = '/login/'

    template_name = 'post/home.html'  # <app>/<model>_<viewtype>/html
    context_object_name = 'posts'
    ordering = ['-date_posted']

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post_type'] = "Reflective Question"
        # This chonker returns a tuple of post ids that the user has saved
        context['saved_posts'] = list(UserPostOptions.objects.filter(user=self.request.user, option_type="Save").values_list('post', flat=True))
        context['save_str'] = "Save"
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        user_items = queryset.filter(post_type="Question").filter(author=self.request.user)  # .values('title')
        items = queryset.filter(title__in=list(user_items))
        return items

# User's history of posts
class HistoryListView(CustomLoginRequiredMixin, ListView):
    model = Post
    login_url = '/login/'

    template_name = 'post/home.html'  # <app>/<model>_<viewtype>/html
    context_object_name = 'posts'
    ordering = ['-date_posted']

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(author_id=self.request.user.id)

# View all posts saved, not time limited
class SavePostListView(CustomLoginRequiredMixin, ListView):
    model = UserPostOptions
    login_url = '/login/'

    template_name = 'post/post_options.html'
    context_object_name = 'posts'
    ordering = ['-date_created']

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["rand_name"] = rand_anon_author()
        context['option_name'] = "Saved"
        context['option_type'] = "Save"
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        saved_posts = queryset.filter(user=self.request.user, option_type="Save").values('post')
        actual_posts = []
        for post in saved_posts:
            actual_posts.append(Post.objects.get(pk=post['post']))
        return actual_posts

# View all hidden posts
class HidePostListView(CustomLoginRequiredMixin, ListView):
    model = UserPostOptions
    login_url = '/login/'

    template_name = 'post/post_options.html'
    context_object_name = 'posts'
    ordering = ['-date_created']

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["rand_name"] = rand_anon_author()
        context['option_name'] = "Hidden"
        context['option_type'] = "Hide"
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        saved_posts = queryset.filter(user=self.request.user, option_type="Hide").values('post')
        actual_posts = []
        for post in saved_posts:
            actual_posts.append(Post.objects.get(pk=post['post']))
        return actual_posts

# Show details about one post
class PostDetailView(CustomLoginRequiredMixin, DetailView):
    model = Post
    login_url = '/login/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # This chonker returns a tuple of post ids that the user has saved/hidden
        context['saved_posts'] = list(UserPostOptions.objects.filter(user=self.request.user, option_type="Save").values_list('post', flat=True))
        context['save_str'] = "Save"
        context['hidden_posts'] = list(UserPostOptions.objects.filter(user=self.request.user, option_type="Hide").values_list('post', flat=True))
        context['hide_str'] = "Hide" 
        return context

    # Get post
    def get_queryset(self):
        qs = super(PostDetailView, self).get_queryset()
        pk = self.kwargs.get('pk')
        result = qs.filter(pk=pk)

        return result

# ==============POST OPERATIONS================
# Create a post
class PostCreateView(CustomLoginRequiredMixin, CreateView):
    # Redirect if not authenticated
    login_url = '/login/'

    model = Post
    fields = ['title', 'content', 'post_type', 'date_posted']

    gratitude_question = "What are you grateful for today?"
    reflection_questions = [
        "What would you do if you knew you could not fail?",
        "What did you do today that you are most proud of?",
        "Are you letting things out of your control make you stressed?",
        "What did you achieve today?",
        "What inspires you?",
        "I can't imagine living without...",
        "Am I living true to myself?",
        "Why do I matter?",
        "What have I given up on?",
        "Is it more important to love or be loved?",
        "If I could talk to my younger self, I would tell them...",
        "List 5 things that make you smile",

    ]  # https://positivepsychology.com/introspection-self-reflection/

    def get_initial(self):
        """
        Pre-populates post title based on post type
        Post type sent through GET request (0 -> gratitude, 1 -> reflective, none -> personal entry)
        """
        initial = super(CreateView, self).get_initial()
        question = False
        for k, v in self.request.GET.items():
            if v == '1':  # reflective question
                initial.update({'title': random.choice(self.reflection_questions)})
                initial.update({'post_type': "Question"})
                question = True
        if not question:  # gratitude post
            initial.update({'title': self.gratitude_question})
            initial.update({'post_type': "Gratitude"})
        return initial

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.add_message(self.request, messages.SUCCESS,
                             "Post successfully created.")
        return super().form_valid(form)

# Delete a post
class PostDeleteView(CustomLoginRequiredMixin, DeleteView):
    login_url = '/login/'

    model = Post
    success_url = "/posts" #TODO Redirection on Delete

    def get_queryset(self):
        return get_post_queryset(PostDeleteView, self)

    def delete(self, request, *args, **kwargs):
        messages.add_message(self.request, messages.SUCCESS,
                             "Post successfully deleted.")
        return super(PostDeleteView, self).delete(request, *args, **kwargs)

# Update a post
class PostUpdateView(CustomLoginRequiredMixin, UpdateView):
    login_url = '/login/'

    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        if not self.request.user.is_superuser:
            form.instance.author = self.request.user
        messages.add_message(self.request, messages.SUCCESS,
                             "Post successfully updated.")
        return super().form_valid(form)

    def get_queryset(self):
        return get_post_queryset(PostUpdateView, self)

# ==============SAVING AND HIDING POSTS================
# Saving and Hiding posts
class PostOptionView(CustomLoginRequiredMixin, DetailView):
    model = Post
    login_url = '/login/'
    template_name = 'post/post_option_detail.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['option_type'] = self.kwargs.get('option')
        return context

    def get_queryset(self):
        qs = super(PostOptionView, self).get_queryset()
        pk = self.kwargs.get('pk')
        result = qs.filter(pk=pk)
        # if we can't find the post in saved or hid
        if not UserPostOptions.objects.filter(post__in=result, option_type=self.kwargs.get('option')):
            messages.add_message(self.request, messages.ERROR,
                                 "Post not found")
            raise ObjectDoesNotExist
        return result

# Remove a post from Saved/Hidden posts
def PostOptionEdit(request, pk, option):
    model = UserPostOptions
    user = User.objects.get(username=request.user.username)
    post = Post.objects.get(pk=pk)
    model.objects.filter(user=user, post=post, option_type=option).delete()

    if option == model.OPTION_TYPES[0][0]: # Save
        messages.add_message(request,messages.SUCCESS, "Saved post successfully removed from list.")    
    else: # Hidden
        messages.add_message(request,messages.SUCCESS, "Hidden post successfully removed from list.")

    referer = request.META.get('HTTP_REFERER')
    if "Save" in str(referer):
        return redirect('/saved')
    elif "Hide" in str(referer):
        return redirect('/hid')
    else:
        return redirect(referer)

# Save a post
def UserPostSave(request, pk, user):
    model = UserPostOptions
    user = User.objects.get(username=user)
    post = Post.objects.get(pk=pk)
    model.objects.get_or_create(user=user, post=post, option_type='Save')
    messages.add_message(request, messages.SUCCESS, "Post successfully saved.")

    if post.post_type == post.POST_TYPES[0][0]: # Gratitude
        return redirect('post-gratitude')
    else: # Question
        return redirect('post-question')

# Hide a post
def UserPostHide(request, pk, user):
    model = UserPostOptions
    user = User.objects.get(username=user)
    post = Post.objects.get(pk=pk)
    model.objects.get_or_create(user=user, post=post, option_type='Hide')
    messages.add_message(request, messages.SUCCESS, "Post successfully hidden.")

    if post.post_type == post.POST_TYPES[0][0]: # Gratitude
        return redirect('post-gratitude')
    else:  # Question
        return redirect('post-question')

# Used to determine if the user has edit/delete permissions for the post
def get_post_queryset(PostView, self):
    qs = super(PostView, self).get_queryset()
    pk = self.kwargs.get('pk')
    if self.request.user.is_superuser:
        result = qs.filter(pk=pk)
    else:
        result = qs.filter(author_id=self.request.user.id).filter(pk=pk)
        if len(result.filter(pk=pk)) == 0:  # Post does not belong to user
            messages.add_message(self.request, messages.ERROR,
                                 self.user_permission_denied_message)
            raise PermissionDenied

    return result

# ==============AUTHENTICATION================
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.save()
            raw_password = form.cleaned_data.get('password1')

            return redirect('login')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})


def login(request):
    return render(request, 'registration/login.html', {'title': 'User Login'})

def logout(request):
    return render(request, 'registration/logout.html', {'title': 'User Logout'})

# ==============SEARCH================
@login_required()
def search(request):
    query = request.POST['search']
    # print("QUERY>>", query)
    # print("Objects;", Post.objects.all())
    if not request.user.is_authenticated:
        return render(request, 'post/search.html', {'title': 'Search', 'posts': []})
    if request.user.is_superuser:
        results = Post.objects.filter(Q(title__icontains=query) | Q(content__icontains=query))
    else:
        # is limited to its owns posts?
        # Post.objects.filter(author_id = request.user.id)
        criterion1 = Q(title__icontains=query)
        criterion2 = Q(content__icontains=query)
        criterion3 = Q(author_id=request.user.id)
        criterion4 = Q(date_posted__gt=timezone.now() - datetime.timedelta(days=1))

        results = Post.objects.filter((criterion1 | criterion2) & criterion3 & criterion4)

    return render(request, 'post/search.html', {'title': 'Search', 'posts': results})

