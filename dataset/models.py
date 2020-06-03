from django.db import models

# Create your models here.
__all__ = ['DataSet', 'Data', 'Label']


class DataSet(models.Model):

    type = models.CharField(max_length=1)
    name = models.CharField(max_length=64, primary_key=True)

    create = models.DateTimeField(auto_now_add=True)
    modify = models.DateTimeField(auto_now=True)


class Data(models.Model):

    md5 = models.CharField(max_length=32, primary_key=True)

    path = models.CharField(max_length=512)
    time = models.DateTimeField(auto_now=True)

    marker = models.FileField(null=True)
    source = models.CharField(max_length=512)


class Label(models.Model):

    dataset = models.CharField(max_length=64, db_index=True)
    label = models.CharField(max_length=64, db_index=True)
    data = models.CharField(max_length=32)
