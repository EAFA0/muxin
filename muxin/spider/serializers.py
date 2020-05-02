import json
from scrapyd_api import ScrapydAPI
from rest_framework import serializers

from .models import Task, Spider
from muxin.settings import CRAWLER_URL


__all__ = ['TaskSerializer']


class TaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = ['name', 'args', 'last', 'create']


class SpiderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Spider
        fields = ['id', 'task', 'status', 'spider', 'project']


    def create(self, validated_data):
        args_list = ['name', 'args']
        args = json.loads(validated_data['args'])

        spiders = args['spiders']
        files = args['files']
        for filename in files:
            breakpoint()



        task = Task.objects.create(**validated_data)
        return task
