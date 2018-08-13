# Generated by Django 2.0.5 on 2018-08-06 14:15

from django.db import migrations
import explorea.events.models
import imagekit.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0008_auto_20180730_1907'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='main_image',
            field=imagekit.models.fields.ProcessedImageField(null=True, upload_to=explorea.events.models.main_image_url),
        ),
        migrations.AddField(
            model_name='event',
            name='thumbnail',
            field=imagekit.models.fields.ProcessedImageField(null=True, upload_to=explorea.events.models.thumbnail_image_url),
        ),
    ]