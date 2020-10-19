from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

from .models import *

from ckeditor.widgets import CKEditorWidget
from ckeditor_uploader.widgets import CKEditorUploadingWidget


def file_size_limit(value):
    limit = 25 * 1024
    if value.size > limit:
        raise ValidationError('File too large. Size should not exceed 25 KiB.')

def regulation_size_limit(value):
    limit = 1024 * 1024
    if value.size > limit:
        raise ValidationError('File too large. Size should not exceed 1 MB.')


class RthCategoryAdminForm(forms.ModelForm):
    kategori = forms.ModelChoiceField(
        label=_('Kategori PSU'),
        queryset=KategoriPsu.objects.all()
    )
    name = forms.CharField(label=_('Jenis Taman'), max_length=20)
    icon = forms.FileField(
        label=_('Ikon'),
        widget=forms.FileInput(attrs={'required': 'required'}),
        validators=[file_size_limit],
        help_text=_("File harus berupa <i>.png</i> atau <i>.ico</i>.<br/>")
    )

    class Meta:
        model = JenisPsu
        fields = ('kategori','name', 'icon')


class CityProfileAdminForm(forms.ModelForm):
    base_map = forms.ModelChoiceField(
        label=_('Peta Dasar'),
        queryset=Map.objects.all()
    )
    name = forms.CharField(label=_('Nama Kecamatan'), max_length=200)
    area = forms.FloatField(label=_('Luas Wilayah (Km)'), min_value=1.0)
    population = forms.IntegerField(label=_('Jumlah Penduduk'), min_value=0)
    website = forms.CharField(label=_('Website'), max_length=200, required=False)
    description = forms.CharField(
        required=False,
        widget=CKEditorUploadingWidget(
            attrs={'cols': 80, 'rows': 30}
        ),
    )
    icon = forms.FileField(
        label=_('Ikon'),
        widget=forms.FileInput(attrs={'required': 'required'}),
        validators=[file_size_limit],
        help_text=_("File harus berupa <i>.png</i> atau <i>.ico</i>.<br/>")
    )
    latitude = forms.FloatField(label=_('Latitude'), widget=forms.TextInput)
    longitude = forms.FloatField(label=_('Longitude'), widget=forms.TextInput)

    class Meta:
        model = CityProfile
        fields = ('name', 'area', 'population')

    def map_path(self):
        return self.base_map.geojson


class CityRthProfileAdminForm(forms.ModelForm):
    base_map = forms.ModelChoiceField(
        label=_('Peta Dasar'),
        queryset=Map.objects.all()
    )
    rth_category = forms.ModelChoiceField(
        label=_('Jenis PSU'),
        queryset=JenisPsu.objects.all()
    )
    city = forms.CharField(label=_('Nama Kecamatan'), max_length=200)
    urban_area = forms.CharField(label=_('Perkotaan'), max_length=200, required=False)
    name = forms.CharField(label=_('Nama PSU'), max_length=200)
    address = forms.CharField(label=_('Alamat Lokasi'), max_length=200)
    area = forms.FloatField(label=_('Luas (M)'), min_value=1.0)
    planning = forms.CharField(label=_('Perencanaan'), max_length=200, required=False)
    latitude = forms.FloatField(label=_('Latitude'), widget=forms.TextInput)
    longitude = forms.FloatField(label=_('Longitude'), widget=forms.TextInput)
    description = forms.CharField(
        required=False,
        widget=CKEditorUploadingWidget(
            attrs={'cols': 80, 'rows': 30}
        ),
    )

    class Meta:
        model = CityRthProfile
        fields = ('city', 'name', 'address')


class RegulationAdminForm(forms.ModelForm):
    filename = forms.FileField(
        label=_('Dokumen'),
        widget=forms.FileInput(attrs={'required': 'required'}),
        validators=[regulation_size_limit],
        help_text=_("File harus berupa <i>.doc</i>, <i>.docx</i> atau <i>.pdf</i>.<br/>")
    )
    title = forms.CharField(label=_('Judul Peraturan'), max_length=200)

    class Meta:
        model = Regulation
        fields = ('filename', 'title')


class ArticleAdminForm(forms.ModelForm):
    title = forms.CharField(label=_("Judul Artikel"))
    content = forms.CharField(
        widget=CKEditorUploadingWidget(
            attrs={'cols': 80, 'rows': 30}
        ),
    )

    class Meta:
        model = Article
        fields = ('title', 'content')


class GalleryAdminForm(forms.ModelForm):
    filename = forms.FileField(
        label=_('Upload Gambar'),
        widget=forms.FileInput(attrs={'required': 'required'}),
        validators=[regulation_size_limit],
        help_text=_("File harus berupa <i>.png</i>, <i>.jpg</i>, dan <i>.gif</i>.<br/>")
    )
    caption = forms.CharField(label=_('Judul'), max_length=200)
    description = forms.CharField(
        label=_('Deskripsi'),
        widget=forms.Textarea
    )

    class Meta:
        model = Gallery
        fields = ('filename', 'caption', 'description')


class DataProcessingAdminForm(forms.ModelForm):
    title = forms.CharField(label=_("Judul"))
    description = forms.CharField(
        label=_("Deskripsi"),
        widget=CKEditorUploadingWidget(
            attrs={'cols': 80, 'rows': 30}
        ),
    )

    class Meta:
        model = DataProcessing
        fields = ('title', 'description')


class DesaProfileAdminForm(forms.ModelForm):
    geojson = forms.ModelChoiceField(
        label=_('Peta Dasar'),
        queryset=Map.objects.all()
    )
    name = forms.CharField(label=_('Nama Kecamatan'), max_length=200)
    area = forms.FloatField(label=_('Luas Wilayah (Km)'), min_value=1.0)
    population = forms.IntegerField(label=_('Jumlah Penduduk'), min_value=0)
    website = forms.CharField(label=_('Website'), max_length=200, required=False)
    description = forms.CharField(
        required=False,
        widget=CKEditorUploadingWidget(
            attrs={'cols': 80, 'rows': 30}
        ),
    )
    icon = forms.FileField(
        label=_('Ikon'),
        widget=forms.FileInput(attrs={'required': 'required'}),
        validators=[file_size_limit],
        help_text=_("File harus berupa <i>.png</i> atau <i>.ico</i>.<br/>")
    )
    latitude = forms.FloatField(label=_('Latitude'), widget=forms.TextInput)
    longitude = forms.FloatField(label=_('Longitude'), widget=forms.TextInput)

    class Meta:
        model = CityProfile
        fields = ('name', 'area', 'population')

    def map_path(self):
        return self.base_map.geojson

