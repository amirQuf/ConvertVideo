from celery import shared_task
from .models import Video
import ffmpeg
from django.conf import settings

@shared_task
def convert(id):
    instance = Video.objects.get(id=id)
    video_path = instance.video.path   
    video_name= instance.video.name[6:-4]

    stream = ffmpeg.input(video_path)
    stream_360 = stream.filter('scale',h = 360 ,w = 640)
    stream_360 = ffmpeg.output(stream_360,f'media/video_360/{video_name}.mp4')
    stream_240 = stream.filter('scale',h = 240 ,w = 426)
    ffmpeg.run(stream_360)
    stream_240 = ffmpeg.output(stream_240,f'media/video_240/{video_name}.mp4')
    ffmpeg.run(stream_240)
    instance.video_240 = settings.MEDIA_ROOT + f"/video_360/{video_name}.mp4"
    instance.video_360 = settings.MEDIA_ROOT + f"/video_360/{video_name}.mp4"
    instance.save()
    return video_path