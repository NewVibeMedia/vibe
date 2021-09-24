from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.safestring import mark_safe

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

    def get_queryset(self):
        return Mood.objects.filter(author=self.request.user)

# TODO convert to method: https://realpython.com/django-redirects/
class MoodDetailView(CustomLoginRequiredMixin, DetailView):
    model = Mood
    login_url = "login"

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        objects_filter = Mood.objects.filter(author=self.request.user).filter(pk=pk)
        if len(objects_filter) == 0: # not found
            messages.add_message(self.request, messages.WARNING,
                                 "You don't have permission to access that mood")
            # TODO redirect to mood list page
        return objects_filter

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
    # mood_data = []
    # # populate mood_data with mood's data
    # mood_data.append(Mood.objects.first())
    context = {
        'title': 'Display',
        'data': Mood.objects.first(), # works but only returns string value of mood

        # NOT WORKING
        # 'data': Mood.objects.get(1).mood,
        # 'data': mark_safe(mood_data),
    }
    return render(request, 'charts/display.html', context)
