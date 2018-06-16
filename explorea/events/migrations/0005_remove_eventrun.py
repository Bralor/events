from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):
	dependencies = [
        ('events', '0004_auto_20180604_1457'),
    				]

	operations = [
        migrations.DeleteModel(
           name='eventrun',
        						),
    				]