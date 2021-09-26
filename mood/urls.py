from django.urls import path
from . import views
from .views import MoodCreateView, MoodListView, MoodDetailView, MoodUpdateView, MoodDeleteView

urlpatterns = [
    path('moods/', MoodListView.as_view(), name='mood-home'),
    path('moods/<int:pk>', MoodDetailView.as_view(), name='mood-detail'),  # pk primary key, int integer
    path('moods/<int:pk>/edit/', MoodUpdateView.as_view(), name='mood-edit'),
    path('moods/<int:pk>/delete/', MoodDeleteView.as_view(), name='mood-delete'),
    # path('moods/create', MoodCreateView.as_view(), name='mood-create'),
    path('moods/new/', views.mood_new, name='mood-new'),
    path('calendar/', views.display, name='mood-display'),
]