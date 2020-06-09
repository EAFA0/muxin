from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from . import views

urlpatterns = [
    path('', views.SchedulerAPIView.as_view()),
    path('<id>/', views.SchedulerAPIView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
