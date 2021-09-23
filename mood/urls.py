from django.urls import path
from . import views
from .views import MoodCreateView, MoodListView, MoodDetailView

urlpatterns = [
    path('', MoodListView.as_view(), name='mood-home'),
    path('<int:pk>', MoodDetailView.as_view(), name='mood-detail'),  # pk primary key, int integer

    path('new/', MoodCreateView.as_view(), name='mood-create'),

]