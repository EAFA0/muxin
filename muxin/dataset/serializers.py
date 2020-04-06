from rest_framework import serializers
from .models import *

__all__ = ['DataSetSerializer', 'ImageSerializer', 'VideoSerializer',
           'ImageLabelSerializer', 'VideoLabelSerializer']


class DataSetSerializer(serializers.ModelSerializer):

    class Meta:
        model = DataSet
        fields = ['id', 'name', 'type', 'create', 'modify', 'creator']


class ImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Image
        fields = ['md5', 'path', 'size', 'width',
                  'store', 'marker', 'height', 'dataset']


class VideoSerializer(serializers.ModelSerializer):

    class Meta:

        model = Video
        fields = ['sid', 'path', 'size', 'store', 'marker', 'dataset']


class ImageLabelSerializer(serializers.ModelSerializer):

    class Meta:
        model = ImageLabel
        fields = ['id', 'image', 'label']


class VideoLabelSerializer(serializers.ModelSerializer):

    class Meta:
        model = VideoLabel
        fields = ['id', 'video', 'label']
