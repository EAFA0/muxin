from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path('', views.DataSetView.as_view()),
    path('dataset',views.DataSetView.as_view()),
    path('<int:pk>/', views.DataSetView.as_view()),

    path('<int:dataset_id>/file/',
         views.DataSetFileView.as_view()),
    path('<int:dataset_id>/file/<pk>/',
         views.DataSetFileView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
