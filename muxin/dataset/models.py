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

    path = models.CharField(max_length=512)
    size = models.IntegerField()
    time = models.DateTimeField(auto_now=True)

    marker = models.FileField(null=True)
    dataset = models.CharField(max_length=64, db_index=True)


class ImageLabel(models.Model):
    # image 字段保存 image 的主键 id
    image = models.ForeignKey(Image, models.CASCADE, to_field='md5',
                              related_name='labels', related_query_name='label')
    label = models.CharField(max_length=64, db_index=True)

    # class Meta:
        # unique_together = ('image', 'label')
        # ordering = ['label']

    def __unicode__(self):
        return self.label


class Video(models.Model):

    vid = models.CharField(max_length=32, primary_key=True)

    path = models.CharField(max_length=512)
    size = models.IntegerField()
    time = models.DateTimeField(auto_now=True)

    marker = models.FileField()
    dataset = models.CharField(max_length=64, db_index=True)


class VideoLabel(models.Model):

    video = models.ForeignKey(Video, models.CASCADE,
                              related_name='labels', related_query_name='label')
    label = models.CharField(max_length=64, db_index=True)

    def __unicode__(self):
        return self.label