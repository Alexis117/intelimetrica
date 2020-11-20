from django.urls import path, re_path
from .views import upload, restaurants, restaurant_detail, statistics

urlpatterns = [
    #CRUD API
    path('get/all/', restaurants, name='all'),
    path('get/<str:id>/', restaurant_detail, name='getbyid'),
    path('create/', restaurants, name='create'),
    path('update/<str:id>/', restaurant_detail, name='update'),
    path('delete/all/', restaurants, name='delete-all'),
    path('delete/<str:id>/', restaurant_detail, name='deletebyid'),

    #Statistics API
    re_path(r'^statistics$', statistics, name='statistics'),

    #Utilidad para cargar los datos a partir del csv
    path('upload/', upload, name='upload'),
]
