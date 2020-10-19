from django.urls import path

from . import views

app_name = 'map'
urlpatterns = [
    path('', views.index, name='index'),
    path('profile/city', views.profile_city, name='profile_city'),
    path('profile/city/<int:model_id>', views.profile_city_view, name='profile_city_view'),
    path('profile/city/rth/<int:model_id>', views.profile_rth_view, name='profile_rth_view'),
    path('profile/city/rth', views.profile_rth, name='profile_rth'),
    path('profile/city/rth/filter', views.profile_rth_filter, name='profile_rth_filter'),
    path('regulation', views.regulation, name='regulation'),
    path('article', views.article, name='article'),
    path('article/view/<int:model_id>', views.article_view, name='article_view'),
    path('slider/article/<int:model_id>', views.slider_article, name='slider_article'),
    path('gallery', views.gallery, name='gallery'),
    path('profile/city/desa/filter', views.get_desa, name='profile_desa_filter'),
    path('profile/city/desa/<int:model_id>', views.profile_desa_view, name='profile_desa_view'),
    path('profile/city/rth/desa/filter', views.get_desa_psu, name='profile_desa_rth_filter'),
    path('profile/city/rth/desa/<int:model_id>', views.profile_desa_psu_view, name='profile_desa_psu_view'),
    path('profile/city/rth/psu/filter', views.get_psu, name='profile_psu'),
    path('profile/city/rth/psu/category', views.filter_category, name='category_psu'),

]
