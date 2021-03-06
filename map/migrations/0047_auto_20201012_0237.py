# Generated by Django 3.1.1 on 2020-10-11 19:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('map', '0046_auto_20201012_0218'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='psuprofile',
            options={'verbose_name': 'Profil Desa PSU', 'verbose_name_plural': 'Profil Desa PSU'},
        ),
        migrations.RemoveField(
            model_name='psuprofile',
            name='address',
        ),
        migrations.RemoveField(
            model_name='psuprofile',
            name='nama_psu',
        ),
        migrations.RemoveField(
            model_name='psuprofile',
            name='planning',
        ),
        migrations.RemoveField(
            model_name='psuprofile',
            name='urban_area',
        ),
        migrations.AlterField(
            model_name='psuprofile',
            name='desa',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.PROTECT, to='map.mapdesa'),
        ),
    ]
