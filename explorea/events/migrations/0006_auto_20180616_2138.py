# Generated by Django 2.0.5 on 2018-06-16 19:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0005_remove_eventrun'),
    ]

    operations = [
        migrations.CreateModel(
            name='EventRun',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('time', models.TimeField()),
                ('seats_available', models.PositiveIntegerField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.AlterField(
            model_name='event',
            name='category',
            field=models.CharField(choices=[('FN', 'fun'), ('RX', 'relax'), ('EX', 'experience'), ('SI', 'sights')], default='FN', max_length=20),
        ),
        migrations.AlterField(
            model_name='event',
            name='description',
            field=models.TextField(max_length=1000),
        ),
        migrations.AddField(
            model_name='eventrun',
            name='event',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='events.Event'),
        ),
    ]
