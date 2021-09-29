import random
import datetime
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from .models import Post
from django.contrib.auth.models import User
# from django.http import HttpResponse
from django.core.management import call_command
from django.db.models import Q
from django.utils import timezone
import os

# Routes
def home(request):
    # return HttpResponse('<h1>Diary Home</h1>')
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'post/home.html', context)

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


class RecentListView(ListView):
    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.is_superuser:
            queryset = queryset.filter(date_posted__gt=timezone.now() - datetime.timedelta(days=1))
        return queryset


class PostListView(RecentListView):
    model = Post
    login_url = '/login/'
    
    template_name = 'post/home.html' # <app>/<model>_<viewtype>/html
    context_object_name = 'posts'
    ordering = ['-date_posted']


class GratitudePostListView(CustomLoginRequiredMixin, RecentListView):
    model = Post
    login_url = '/login/'

    template_name = 'post/home.html' # <app>/<model>_<viewtype>/html
    context_object_name = 'posts'
    ordering = ['-date_posted']

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post_type'] = "Gratitude"
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(post_type="Gratitude")
        return queryset

class QuestionPostListView(CustomLoginRequiredMixin, RecentListView):
    model = Post
    login_url = '/login/'

    template_name = 'post/home.html' # <app>/<model>_<viewtype>/html
    context_object_name = 'posts'
    ordering = ['-date_posted']

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post_type'] = "Reflective Question"
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        user_items = queryset.filter(post_type="Question").filter(author=self.request.user) #.values('title')
        items = queryset.filter(title__in=list(user_items))
        return items

class PersonalPostListView(CustomLoginRequiredMixin, ListView):
    model = Post
    login_url = '/login/'

    template_name = 'post/home.html' # <app>/<model>_<viewtype>/html
    context_object_name = 'posts'
    ordering = ['-date_posted']

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post_type'] = "Personal Reflection"
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(post_type="Personal").filter(author=self.request.user)
        return queryset

class PostDetailView(CustomLoginRequiredMixin, DetailView):
    model = Post
    login_url = '/login/'

    # Get post if it's not personal
    def get_queryset(self):
        qs = super(PostDetailView, self).get_queryset()
        pk = self.kwargs.get('pk')
        result = qs.filter(pk=pk)

        if not self.request.user.is_superuser:
            # Check if post is personal
            if len(result.filter(post_type="Personal")) != 0:
                # If it is, also check if it belongs to user.
                if len(result.filter(author_id=self.request.user.id)) == 0:
                    messages.add_message(self.request, messages.ERROR,
                                            self.user_permission_denied_message)
                    raise PermissionDenied
        
        return result


class PostDeleteView(CustomLoginRequiredMixin, DeleteView):
    login_url = '/login/'

    model = Post
    success_url = "/"

    # https://stackoverflow.com/questions/5531258/example-of-django-class-based-deleteview
    def get_queryset(self):
        return get_post_queryset(PostDeleteView, self)


    def delete(self, request, *args, **kwargs):
        messages.add_message(self.request, messages.SUCCESS,
                                 "Post was successfully deleted.")
        return super(PostDeleteView, self).delete(request, *args, **kwargs)

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
        "I can't imagine living without..."
    ]  # https://positivepsychology.com/introspection-self-reflection/

    def get_initial(self):
        """
        Pre-populates post title based on post type
        Post type sent through GET request (0 -> gratitude, 1 -> reflective, none -> personal entry)
        """
        initial = super(CreateView, self).get_initial()
        for k, v in self.request.GET.items():
            if v == '0':  # gratitude post
                initial.update({'title': self.gratitude_question})
                initial.update({'post_type': "Gratitude"})
            elif v == '1':  # reflective question
                initial.update({'title': random.choice(self.reflection_questions)})
                initial.update({'post_type': "Question"})
            else:
                initial.update({'title': ""})
                initial.update({'post_type': "Personal"})
        return initial

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.add_message(self.request, messages.SUCCESS,
                             "Post created successfully")
        return super().form_valid(form)

class PostUpdateView(CustomLoginRequiredMixin, UpdateView):
    login_url = '/login/'

    model = Post
    fields = ['title', 'content']
    
    def form_valid(self, form):
        if not self.request.user.is_superuser:
            form.instance.author = self.request.user
        messages.add_message(self.request, messages.SUCCESS,
                            "Post was successfully updated.")
        return super().form_valid(form)

    def get_queryset(self):
        return get_post_queryset(PostUpdateView, self)

class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

# Used to determine if the user has edit/delete permissions for the post
def get_post_queryset(PostView, self):
    qs = super(PostView, self).get_queryset()
    pk = self.kwargs.get('pk')
    if self.request.user.is_superuser:
        result = qs.filter(pk=pk)
    else:
        result = qs.filter(author_id=self.request.user.id).filter(pk=pk)
        if len(result.filter(pk=pk)) == 0: # Post does not belong to user
            messages.add_message(self.request, messages.ERROR,
                                    self.user_permission_denied_message)
            raise PermissionDenied

    return result

# TODO Success Message: https://stackoverflow.com/questions/47054538/django-loginview-send-success-message
def login(request):
    return render(request, 'registration/login.html', {'title': 'User Login'})

def logout(request):
    return render(request, 'registration/logout.html', {'title': 'User Logout'})

def about(request):
    # return HttpResponse('<h1>Diary About</h1>')
    return render(request, 'post/about.html', {'title': 'About'})

@login_required()
def search(request):
    query = request.POST['search']
    # print("QUERY>>", query)
    # print("Objects;", Post.objects.all())
    if not request.user.is_authenticated:
        #TODO: add messages
        return render(request, 'post/search.html', {'title': 'Search', 'posts': []})
    if request.user.is_superuser:
        # TODO: 24 hours
        results = Post.objects.filter(Q(title__icontains=query) | Q(content__icontains=query))
    else:
        # is limited to its owns posts?
        # Post.objects.filter(author_id = request.user.id)
        criterion1 = Q(title__icontains=query)
        criterion2 = Q(content__icontains=query)
        criterion3 = Q(author_id=request.user.id)
        results = Post.objects.filter( (criterion1 | criterion2)  & criterion3 )


    return render(request, 'post/search.html', {'title': 'Search', 'posts': results})

def reset(request):
    #
    DJANGO_ENV = os.environ.get('DJANGO_ENV')
    if DJANGO_ENV == "production":
        raise ValueError("Unable to reset database in production")

    print("reset db", DJANGO_ENV)
    call_command("truncate", "--apps", "post", "mood")
    call_command("loaddata", "db/fixtures/moods.json")
    call_command("loaddata", "db/fixtures/posts.json")
    return render(request, 'reset.html', {'title': 'Reset DB'})
