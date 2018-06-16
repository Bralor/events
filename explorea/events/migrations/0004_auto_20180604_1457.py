from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):
    dependencies = [
        ('events', '0003_event_host'),
                    ]

    operations = [
        migrations.RenameField(
            model_name='eventrun',
            old_name='happens',
            new_name='date'
                                ),
        migrations.AddField(
            model_name='eventrun',
            name='time',
            field=models.TimeField(default=django.utils.timezone.now),
            preserve_default=False,
                            ),
                    ]
