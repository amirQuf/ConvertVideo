from  django.db.models.signals import post_save
from    .models import Video  
from django.dispatch import receiver

from .tasks import convert

@receiver(post_save,sender = Video)
def calling_Convert_task(sender , instance,created,**kargs):
    if created:
        print(instance.id)
        convert.delay(instance.id)

