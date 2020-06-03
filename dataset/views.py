import json
import itertools

from django.shortcuts import get_object_or_404

from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .serializers import DataSetSerializer, DataSerializer, LabelSerializer
from .models import DataSet, Data, Label

# Create your views here.


class DataSetRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    lookup_field = 'name'
    queryset = DataSet.objects.all()
    serializer_class = DataSetSerializer


class DataSetCreateListAPIView(generics.ListCreateAPIView):
    queryset = DataSet.objects.all()
    serializer_class = DataSetSerializer


class DataAPIView(APIView):

    datas = Data.objects.all()

    def _get_datas_and_labels(self, *, pk: str = None, dataset: str = None, labels: list = None) -> (list, dict):
        '''
        返回的数据结构:
        data :  [Datas]
        labels: {data.md5: [Labels]}
        '''

        if pk is not None:
            data = get_object_or_404(Data, pk=pk)
            label = get_object_or_404(Label, data=data.md5)
            return [data], {data.md5: [label]}

        if dataset is None:
            raise ValueError("dataset is None")

        if labels is None:
            label_objs = Label.objects.filter(dataset=dataset)
        else:
            label_objs = Label.objects.filter(
                dataset=dataset, label__in=labels)

        labels_dict = {
            key: list(list_iter)
            for key, list_iter in itertools.groupby(
                label_objs, key=lambda label: label.data)
        }

        data_pks = [label.data for label in label_objs]
        return self.datas.filter(pk__in=data_pks), labels_dict

    def create_data(self, data_json: dict):
        labels = data_json['labels'] \
            if 'labels' in data_json else dict()

        # 保存 data 部分数据
        data_ser = DataSerializer(data=data_json)
        if data_ser.is_valid():
            data_ser.save()
        else:
            raise ValueError(data_ser.errors)

        # 保存 labels 数据, 并建立 data 和 label 之间的连接
        for label in labels:
            label['data'] = data_json['md5']
            label_ser = LabelSerializer(data=label)
            if label_ser.is_valid():
                label_ser.save()
            else:
                raise ValueError(label_ser.errors)

    def _serialized(self, data, labels):
        # 序列化 data, labels 对象
        data_json = DataSerializer(instance=data).data
        label_jsons = [LabelSerializer(instance=label).data
                       for label in labels]

        # 合并 data, labels 的 json 字符串
        data_json['labels'] = label_jsons
        return data_json

    def serialized_datas(self, datas, labels_dict) -> json:
        '''
        datas:          [Datas]
        lebels_dict:    {Data.md5:[Labels]}
        '''
        json_obj = [
            self._serialized(data, labels_dict[data.md5])
            for data in datas
        ]

        return json_obj

    def get_datas_and_labels_dict(self, params, name, pk, format=None):
        '''
        获取指定 dataset 中的指定 / 全部文件描述
        '''
        # 这里需要增加对 dataset 的检查
        dataset = get_object_or_404(DataSet, pk=name)

        # 获取 labels 字段
        labels = params['labels'].split(',') \
            if 'labels' in params else None

        # 获取 data, labels 数据
        return self._get_datas_and_labels(
            dataset=dataset.name, pk=pk, labels=labels)


class DataCreateListAPIView(DataAPIView):

    def get(self, request, name, format=None):
        # 获取 data 和 labels 数据
        datas, labels_dict = self.get_datas_and_labels_dict(
            request.GET, name, None, format=format)

        json_obj = self.serialized_datas(datas, labels_dict)
        return Response(json_obj)

    def post(self, request, name, format=None):
        '''
        dataset 新增一个文件描述
        '''
        # 检查数据集是否存在
        get_object_or_404(DataSet, pk=name)

        _data = request.data
        if isinstance(_data, list):
            datas = _data
        elif isinstance(_data, dict):
            datas = list(_data)

        try:
            for data_dict in datas:
                self.create_data(data_dict)
        except ValueError as err:
            return Response(str(err), status=status.HTTP_400_BAD_REQUEST)
        except Exception as err:
            return Response(str(err), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(datas, status=status.HTTP_201_CREATED)


class DataRetrieveUpdateAPIView(DataAPIView):

    def get(self, request, name, pk, format=None):
        # 查询 data 和 labels 对象
        datas, labels_dict = self.get_datas_and_labels_dict(
            request.GET, name, pk, format=format)

        # 从查询结果列表中取出第一个查询结果
        json_objs = self.serialized_datas(datas, labels_dict)
        json_obj = json_objs[0] if len(json_objs) > 0 else {}

        return Response(json_obj)
