from django.test import TestCase
from .models import Video 

class Test_ffmpeg(TestCase):
    def test_exitance_of_ffmpeg(self):
        import ffmpeg
        assert ffmpeg

    def test_upload_file(self):
        video = Video(video ='media/video/fak.mp4')
        asert video.video_240 == 'media/video_240/fak.mp4'
        asert video.video_360 == 'media/video_360/fak.mp4'
        


