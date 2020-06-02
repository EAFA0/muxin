from django.db import models


class Task(models.Model):

    name = models.CharField(max_length=32, primary_key=True)
    config = models.FileField(upload_to="task/configs/")
    dataset = models.CharField(max_length=64)

    last = models.DateTimeField(auto_now=True)
    create = models.DateTimeField(auto_now_add=True)


class Spider(models.Model):

    id = models.CharField(max_length=32, primary_key=True)
    task = models.ForeignKey(Task, models.CASCADE, related_name='spiders')

    name = models.CharField(max_length=64)
    project = models.CharField(max_length=64)
