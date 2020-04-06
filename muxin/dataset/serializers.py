from rest_framework import serializers
from .models import *

__all__ = ['DataSetSerializer', 'ImageSerializer', 'VideoSerializer',
           'ImageLabelSerializer', 'VideoLabelSerializer']


class DataSetSerializer(serializers.ModelSerializer):

    class Meta:
        model = DataSet
        fields = ['id', 'name', 'type', 'create', 'modify']


class ImageLabelSerializer(serializers.ModelSerializer):

    class Meta:
        model = ImageLabel
        fields = ['label']


class ImageSerializer(serializers.ModelSerializer):

    labels = ImageLabelSerializer(many=True)

    class Meta:
        model = Image
        fields = ['md5', 'path', 'size', 'time', 'labels',
                  'width', 'height', 'marker', 'dataset']

    def create(self, validated_data):
        labels_data = validated_data.pop('labels')
        image = Image.objects.create(**validated_data)
        for label_data in labels_data:
            ImageLabel.objects.create(image=image, **label_data)
        return image

    def update(self, instance, validated_data):
        if 'labels' in validated_data:
            labels_data = validated_data.pop('labels')
        else:
            labels_data = {}

        instance = super().update(instance, validated_data)
        for label_data in labels_data:
            ImageLabel.objects.update_or_create(image=instance, **label_data)
        return instance


class VideoLabelSerializer(serializers.ModelSerializer):

    class Meta:
        model = VideoLabel
        fields = ['label']


class VideoSerializer(serializers.ModelSerializer):

    labels = VideoLabelSerializer(many=True)

    class Meta:

        model = Video
        fields = ['vid', 'path', 'size', 'time', 'labels',
                  'marker', 'dataset']

    def create(self, validated_data):
        labels_data = validated_data.pop('labels')
        video = Video.objects.create(**validated_data)
        for label_data in labels_data:
            VideoLabel.objects.create(video=video, **label_data)
        return video

    def update(self, instance, validated_data):
        if 'labels' in validated_data:
            labels_data = validated_data.pop('labels')
        else:
            labels_data = {}

        instance = super().update(instance, validated_data)
        for label_data in labels_data:
            VideoLabel.objects.update_or_create(video=instance, **label_data)
        return instance
