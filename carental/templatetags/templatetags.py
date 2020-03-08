import datetime

import pytz
from django import template

from carental.models import Reservation, Promotion

utc = pytz.UTC


def fuel_number2str(value):
    return 'Essence' if value == '2' else 'Diesel'


def img_file(value):
    return str(value).split('/')[-1]


def reverse_sort_order(value):
    return value[1:] if value[0] == '-' else '-' + value


def is_available(value):
    today = datetime.datetime.now()
    same_car_reservations = list(Reservation.objects.filter(car_id=value.id))
    for car_res in same_car_reservations:
        car_res_date = car_res.date.replace(tzinfo=utc)
        today = today.replace(tzinfo=utc)
        if car_res_date <= today <= car_res_date + datetime.timedelta(hours=car_res.duration):
            return 'déjà loué'
    return 'disponible'


def get_promotion(value):
    try:
        promotion = value.promotion
        if promotion.begin_date <= datetime.date.today() <= promotion.end_date:
            return {'exists': True, 'percentage': promotion.percentage,
                    'new_price': value.price - value.price * promotion.percentage // 100,
                    'end': promotion.end_date.strftime('%b, %d')}
        return {'exists': False}
    except Promotion.DoesNotExist:
        return {'exists': False}

register = template.Library()
register.filter('fuel_number2str', fuel_number2str)
register.filter('img_file', img_file)
register.filter('reverse_sort_order', reverse_sort_order)
register.filter('is_available', is_available)
register.filter('get_promotion', get_promotion)
