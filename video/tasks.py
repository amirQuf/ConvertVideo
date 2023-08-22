from time import perf_counter
import ffmpeg
import re
from celery import shared_task
from django.conf import settings
from .models import Video

class VideoUtils:
    @staticmethod
    def generate_ffmpeg_cmd(video_path, output_name):
        return (
            ffmpeg
            .input(video_path)
            .output(output_name, bitrate='500k', resolution ='420x240' if "240" in output_name else '640x360')
        )

    @staticmethod
    def save_and_remove_files(instance, output_name, video_name):
        with open(output_name, 'rb') as file:
            instance.video_240.save(f"{video_name}_240.mp4", File(file)) if "240" in output_name else instance.video_360.save(f"{video_name}_360.mp4", File(file))
        os.remove(output_name)


@shared_task
def convert(id):
    start_time = perf_counter()
    try:
        instance = Video.objects.get(id=id)
    except Video.DoesNotExist:
        return None

    video_path = instance.video.path   
    video_name = re.search(r'\/((.+))\.mp4',video_path).group(1)
    resolutions = ["240", "360"]
    for resolution in resolutions:
        output_name = f'media/video_{resolution}/{video_name}_{resolution}.mp4'
        instance.url =  settings.MEDIA_ROOT + f"/video_{resolution}/{video_name}.mp4"
        ffmpeg_cmd = VideoUtils.generate_ffmpeg_cmd(video_path, output_name)
        ffmpeg_cmd.run()
        VideoUtils.save_and_remove_files(instance, output_name, video_name)

    stop_time = perf_counter()
    instance.time_to_convert = stop_time - start_time
    instance.save()
    return instance
