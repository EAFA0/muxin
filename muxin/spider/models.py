from django.db import models

# Create your models here.


class Task(models.Model):

    name = models.CharField(max_length=32, primary_key=True)

    args = models.FileField()
    last = models.DateTimeField(auto_now=True)
    create = models.DateTimeField(auto_now_add=True)


class Spider(models.Model):

    id = models.CharField(max_length=32, primary_key=True)
    task = models.CharField(max_length=32, db_index=True)

    status = models.CharField(max_length=1)
    spider = models.CharField(max_length=64)
    project = models.CharField(max_length=64)
