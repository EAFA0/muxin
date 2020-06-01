from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path('', views.DataSetAPIView.as_view()),
    path('<name>/', views.DataSetAPIView.as_view()),

    path('<name>/file/',
         views.DataSetFileView.as_view()),
    path('<name>/file/<pk>/',
         views.DataSetFileView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
