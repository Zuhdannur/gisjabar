# Generated by Django 3.1.1 on 2020-09-07 14:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('map', '0025_desapsuprofile'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='cityrthprofile',
            options={'verbose_name': 'Profil PSU Kecamatan', 'verbose_name_plural': 'Profil PSU Kecamatan'},
        ),
        migrations.AddField(
            model_name='desapsuprofile',
            name='rth_category',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.PROTECT, to='map.rthcategory'),
        ),
    ]
