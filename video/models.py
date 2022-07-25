from django.db import models




class Video(models.Model):
    video = models.FileField(upload_to='video')
    video_240 = models.CharField(max_length=500, null= True , blank=True)
    video_360 = models.CharField(max_length=500, null= True , blank=True)
    time_to_convert = models.PositiveIntegerField(default = 0)
