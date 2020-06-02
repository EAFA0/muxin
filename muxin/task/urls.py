from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from . import views

urlpatterns = [
    path('spider', views.TaskView.as_view()),
    path('<pk>/', views.TaskView.as_view())
]

urlpatterns = format_suffix_patterns(urlpatterns)
