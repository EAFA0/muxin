from django.db import models

# Create your models here.


class Task(models.Model):

    name = models.CharField(max_length=32, primary_key=True)
    dataset = models.CharField(max_length=64)

    args = models.FileField()
    last = models.DateTimeField(auto_now=True)
    create = models.DateTimeField(auto_now_add=True)
    


class Spider(models.Model):

    id = models.CharField(max_length=32, primary_key=True)
    task = models.CharField(max_length=32, db_index=True)

    name = models.CharField(max_length=64)
    status = models.CharField(max_length=1)
    project = models.CharField(max_length=64)
