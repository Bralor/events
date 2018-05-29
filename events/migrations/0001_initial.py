# Generated by Django 2.0.5 on 2018-05-29 08:40

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField(max_length=200)),
                ('location', models.CharField(max_length=500)),
                ('category', models.CharField(max_length=20)),
            ],
        ),
    ]
