from django.urls import path
from movie import views

urlpatterns = [
    path('detail/', views.MovieListView.as_view(), name='detail'),
]