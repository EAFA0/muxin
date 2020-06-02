from django.shortcuts import render, get_object_or_404

from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.response import Response


from .models import Task, Spider
from .serializers import TaskSerializer, SpiderSerializer
# Create your views here.


class TaskView(generics.RetrieveUpdateDestroyAPIView):

    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def get(self, request, pk: str = None, *args,  **kwargs):
        if pk is None:
            return generics.ListCreateAPIView(self, request, *args, **kwargs)
        else:
            return super().get(request, pk, *args, **kwargs)



# class TaskView(APIView):

#     def get(self, request, task: str = None, format=None):
#         '''
#         获取一个 Task 的信息
#         '''
#         if task is not None:
#             obj = get_object_or_404(Task, name=task)
#             ser = TaskSerializer(obj)

#             return Response(ser.data)
#         else:
#             return Response('')

#     def post(self, request, task: str = None, format=None):
#         '''
#         新建一个 Task
#         '''
#         ser = TaskSerializer(data=request.data)

#         if ser.is_valid():
#             ser.save()
#             return Response(ser.data, status=status.HTTP_201_CREATED)
#         else:
#             return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)


#     def put(self, request, task: str = None, format=None):
#         '''
#         修改 Task 信息并重新拉起
#         '''

#     def delete(self, request, task: str = None, format=None):
#         '''
#         删除一个 Task, 并停止
#         '''
