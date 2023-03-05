from time import perf_counter

import ffmpeg
from celery import shared_task
from django.conf import settings

from .models import Video


@shared_task
def convert(id):
    start_time = perf_counter()
    instance = Video.objects.get(id=id)
    video_path = instance.video.path   
    video_name = re.search(r'\/((.+))\.mp4',video_path).group(1)
    output_name_240 = f'media/video_240/{video_name}_240.mp4'   
    output_name_360 = f'media/video_360/{video_name}_360.mp4'
    
    ffmpeg_cmd_240= (
        ffmpeg
        .input(video_path)
        .output(output_name_240,bitrate='500k',resolution ='420x240')
    )
    ffmpeg_cmd_240.run()

    ffmpeg_cmd_360= (
        ffmpeg
        .input(video_path)
        .output(output_name_360 ,bitrate='500k',resolution ='640x360')
    )
    ffmpeg_cmd_360.run()
    
    instance.url_240 =  settings.MEDIA_ROOT+ f"/video_240/{video_name}.mp4"
    instance.url_360 = settings.MEDIA_ROOT+ f"/video_360/{video_name}.mp4"
    stop_time = perf_counter()
    delta_time = stop_time - start_time
    instance.time_to_convert = delta_time
    instance.save()
    return instance
