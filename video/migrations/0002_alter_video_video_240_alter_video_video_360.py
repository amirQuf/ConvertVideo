# Generated by Django 4.0.6 on 2022-07-25 10:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('video', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='video_240',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='video',
            name='video_360',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]
