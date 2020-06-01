from rest_framework import serializers
from .models import *

__all__ = ['DataSetSerializer', 'DataSerializer', 'LabelSerializer']


class DataSetSerializer(serializers.ModelSerializer):

    class Meta:
        model = DataSet
        fields = ['name', 'type', 'create', 'modify']



class DataSerializer(serializers.ModelSerializer):

    class Meta:
        model = Data
        fields = ['md5', 'path', 'size', 'time', 'marker']

    def create(self, validated_data):
        # 标签是一个列表字段
        labels = validated_data.pop('labels')
        # 数据集名字和描述信息一块传递
        dataset = validated_data.pop('dataset')
        data = Data.objects.create(**validated_data)

        # 创建标签数据
        for label in labels:
            Label.objects.create(dataset=dataset, label=label)
        return data

    # 该函数似乎还没有完成，历史有点久远不是很清楚
    def update(self, instance, validated_data):
        dataset = validated_data.pop('dataset')
        if 'labels' in validated_data:
            labels = validated_data.pop('labels')
        else:
            labels = {}

        instance = super().update(instance, validated_data)
        for label in labels:
            Label.objects.update_or_create(dataset=dataset, label=label)
        return instance


class LabelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Label
        fields = ['dataset', 'label']
