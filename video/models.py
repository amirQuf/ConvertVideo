from django.db import models

class Video(models.Model):
    video = models.FileField(upload_to='video')
    url_240p = models.CharField(max_length=200 ,null=True ,blank =True)
    url_360p = models.CharField(max_length=200 ,null=True ,blank =True)
    time_to_convert = models.FloatField(default = 0)

