import random

from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
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

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.add_message(request, messages.WARNING,
                                 self.permission_denied_message)
            return self.handle_no_permission()
        return super(CustomLoginRequiredMixin, self).dispatch(
            request, *args, **kwargs
        )

class PostListView(ListView):
    model = Post
    login_url = '/login/'
    
    template_name = 'post/home.html' # <app>/<model>_<viewtype>/html
    context_object_name = 'posts'
    ordering = ['-date_posted']


class GratitudePostListView(CustomLoginRequiredMixin, ListView):
    model = Post
    login_url = '/login/'

    template_name = 'post/home.html' # <app>/<model>_<viewtype>/html
    context_object_name = 'posts'
    ordering = ['-date_posted']

    def get_queryset(self):
        return Post.objects.filter(post_type="Gratitude")

class QuestionPostListView(CustomLoginRequiredMixin, ListView):
    model = Post
    login_url = '/login/'

    template_name = 'post/home.html' # <app>/<model>_<viewtype>/html
    context_object_name = 'posts'
    ordering = ['-date_posted']

    def get_queryset(self):
        user_items = Post.objects.filter(post_type="Question").filter(author=self.request.user) #.values('title')
        items = Post.objects.filter(title__in=list(user_items))
        return items

class PersonalPostListView(CustomLoginRequiredMixin, ListView):
    model = Post
    login_url = '/login/'

    template_name = 'post/home.html' # <app>/<model>_<viewtype>/html
    context_object_name = 'posts'
    ordering = ['-date_posted']

    def get_queryset(self):
        return Post.objects.filter(post_type="Personal").filter(author=self.request.user)

class PostDetailView(CustomLoginRequiredMixin, DetailView):
    model = Post

class PostDeleteView(CustomLoginRequiredMixin, DeleteView):
    login_url = '/login/'

    model = Post
    success_url = "/"


class PostCreateView(CustomLoginRequiredMixin, CreateView):
    # Redirect if not authenticated
    login_url = '/login/'

    model = Post
    fields = ['title', 'content', 'post_type']

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
        form.instance.author = User.objects.get(id=1)
        return super().form_valid(form)

class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

def login(request):
    return render(request, 'registration/login.html', {'title': 'User Login'})

def logout(request):
    return render(request, 'registration/logout.html', {'title': 'User Logout'})

def about(request):
    # return HttpResponse('<h1>Diary About</h1>')
    return render(request, 'post/about.html', {'title': 'About'})

