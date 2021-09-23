from django.shortcuts import render
from .models import Mood
from django.views.generic import CreateView, DetailView, ListView


# Create your views here.


def index(request):
    return render(request, 'mood/mood.html', {})

class MoodListView(ListView):
    model = Mood
    template_name = 'post/mood.html' # <app>/<model>_<viewtype>/html
    context_object_name = 'moods'
    ordering = ['-date_posted']

class MoodDetailView(DetailView):
    model = Mood

class MoodCreateView(CreateView):
    # Redirect if not authenticated
    login_url = '/login/'

    model = Mood
    fields = ['mood']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)