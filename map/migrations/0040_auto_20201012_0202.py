# Generated by Django 3.1.1 on 2020-10-11 19:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('map', '0039_kategoriproduksi'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='KategoriProduksi',
            new_name='KategoriPsu',
        ),
        migrations.AlterModelOptions(
            name='kategoripsu',
            options={'verbose_name': 'Kategori PSU', 'verbose_name_plural': 'Kategori Psu'},
        ),
    ]
