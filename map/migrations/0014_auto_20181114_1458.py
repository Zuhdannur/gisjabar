# Generated by Django 2.1.2 on 2018-11-14 14:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('map', '0013_auto_20181114_1455'),
    ]

    operations = [
        migrations.AddField(
            model_name='page',
            name='title',
            field=models.CharField(default='Kontak', max_length=200),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='page',
            name='code',
            field=models.SlugField(max_length=100, unique=True),
        ),
    ]
