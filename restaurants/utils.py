from math import sin, cos, sqrt, atan2, radians
import statistics 

def is_coordinate_inside_area(lat1, lng1, lat2, lng2, radius):
    '''Calculamos la distancia entre dos coordenadas'''

    R = 6373.0 #Radio de la tierra en km

    lat1 = radians(lat1)
    lng1 = radians(lng1)
    lat2 = radians(lat2)
    lng2 = radians(lng2)

    dlng = lng2 - lng1
    dlat = lat2 - lat1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlng / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c

    if (distance * 1000) <= radius:
        return True
    return False

def get_avg_std(restaurants):
    '''Calculamos el promedio y la desviación estandar de una lista de restaurantes'''
    ratings = [ restaurant.rating for restaurant in restaurants ]
    avg = statistics.mean(ratings)
    try:
        std = statistics.stdev(ratings)
    except statistics.StatisticsError:
        std = 'Se necesitan dos o más puntos para calcular la desviación estándar'
    return avg, std

