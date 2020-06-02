from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from . import views

urlpatterns = [
    path('', views.TaskListCreateAPIView.as_view()),
    path('<name>/', views.TaskRetrieveAPIView.as_view()),

    path('<name>/schedule', views.TaskScheduleAPIView.as_view())
]

urlpatterns = format_suffix_patterns(urlpatterns)
