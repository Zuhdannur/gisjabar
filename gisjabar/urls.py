"""gisjabar URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.urls import include, path, re_path

from map import views

urlpatterns = [
                  path('', views.index, name='index'),
                  path('page/<slug:slug>/', views.page_view, name='page'),
                  path('map/', include('map.urls')),
                  path('admin/', admin.site.urls),
                  path('filter-kategori', views.filter_kategori, name='filter_kategori'),
                  re_path(r'^ckeditor/', include('ckeditor_uploader.urls')),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header = 'Dinas Perumahan & Kawasan Permukiman & Pertanahan'
admin.site.index_title = 'Fitur'  # default: "Site administration"
admin.site.site_title = 'Dinas Perumahan & Kawasan Permukiman & Pertanahan'
