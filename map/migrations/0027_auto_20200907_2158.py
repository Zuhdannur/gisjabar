# Generated by Django 3.1.1 on 2020-09-07 14:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('map', '0026_auto_20200907_2157'),
    ]

    operations = [
        migrations.AlterField(
            model_name='desapsuprofile',
            name='rth_category',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='map.rthcategory'),
        ),
    ]
