from django.shortcuts import render, get_object_or_404

from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Task, Spider
from .serializers import TaskSerializer, SpiderSerializer
from .api import TaskAPI, SpiderAPI


class TaskRetrieveAPIView(generics.RetrieveAPIView):

    lookup_field = 'name'
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

class TaskListCreateAPIView(generics.ListAPIView):

    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def post(self, request, format=None):
        config_str = request.data['config']

        task = TaskAPI.create(config_str)
        task_str = TaskSerializer(instance=task).data
        return Response(task_str, status=status.HTTP_201_CREATED)

class TaskScheduleAPIView(APIView):

    def post(self, request, name: str, format=None):
        TaskAPI.start(name)
        return Response()
    
    def delete(self, request, name:str , format=None):
        TaskAPI.cancel(name)
        return Response()