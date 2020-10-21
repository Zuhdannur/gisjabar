import os, datetime
from django.db import models
from django.core import validators as V
from django.template.defaultfilters import slugify

from ckeditor_uploader.fields import RichTextUploadingField


# Create your models here.
class ImageSlider(models.Model):
    image = models.FileField(
        upload_to='uploads/%Y/%m/%d/',
        validators=[V.FileExtensionValidator(allowed_extensions=['jpg', 'png', 'gif'])]
    )
    caption = models.CharField(max_length=200)
    description = RichTextUploadingField(null=True, blank=True)

    class Meta:
        verbose_name = 'Slide Show'
        verbose_name_plural = 'Daftar Slide Show'


class Gallery(models.Model):
    def get_upload_path(self, filename):
        now = datetime.datetime.now()
        path = "galleries/%s/%s/%s" % (now.year, now.month, now.day)
        name, ext = os.path.splitext(filename)
        return os.path.join(path, slugify(name) + ext)

    filename = models.FileField(
        upload_to=get_upload_path,
        validators=[V.FileExtensionValidator(allowed_extensions=['jpg', 'png', 'gif'])]
    )
    caption = models.CharField(max_length=200)
    description = models.TextField(null=True)

    class Meta:
        verbose_name = 'Galeri Foto'
        verbose_name_plural = 'Galeri Foto'


class Map(models.Model):
    name = models.CharField(max_length=200, unique=True)
    geojson = models.FileField(
        upload_to='maps/city/',
        validators=[V.FileExtensionValidator(allowed_extensions=['geojson'])]
    )

    class Meta:
        verbose_name = 'Peta Dasar'
        verbose_name_plural = 'Daftar Peta Dasar'

    def __str__(self):
        return self.name


class JenisPsu(models.Model):
    kategori = models.ForeignKey('KategoriPsu', on_delete=models.PROTECT)
    name = models.CharField(max_length=20, unique=True)
    icon = models.FileField(
        upload_to='maps/icon/rth-category',
        validators=[V.FileExtensionValidator(allowed_extensions=['png', 'ico'])]
    )

    class Meta:
        verbose_name = 'Jenis PSU'
        verbose_name_plural = 'Jenis PSU'

    def __str__(self):
        return self.name


class CityProfile(models.Model):
    base_map = models.ForeignKey('Map', on_delete=models.PROTECT)
    name = models.CharField(max_length=200)
    area = models.FloatField()
    population = models.IntegerField(
        validators=[V.MinValueValidator(0)]
    )
    website = models.CharField(max_length=30, blank=True, null=True)
    description = RichTextUploadingField(null=True, blank=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    icon = models.FileField(
        upload_to='maps/icon/city-profile',
        validators=[V.FileExtensionValidator(allowed_extensions=['png', 'ico'])]
    )

    class Meta:
        verbose_name = 'Profil Kecamatan'
        verbose_name_plural = 'Profil Kecamatan'

    def __str__(self):
        return self.name


class CityRthProfile(models.Model):
    base_map = models.ForeignKey('Map', on_delete=models.PROTECT)
    city = models.CharField(max_length=200)
    area = models.FloatField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    description = RichTextUploadingField(null=True, blank=True)

    class Meta:
        verbose_name = 'Profil PSU Kecamatan'
        verbose_name_plural = 'Profil PSU Kecamatan'

    def __str__(self):
        return self.city


class Regulation(models.Model):
    filename = models.FileField(
        upload_to='uploads/%Y/%m/%d/',
        validators=[V.FileExtensionValidator(allowed_extensions=['doc', 'docx', 'pdf'])]
    )
    title = models.CharField(max_length=200)

    class Meta:
        verbose_name = 'Download'
        verbose_name_plural = 'Download'


class Article(models.Model):
    title = models.CharField(max_length=200)
    content = RichTextUploadingField()

    class Meta:
        verbose_name = 'Artikel'
        verbose_name_plural = 'Artikel'


class Page(models.Model):
    code = models.SlugField(max_length=100, unique=True)
    title = models.CharField(max_length=200)
    content = RichTextUploadingField()

    class Meta:
        verbose_name = 'Kontak'
        verbose_name_plural = 'Kontak'


class DataProcessing(models.Model):
    title = models.CharField(max_length=200)
    description = RichTextUploadingField()

    class Meta:
        verbose_name = 'Olah Data'
        verbose_name_plural = 'Olah Data'


class DesaProfile(models.Model):
    name = models.CharField(max_length=200)
    area = models.FloatField()
    population = models.IntegerField(
        validators=[V.MinValueValidator(0)]
    )
    geojson = models.FileField(
        upload_to='maps/desa/',
        validators=[V.FileExtensionValidator(allowed_extensions=['geojson'])],
        default='settings.MEDIA_ROOT/logos/anonymous.jpg'
    )
    color = models.CharField(max_length=200, default='#abeb34')
    city = models.ForeignKey('CityProfile', on_delete=models.PROTECT, default=0)
    website = models.CharField(max_length=30, blank=True, null=True)
    description = RichTextUploadingField(null=True, blank=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    icon = models.FileField(
        upload_to='maps/icon/desa',
        validators=[V.FileExtensionValidator(allowed_extensions=['png', 'ico'])]
    )

    class Meta:
        verbose_name = 'Profil Desa'
        verbose_name_plural = 'Profil Desa'

    def __str__(self):
        return self.name


class MapDesa(models.Model):
    name = models.CharField(max_length=200, unique=True)
    geojson = models.FileField(
        upload_to='maps/dasar-desa/',
        validators=[V.FileExtensionValidator(allowed_extensions=['geojson'])]
    )
    color = models.CharField(max_length=200, default='#abeb34')
    latitude = models.FloatField(default=0)
    longitude = models.FloatField(default=0)

    class Meta:
        verbose_name = 'Peta Dasar KSK'
        verbose_name_plural = 'Daftar Peta Dasar KSK'

    def __str__(self):
        return self.name


class PsuProfile(models.Model):
    desa = models.ForeignKey('MapDesa', on_delete=models.PROTECT, default=0)
    kategori_psu = models.ForeignKey('KategoriPsu', on_delete=models.PROTECT, default=0)
    jenis_psu = models.ForeignKey('JenisPsu', on_delete=models.PROTECT, default=0)
    latitude = models.FloatField()
    longitude = models.FloatField()
    icon = models.FileField(
        upload_to='maps/icon/desa-psu',
        validators=[V.FileExtensionValidator(allowed_extensions=['png', 'ico'])]
    )
    description = RichTextUploadingField(null=True, blank=True)

    class Meta:
        verbose_name = 'Profil KSK PSU'
        verbose_name_plural = 'Profil KSK PSU'

    def __str__(self):
        return self.desa.name


class KategoriPsu(models.Model):
    nama_kategori = models.CharField(max_length=200, default='')

    class Meta:
        verbose_name = 'Kategori PSU'
        verbose_name_plural = 'Kategori Psu'

    def __str__(self):
        return self.nama_kategori
