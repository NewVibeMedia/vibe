from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from .models import Mood
from django.views.generic import CreateView, DetailView, ListView


# Create your views here.
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

class MoodListView(CustomLoginRequiredMixin, ListView):
    model = Mood
    login_url = "login"
    context_object_name = 'moods'
    ordering = ['-date_posted']

class MoodDetailView(CustomLoginRequiredMixin, DetailView):
    model = Mood
    login_url = "login"

class MoodCreateView(CustomLoginRequiredMixin, CreateView):
    # Redirect if not authenticated
    login_url = '/login/'

    model = Mood
    fields = ['mood']

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.add_message(self.request, messages.SUCCESS,
                             "Mood created successfully")
        return super().form_valid(form)

def display(request):
    return render(request, 'charts/display.html', {'title': 'Display'})
