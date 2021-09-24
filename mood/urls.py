from django.urls import path
from . import views
from .views import MoodCreateView, MoodListView, MoodDetailView

urlpatterns = [
    path('moods/', MoodListView.as_view(), name='mood-home'),
    path('moods/<int:pk>', MoodDetailView.as_view(), name='mood-detail'),  # pk primary key, int integer
    path('moods/new/', MoodCreateView.as_view(), name='mood-create'),
    path('calendar/', views.display, name='mood-display'),
]