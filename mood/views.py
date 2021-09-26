from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core import serializers
from django.db.models import CharField, DateTimeField
from django.db.models.functions import Cast, TruncSecond
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.safestring import mark_safe

from .models import Mood
from django.views.generic import CreateView, DetailView, ListView, UpdateView, DeleteView
from datetime import date


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
        if len(objects_filter) == 0:  # not found
            messages.add_message(self.request, messages.WARNING,
                                 "You don't have permission to access that mood")
            # TODO redirect to mood list page
        return objects_filter


class MoodCreateView(CustomLoginRequiredMixin, CreateView):
    # Redirect if not authenticated
    login_url = '/login/'
    success_url = "/moods"
    model = Mood
    fields = ['mood']

    # The form has been already validated
    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.add_message(self.request, messages.SUCCESS,
                             "Mood created successfully")
        result = super().form_valid(form)
        return result

    def form_invalid(self, form):
        messages.add_message(self.request, messages.WARNING,
                             "Problem adding moods")
        return HttpResponseRedirect('/moods')


class MoodUpdateView(CustomLoginRequiredMixin, UpdateView):
    login_url = '/login/'

    model = Mood
    fields = ['mood', 'date_posted']
    success_url = "/moods"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class MoodDeleteView(CustomLoginRequiredMixin, DeleteView):
    login_url = '/login/'
    model = Mood
    success_url = "/moods"


@login_required
def display(request):
    login_url = '/login/'

    the_moods = list(Mood.objects.filter(author=request.user).order_by('-date_posted'))
    values = [v.to_list() for v in the_moods]
    # unix time: date.replace(tzinfo=timezone.utc).timestamp()

    context = {
        'title': 'Display',
        'data': mark_safe(list(values)),  # works but only returns string value of mood
    }
    return render(request, 'charts/display.html', context)


def mood_new(request):
    if not request.user.is_authenticated:
        messages.add_message(request, messages.WARNING,
                             'You have to be logged in to perform that action')
        return redirect("/login");

    if request.method == 'POST':
        new_mood = Mood(request.POST)
        new_mood.mood = int(request.POST["mood"])
        new_mood.author_id = request.user.id
        new_mood.id = None
        if new_mood.is_valid():
            new_mood.save()
            messages.add_message(request, messages.SUCCESS,
                                 "Mood created successfully");
            return redirect("/moods");
        else:
            messages.add_message(request, messages.WARNING,
                                 "Only one mood is allowed for one day.")
            return render(request, 'mood/mood_form.html', {"object": new_mood})

    else:
        new_mood = Mood()
        new_mood.date_posted = date.today()
        return render(request, 'mood/mood_form.html', {"object": new_mood})

    # post
