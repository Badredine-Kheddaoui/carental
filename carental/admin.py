from django.contrib import admin

# Register your models here.
from carental.models import Car, Reservation, User, Promotion

admin.site.register(Car)
admin.site.register(User)
admin.site.register(Reservation)
admin.site.register(Promotion)