import json
from scrapyd_api import ScrapydAPI
from rest_framework import serializers

from .models import Task, Spider


class SpiderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Spider
        fields = ['id', 'name', 'task', 'project']


class TaskSerializer(serializers.ModelSerializer):

    spiders = SpiderSerializer(read_only=True, many=True)

    class Meta:
        model = Task
        fields = ['name', 'config', 'dataset', 'last', 'create', 'spiders']
