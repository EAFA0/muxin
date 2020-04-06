from django.shortcuts import render, get_object_or_404

from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .serializers import *
from .models import *

# Create your views here.

class DataSetView(generics.ListCreateAPIView,
                  generics.RetrieveUpdateAPIView):

    queryset = DataSet.objects.all()
    serializer_class = DataSetSerializer