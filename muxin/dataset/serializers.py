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


class LabelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Label
        fields = ['dataset', 'label', 'data']
