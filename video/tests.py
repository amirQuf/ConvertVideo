from django.test import TestCase
from .models import Video 
import pytest
import redis
import os
import subprocess

def is_redis_available(host='localhost', port=6379):
    try:
        client = redis.StrictRedis(host=host, port=port, db=0)

        client.ping()
        return True
    except redis.ConnectionError:
        return False

def test_redis_availability():
   
    assert is_redis_available(), "Redis is not available. Please ensure it is running and accessible."


def is_ffmpeg_installed():
    try:
        # اجرای دستور ffmpeg -version و بررسی خروجی آن
        subprocess.run(['ffmpeg', '-version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        return True
    except subprocess.CalledProcessError:
        return False

@pytest.mark.parametrize("input_quality, output_quality", [("source.mp4", "240"), ("source.mp4", "360")])
def test_ffmpeg_quality_conversion(input_quality, output_quality):
    # بررسی وجود ffmpeg
    assert is_ffmpeg_installed(), "FFmpeg is not installed or accessible. Please ensure it is properly installed."

    # دستور تبدیل کیفیت با ffmpeg
    input_file = os.path.join("path_to_test_files", input_quality)
    output_file = os.path.join("path_to_test_files", f"output_{output_quality}.mp4")
    ffmpeg_cmd = f"ffmpeg -i {input_file} -vf scale={output_quality}:-1 -c:v libx264 -c:a copy {output_file}"

    try:
        # اجرای دستور تبدیل با ffmpeg
        subprocess.run(ffmpeg_cmd, shell=True, check=True)
        # در اینجا می‌توانید اعتبارسنجی‌های دیگری انجام دهید، مانند بررسی اندازه و کیفیت فایل خروجی
        assert os.path.exists(output_file), f"FFmpeg conversion failed. Output file '{output_file}' not found."
    finally:
        # پاک کردن فایل خروجی برای تمیز کردن محیط تست
        if os.path.exists(output_file):
            os.remove(output_file)
