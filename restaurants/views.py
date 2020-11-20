from django.shortcuts import render
from django.http.response import JsonResponse

import csv
import io
import statistics as st

from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
from rest_framework import status

from .models import Restaurants
from .serializers import RestaurantsSerializer
from .utils import is_coordinate_inside_area, get_avg_std

# Create your views here.
@api_view(['GET', 'POST', 'DELETE'])
def restaurants(request):
    '''API View para consultar, eliminar todas las entradas o crear una nueva'''
    if request.method == 'GET':
        restaurants = Restaurants.objects.all()
        restaurants_serialized = RestaurantsSerializer(restaurants, many=True)
        return JsonResponse(restaurants_serialized.data, safe=False)
    if request.method == 'POST':
        restaurants_data = JSONParser().parse(request)
        restaurants_serialized = RestaurantsSerializer(data=restaurants_data)
        if restaurants_serialized.is_valid():
            restaurants_serialized.save()
            return JsonResponse(restaurants_serialized.data, status=status.HTTP_201_CREATED) 
        return JsonResponse(restaurants_serialized.errors, status=status.HTTP_400_BAD_REQUEST)
    if request.method == 'DELETE':
        Restaurants.objects.all().delete()
        return JsonResponse({'message': 'Se han borrado todos los restaurantes'}, status=status.HTTP_200_OK)

@api_view(['GET', 'PUT', 'DELETE'])
def restaurant_detail(request, id):
    '''API View para consultar, editar o eliminar alguna entrada por id'''
    try: 
        restaurant = Restaurants.objects.get(id=id) 
    except Restaurants.DoesNotExist: 
        return JsonResponse({'message': 'No existe un restaurante con ese id'}, status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        restaurant_serialized = RestaurantsSerializer(restaurant) 
        return JsonResponse(restaurant_serialized.data)
    if request.method == 'PUT':
        restaurant_data = JSONParser().parse(request)
        restaurant_serialized = RestaurantsSerializer(restaurant, data=restaurant_data)
        if restaurant_serialized.is_valid():
            restaurant_serialized.save()
            return JsonResponse(restaurant_serialized.data) 
        return JsonResponse(restaurant_serialized.errors, status=status.HTTP_400_BAD_REQUEST)
    if request.method == 'DELETE':
        restaurant.delete()
        return JsonResponse({'message': 'Se ha borrado el restaurante con éxito'}, status=status.HTTP_200_OK)

@api_view(['GET'])
def statistics(request):
    '''API View que devuelve la lista de restaurantes que estan dentro del rango'''
    if request.method == 'GET':
        #Validamos los parámetros
        latitude = request.GET.get('latitude')
        if latitude is None: return JsonResponse({'message': 'Falta el parámetro latitude'}, status=status.HTTP_400_BAD_REQUEST)
        longitude = request.GET.get('longitude')
        if longitude is None: return JsonResponse({'message': 'Falta el parámetro longitude'}, status=status.HTTP_400_BAD_REQUEST)
        radius = request.GET.get('radius')
        if radius is None: return JsonResponse({'message': 'Falta el parámetro radius'}, status=status.HTTP_400_BAD_REQUEST)
        #Filtramos y calculamos
        restaurants = Restaurants.objects.all()
        restaurants = filter(lambda x: is_coordinate_inside_area(float(latitude), float(longitude), x.lat, x.lng, float(radius)), restaurants)
        restaurants = list(restaurants)
        count = len(restaurants)
        avg, std = get_avg_std(restaurants)
        return JsonResponse({'count': count, 'avg': avg, 'std': std})

def upload(request):
    '''Vista que nos ayuda a obtener los datos del csv y cargarlos en sqlite'''
    if request.method == 'POST':
        csv_file = request.FILES['csv_file']
        csv_file.seek(0)
        data = csv.DictReader(io.StringIO(csv_file.read().decode('utf-8')))
        for row in data:
            Restaurants.objects.create(
                id = row['id'],
                rating = int(row['rating']),
                name = row['name'],
                site = row['site'],
                email = row['email'],
                phone = row['phone'],
                street = row['street'],
                city = row['city'],
                state = row['state'],
                lat = float(row['lat']),
                lng = float(row['lng'])
            )
    return render(request, 'upload_file.html'   )