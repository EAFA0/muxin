from django.shortcuts import render, get_object_or_404

from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .serializers import *
from .models import *

# Create your views here.


class DataSetView(generics.RetrieveUpdateAPIView):

    '''
    对 dataset 的本体进行增删改查操作, 暂无权限检查, 待重构
    '''

    def get(self, request, *args,pk = None, **kwargs):
        if pk is None:
            return generics.ListAPIView.get(self, request, *args, **kwargs)
        else:
            return super().get(request, *args, **kwargs)

    queryset = DataSet.objects.all()
    serializer_class = DataSetSerializer


class DataSetFileView(APIView):

    '''
    对 dataset 内部的文件进行增删改查操作,  暂无权限检查
    '''

    datasets = DataSet.objects.all()

    images = Image.objects.all()
    videos = Video.objects.all()

    def get_image_objs(self, dataset: DataSet, pk=None):
        '''
        获得带标签的 img 对象
        '''
        if pk is None:
            return self.images.filter(dataset=dataset.name)
        else:
            return self.images.filter(dataset=dataset.name, md5=pk)

    def get_video_objs(self, dataset: DataSet, pk=None):
        if pk is None:
            return self.videos.filter(dataset=dataset.name)
        else:
            return self.videos.filter(dataset=dataset.name, vid=pk)

    def get_objects(self, dataset, pk: int = None):
        if dataset.type == 'i':
            return self.get_image_objs(dataset, pk)
        elif dataset.type == 'v':
            return self.get_video_objs(dataset, pk)
        else:
            raise ValueError

    def get_serializer_class(self, dataset: DataSet = None, file_type: str = None):
        if dataset or file_type:
            if dataset:
                file_type = dataset.type

            if file_type == 'i':
                return ImageSerializer
            elif file_type == 'v':
                return VideoSerializer
            else:
                raise ValueError('不支持的文件类型')

        else:
            raise ValueError('dataset_id 和 file_type 全为空')

    def get(self, request, dataset_id, pk=None, fileds=None, format=None):
        '''
        获取指定 dataset 中的指定 / 全部文件描述
        '''
        dataset = self.datasets.get(pk=dataset_id)

        serializer_class = self.get_serializer_class(dataset)
        objs = self.get_objects(dataset, pk)
        ser = serializer_class(objs, many=True)

        return Response(ser.data)

    def post(self, request, dataset_id, pk=None, format=None):
        '''
        dataset 新增一个文件描述
        '''
        dataset = self.datasets.get(pk=dataset_id)
        serializer_class = self.get_serializer_class(dataset)

        ser = serializer_class(data=request.data)
        ser.initial_data['dataset'] = dataset.name

        if ser.is_valid():
            ser.save()
            return Response(ser.data, status=status.HTTP_201_CREATED)
        else:
            return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, dataset_id, pk, format=None):
        '''
        更新 dataset 中某一文件的描述
        '''
        dataset = self.datasets.get(pk=dataset_id)

        serializer_class = self.get_serializer_class(dataset)
        old_obj = self.get_objects(dataset, pk)[0]

        new = serializer_class(old_obj, data=request.data, partial=True)

        if new.is_valid():
            new.save()
            return Response(new.data, status=status.HTTP_201_CREATED)
        else:
            return Response(new.errors, status=status.HTTP_400_BAD_REQUEST)
