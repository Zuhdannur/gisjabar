from django.db.models import Sum
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.template import loader
from django.views.decorators.csrf import ensure_csrf_cookie

from .models import *


# Create your views here.
def get_area_percentage(city):
    rth = CityRthProfile.objects.filter(city=city.name).aggregate(Sum('area'))
    if rth:
        try:
            rth_area = round((rth['area__sum'] / city.area) * 100, 2)
            city_area = 100 - rth_area
            return [rth_area, city_area]
        except:
            pass

    return [0, 100]


def index(request):
    images = ImageSlider.objects.all()
    context = {
        'name': "Riki Hidayat",
        'images': images,
    }

    return render(request, 'map/index.html', context)


def slider_article(request, model_id):
    image_slider = ImageSlider.objects.get(pk=model_id)

    context = {
        'image_slider': image_slider
    }

    return render(request, 'map/slider_article.html', context)


@ensure_csrf_cookie
def profile_city(request):
    cities = CityProfile.objects.all()
    context = {
        'cities': cities,
    }

    return render(request, 'map/profile_city.html', context)


def profile_city_view(request, model_id):
    if model_id == 0:
        context = {'many': True, 'data': []}
        for city in CityProfile.objects.all():
            context['data'].append({
                'geojson': city.base_map.geojson.url,
                'icon': city.icon.url,
                'attribute': {
                    'Nama': city.name,
                    'Luas Wilayah': city.area,
                    'Jumlah Penduduk': city.population,
                    'Website': city.website,
                    'Deskripsi': city.description
                },
                'center': [city.latitude, city.longitude],
                'area': get_area_percentage(city),
            })
    else:
        city = CityProfile.objects.get(pk=model_id)

        context = {
            'geojson': city.base_map.geojson.url,
            'icon': city.icon.url,
            'attribute': {
                'Nama': city.name,
                'Luas Wilayah': city.area,
                'Jumlah Penduduk': city.population,
                'Website': city.website,
                'Deskripsi': city.description
            },
            'center': [city.latitude, city.longitude],
            'area': get_area_percentage(city),
            'many': False,
        }

    return JsonResponse(context)


def map_rth(data):
    return {
        'geojson': data.base_map.geojson.url,
        'icon': data.rth_category.icon.url,
        'id': data.id,
        'attribute': {
            'Nama Kecamatan': data.city,
            'Desa': data.urban_area,
            'Nama PSU': data.name,
            'Alamat Lokasi': data.address,
            'Jenis': data.rth_category.name,
            'Luas PSU': data.area,
            'Planning': data.planning,
            'Deskripsi': data.description
        },
        'center': [data.latitude, data.longitude]
    }


def profile_rth(request):
    cprofs = MapDesa.objects.all()
    jenis = JenisPsu.objects.all()
    categories = KategoriPsu.objects.all()
    context = {
        'cities': set([obj for obj in cprofs]),
        'category': set([obj for obj in categories]),
        'jenis': set([obj for obj in jenis]),
        'cprofs': cprofs
    }

    return render(request, 'map/profile_rth.html', context)


def profile_rth_filter(request):
    if request.method == 'POST':
        dict_filter = {}
        if request.POST['rth-desa'].strip():
            dict_filter['id'] = request.POST['rth-desa'].strip()
        if request.POST['rth-category'].strip():
            dict_filter['rth_category_id'] = request.POST['rth-category'].strip()

        cprofs = PsuProfile.objects.filter(**dict_filter)
        context = {
            'data': [map_rth(obj) for obj in cprofs]
        }

        return JsonResponse(context)

    return JsonResponse("400: Bad Request")


def profile_rth_view(request, model_id):
    city = CityRthProfile.objects.get(pk=model_id)
    context = {
        'geojson': city.base_map.geojson.url,
        'icon': city.rth_category.icon.url,
        'attribute': {
            'Nama Kecamatan': city.city,
            'Desa': city.urban_area,
            'Nama PSU': city.name,
            'Alamat Lokasi': city.address,
            'Jenis': city.rth_category.name,
            'Luas PSU': city.area,
            'Planning': city.planning
        },
        'center': [city.latitude, city.longitude]
    }

    return JsonResponse(context)


def regulation(request):
    regulation = Regulation.objects.all()
    context = {
        'regulation': regulation,
    }

    return render(request, 'map/regulation.html', context)


def article(request):
    articles = Article.objects.all()
    context = {
        'articles': articles,
    }

    return render(request, 'map/article.html', context)


def article_view(request, model_id):
    article = Article.objects.get(pk=model_id)
    context = {
        'article': article,
    }

    return render(request, 'map/article_view.html', context)


def gallery(request):
    galleries = Gallery.objects.all()
    context = {
        'galleries': galleries,
    }

    return render(request, 'map/gallery.html', context)


def page_view(request, slug):
    page = Page.objects.get(code=slug)

    context = {
        'page': page
    }

    return render(request, 'map/page_view.html', context)


def get_desa(request):
    if request.method == 'POST':
        city_filter = {}
        if request.POST['city'].strip():
            city_filter = request.POST['city'].strip()

        city_filter = {
            'city_id': request.POST['city'].strip()
        }
        cprofs = MapDesa.objects.all().filter(kecamatan=request.POST['city'].strip())
        context = {
            'data': [map_desa(obj) for obj in cprofs]
        }

        return JsonResponse(context)

    return JsonResponse("400: Bad Request")


