from django.contrib import admin
from django.core.exceptions import PermissionDenied
from django.urls import reverse, re_path
from django.utils.html import format_html
from django.shortcuts import render
from django.template import RequestContext

# Register your models here.
from .models import *
from .forms import *
from .views import get_area_percentage


class ImageSliderAdmin(admin.ModelAdmin):
    list_display = ('id', 'image', 'caption')


class MapAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'geojson')


class RthCategoryAdmin(admin.ModelAdmin):
    form = RthCategoryAdminForm

    list_display = ('id', 'kategori', 'name', 'icon')

    ordering = ('id', 'name', 'icon')

    search_fields = ('name',)


class CityProfileAdmin(admin.ModelAdmin):
    form = CityProfileAdminForm

    list_display = ('id', 'name', 'area', 'population', 'latitude', 'longitude', 'chart_actions')
    ordering = ('name', 'population', 'area')

    fieldsets = [
        ("General", {'fields': ['base_map', 'name', 'area', 'population']}),
        ("Info", {'fields': ['website', 'description']}),
        ("Coordinate", {'fields': ['icon', 'latitude', 'longitude']}),
    ]

    search_fields = ['name', 'area', 'population']

    def view_chart(self, request, pk, *args, **kwargs):
        cp = CityProfile.objects.get(pk=pk)
        persentage_area = get_area_percentage(cp)

        context = {
            'title': 'Chart %s' % cp.name,
            'opts': self.model._meta,
            'rth_area': persentage_area[0],
            'city_area': persentage_area[1]
        }

        return render(request, 'admin/city_chart.html', context)

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            re_path(
                r'^(?P<pk>.+)/chart/$',
                self.admin_site.admin_view(self.view_chart),
                name='chart',
            ),
        ]
        return custom_urls + urls

    def chart_actions(self, obj):
        return format_html(
            '<a class="viewlink" href="{}">Chart</a>&nbsp;',
            reverse('admin:chart', args=[obj.pk]),
        )

    chart_actions.short_description = '-'
    chart_actions.allow_tags = True

    def change_view(self, request, object_id, form_url='', extra_context=None):
        if not request.user.is_superuser and \
                not CityProfile.objects.get(pk=object_id).name.lower() == request.user.profile.city.lower():
            raise PermissionDenied

        return self.changeform_view(request, object_id, form_url, extra_context)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs

        return qs.filter(name=request.user.profile.city)


class CityRthProfileAdmin(admin.ModelAdmin):
    form = CityRthProfileAdminForm

    list_display = ('id', 'city', 'area', 'latitude', 'longitude')
    ordering = ('city', 'area')

    fieldsets = [
        ("General", {'fields': ['base_map', 'city']}),
        ("RTH", {'fields': ['description']}),
        ("Coordinate", {'fields': ['latitude', 'longitude']}),
    ]

    list_filter = ['city']

    search_fields = ['name', 'city', 'latitude', 'longitude']

    def change_view(self, request, object_id, form_url='', extra_context=None):
        if not request.user.is_superuser and \
                not CityProfile.objects.get(pk=object_id).name.lower() == request.user.profile.city.lower():
            raise PermissionDenied

        return self.changeform_view(request, object_id, form_url, extra_context)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs

        return qs.filter(city=request.user.profile.city)


class RegulationAdmin(admin.ModelAdmin):
    form = RegulationAdminForm

    list_display = ('id', 'filename')


class ArticleAdmin(admin.ModelAdmin):
    form = ArticleAdminForm

    list_display = ('id', 'title')


class GalleryAdmin(admin.ModelAdmin):
    form = GalleryAdminForm

    list_display = ('id', 'filename', 'caption')

    ordering = ('id', 'filename')

    search_fields = ['filename', 'caption', 'description']


class PageAdmin(admin.ModelAdmin):
    list_display = ('id', 'code', 'title')

    ordering = ('id', 'code', 'title')

    search_fields = ('code', 'title')


class DataProcessingAdmin(admin.ModelAdmin):
    form = DataProcessingAdminForm

    list_display = ('id', 'title', 'description')

    ordering = ('id', 'title')

    search_fields = ('id', 'description', 'title')


class DesaProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'geojson')


class MapDesaAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'geojson')


class PsuProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'desa','kategori_psu','jenis_psu','longitude','latitude')

    class Media:
        js = ('default/js/kategori-filter.js',)


class KategoriPsuAdmin(admin.ModelAdmin):
    list_display = ('id', 'nama_kategori')


admin.site.register(ImageSlider, ImageSliderAdmin)
# admin.site.register(Map, MapAdmin)
admin.site.register(JenisPsu, RthCategoryAdmin)
# admin.site.register(CityProfile, CityProfileAdmin)
# admin.site.register(CityRthProfile, CityRthProfileAdmin)
admin.site.register(Regulation, RegulationAdmin)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Gallery, GalleryAdmin)
admin.site.register(Page, PageAdmin)
admin.site.register(DataProcessing, DataProcessingAdmin)
# admin.site.register(DesaProfile, DesaProfileAdmin)
admin.site.register(MapDesa, MapDesaAdmin)
admin.site.register(PsuProfile, PsuProfileAdmin)
admin.site.register(KategoriPsu, KategoriPsuAdmin)
