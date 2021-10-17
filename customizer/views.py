from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from rest_framework.decorators import api_view

from .models import Customizer
from django.views.generic import (
    CreateView,
    UpdateView,
)

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

# Create your views here.
def CustomizerView(request):
    model = Customizer
    user = User.objects.get(username=request.user)
    setting = model.objects.filter(user=user)
    if setting:
        setting = setting[0]
        return render(request=request, template_name='customizer_view.html', context={"nav_color": setting.theme_nav,
                                                                                      "bg_color": setting.theme_background,
                                                                                      "font_size": setting.font_size,
                                                                                      "font_style": setting.font_style})
    else:
        return render(request=request, template_name='customizer_view.html', context={"nav_color": Customizer.get_default_nav_color(),
                                                                                      "bg_color": Customizer.get_default_bg_color(),
                                                                                      "font_size": Customizer.get_default_font_size(),
                                                                                      "font_style": Customizer.get_default_font_style()})

# class CustomizerCreateView(CustomLoginRequiredMixin, CreateView):
#     login_url = '/login/'
#     model = Customizer
#
#     def get_initial(self):
#         print("hello")
#
#     def form_valid(self, form):
#         form.instance.author = self.request.user
#         messages.add_message(self.request, messages.SUCCESS,
#                             "Settings has been saved.")

@api_view(['POST'])
def CustomizerSave(request):
    if request.method == 'POST':
        form = request.POST
        model = Customizer
        alldata = request.POST
        user = User.objects.get(username=request.user)
        setting = model.objects.filter(user=user)
        if setting:
            setting.delete()
        model.objects.get_or_create(user=user,
                                    theme_nav=alldata['nav-color'],
                                    theme_background=alldata['bg-color'],
                                    font_size=alldata['font-size-selector'],
                                    font_style=alldata['font-style-selector'])
        messages.add_message(request, messages.SUCCESS,
                             "Settings has been saved.")
        return redirect('customizer-view')