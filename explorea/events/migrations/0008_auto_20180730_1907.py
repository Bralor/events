# Generated by Django 2.0.5 on 2018-07-30 17:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0007_auto_20180730_0904'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='eventrun',
            options={'ordering': ['date', 'time']},
        ),
        migrations.AlterField(
            model_name='event',
            name='slug',
            field=models.SlugField(max_length=200, null=True, unique=True),
        ),
    ]