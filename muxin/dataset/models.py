from django.db import models

# Create your models here.
__all__ = ['DataSet', 'Image', 'Video',
           'ImageLabel', 'VideoLabel']


class DataSet(models.Model):

    type = models.CharField(max_length=1)
    name = models.CharField(max_length=64, db_index=True)

    create = models.DateTimeField(auto_now_add=True)
    modify = models.DateTimeField(auto_now=True)


class Image(models.Model):

    md5 = models.CharField(max_length=32, primary_key=True)

    path = models.FileField()
    size = models.IntegerField()
    time = models.DateTimeField(auto_now=True)

    width = models.IntegerField()
    height = models.IntegerField()

    marker = models.FileField()
    dataset = models.CharField(max_length=64, db_index=True)


class ImageLabel(models.Model):
    # image 字段保存 image 的主键 id
    image = models.CharField(max_length=32)
    label = models.CharField(max_length=64, db_index=True)


class Video(models.Model):

    sid = models.CharField(max_length=32, primary_key=True)

    path = models.FileField()
    size = models.IntegerField()
    time = models.DateTimeField(auto_now=True)

    marker = models.FileField()
    dataset = models.CharField(max_length=64, db_index=True)


class VideoLabel(models.Model):

    video = models.CharField(max_length=32)
    label = models.CharField(max_length=64, db_index=True)
