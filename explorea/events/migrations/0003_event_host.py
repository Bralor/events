from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('events', '0002_eventrun'),
                    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='host',
            field=models.ForeignKey(
                default=1, 
                on_delete=django.db.models.deletion.CASCADE, 
                to=settings.AUTH_USER_MODEL),
            preserve_default=False,
                            ),
                    ]