def map_desa(data):
    return {
        'geojson': data.geojson.name,
        'id': data.id,
        'attribute': {
            'nama': data.name,
            'warna': data.color
        },
        'center': [data.latitude, data.longitude]
    }


def map_desa_psu(data):
    cprofs = PsuProfile.objects.all().filter(desa_id=data.id)
    return {
        'geojson': data.geojson.name,
        'id': data.id,
        'attribute': {
            'nama': data.name,
            'color': data.color,
        },
        'detail': [detail_desa(obj) for obj in cprofs],
        # 'warna': data.color
        # 'center': [data.latitude, data.longitude]
    }


def detail_desa(data):
    return {
        'icon': data.icon.name,
        'kategori': data.kategori_psu_id,
        'jenis': data.jenis_psu_id,
        'attribute': {
            'deskripsi': data.description
        },
        'center': [data.latitude, data.longitude]
    }


def profile_desa_view(request, model_id):
    if model_id != 0:
        desa = DesaProfile.objects.get(pk=model_id)
        context = map_desa(desa)
    else:
        context = {
            'empty': 'null'
        }
    return JsonResponse(context)


# def map_desa_psu(data):
#     return {
#         'geojson': data.base_map.geojson.name,
#         'id': data.id,
#         'attribute': {
#             'NamaDesa': data.name,
#             'warna': data.color
#         },
#         'center': [data.latitude, data.longitude]
#     }


def get_desa_psu(request):
    if request.method == 'POST':
        city_filter = {}
        if request.POST['city'].strip():
            city_filter = request.POST['city'].strip()

        city_filter = {
            'city_id': request.POST['city'].strip()
        }
        # filter(kecamatan_id=request.POST['city'].strip())
        if request.POST['isAll'].strip() == 'true':
            cprofs = MapDesa.objects.all()
            # if request.POST['kategori'].strip() != 0:
            #     cprofs.filter(kategori_psu_id=request.POST['kategori'].strip())
            # if request.POST['jenis'].strip() != 0:
            #     cprofs.filter(rth_category_id=request.POST['jenis'].strip())

            context = {
                'data': [map_desa_psu(obj) for obj in cprofs],
            }
        else:
            desa = MapDesa.objects.filter(id=request.POST['city'].strip()).first()
            detail = PsuProfile.objects.all().filter(desa_id=desa.id)
            context = {
                'geojson': desa.geojson.name,
                'attribute': {
                    'nama': desa.name,
                    'color': desa.color
                },
                'center': [desa.latitude, desa.longitude],
                'detail': [detail_desa(obj) for obj in detail]
            }

        return JsonResponse(context)

    return JsonResponse("400: Bad Request")


def profile_desa_psu_view(request, model_id):
    if model_id != 0:
        desa = PsuProfile.objects.get(pk=model_id)
        context = map_desa_psu(desa)
    else:
        context = {
            'empty': 'null'
        }
    return JsonResponse(context)


def map_psu(data):
    return {
        'id': data.id,
        'attribute': {
            'nama': data.nama_psu,
            'Urban Area': data.urban_area,
            'Planning': data.planning,
            'Address': data.address,
            'Deskripsi': data.description,
            'icon': data.icon.name,
        },
        'center': [data.latitude, data.longitude]
    }


def get_psu(request):
    if request.method == 'POST':
        cprofs = PsuProfile.objects.all().filter(desa_id=request.POST['rth-desa'].strip())
        context = {
            'data': [map_psu(obj) for obj in cprofs],
        }

        return JsonResponse(context)

    return JsonResponse("400: Bad Request")


def filter_category(request):
    if request.method == 'POST':
        if request.POST['desa'].strip() != 0:
            data = PsuProfile.objects.get(id=request.POST['desa'].strip())
            cprofs = PsuProfile.objects.all().filter(desa=request.POST['desa'].strip(),
                                                     rth_category_id=request.POST['rth-category'].strip())
            context = {
                'data': [map_psu(obj) for obj in cprofs],
                'geojson': data.base_map.geojson.name,
                'id': data.id,
                'attribute': {
                    'nama': data.name,
                    'warna': data.color
                },
                'center': [data.latitude, data.longitude]
            }
            return JsonResponse(context)
        # else:
        #     data = DesaPsuProfile.objects.get(desa=request.POST['desa'].strip())
        #     context = {
        #         'geojson': data.base_map.geojson.name,
        #         'id': data.id,
        #         'attribute': {
        #             'nama': data.name,
        #             'warna': data.color
        #             },
        #         'center': [data.latitude, data.longitude]
        #     }
        #     return JsonResponse(context)

    return JsonResponse("400: Bad Request")


def filter_kategori(request):
    if request.method == 'POST':
        data = JenisPsu.objects.all().filter(kategori_id=request.POST['id'].strip())
        context = {
            'data': [get_jenis(obj) for obj in data]
        }
        return JsonResponse(context)

    return JsonResponse("400: Bad Request")


def get_jenis(data):
    return {
        'value': data.id,
        'text': data.name
    }
