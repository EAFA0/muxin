from rest_framework import serializers
from .models import DataSet, Data, Label


class DataSetSerializer(serializers.ModelSerializer):

    class Meta:
        model = DataSet
        fields = ['name', 'type', 'create', 'modify']


class DataSerializer(serializers.ModelSerializer):

    class Meta:
        model = Data
        fields = ['md5', 'path', 'time', 'marker', 'source']


class LabelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Label
        fields = ['dataset', 'label', 'data']
