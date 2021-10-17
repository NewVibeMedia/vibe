from django.urls import path
from . import views
from .views import (
    CustomizerView,
    CustomizerSave,
    # CustomizerCreateView,
)

urlpatterns = [
    path('settings/', CustomizerView, name='customizer-view'),
    path('settings/save/', CustomizerSave, name='customizer-save'),
]