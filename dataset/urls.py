from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path('', views.DataSetCreateListAPIView.as_view()),
    path('<name>/', views.DataSetRetrieveUpdateAPIView.as_view()),

    path('<name>/file/', views.DataCreateListAPIView.as_view()),
    path('<name>/file/<pk>/', views.DataRetrieveUpdateAPIView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
