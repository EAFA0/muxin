from django.db import models

# Create your models here.
__all__ = ['DataSet', 'Image', 'Video',
           'ImageLabel', 'VideoLabel']


class DataSet(models.Model):

    type = models.CharField(max_length=1)
    name = models.CharField(max_length=64)

    create = models.DateTimeField(auto_now_add=True)
    modify = models.DateTimeField(auto_now=True)
    creator = models.CharField(max_length=64)


class Image(models.Model):

    md5 = models.CharField(max_length=32, primary_key=True)

    path = models.FileField()
    size = models.IntegerField()
    width = models.IntegerField()
    store = models.DateTimeField(auto_now=True)

    marker = models.FileField()
    height = models.IntegerField()
    dataset = models.CharField(max_length=64)


class ImageLabel(models.Model):
    # image 字段保存 image 的主键 id
    image = models.CharField(max_length=32, primary_key=True)
    label = models.CharField(max_length=64)


class Video(models.Model):

    sid = models.CharField(max_length=32, primary_key=True)

    path = models.FileField()
    size = models.IntegerField()
    store = models.DateTimeField(auto_now=True)

    marker = models.FileField()
    dataset = models.CharField(max_length=64)


class VideoLabel(models.Model):

    video = models.CharField(max_length=32, primary_key=True)
    label = models.CharField(max_length=64)
