# Generated by Django 3.0.8 on 2020-09-05 00:54

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('map', '0021_auto_20200903_2106'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='desaprofile',
            name='base_map',
        ),
        migrations.AddField(
            model_name='desaprofile',
            name='city',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.PROTECT, to='map.CityProfile'),
        ),
        migrations.AddField(
            model_name='desaprofile',
            name='geojson',
            field=models.FileField(default='settings.MEDIA_ROOT/logos/anonymous.jpg', upload_to='maps/city/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['geojson'])]),
        ),
    ]
