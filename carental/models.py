import datetime

from django.contrib.auth.models import AbstractUser
from django.db import models


FUEL_CHOICES =(
    ("1", "Diesel"),
    ("2", "Essence"),
)


class Car(models.Model):
    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    color = models.CharField(max_length=100)
    fuel = models.CharField(max_length=100, choices=FUEL_CHOICES, null=True, default='2')
    mileage = models.PositiveIntegerField()
    price = models.PositiveIntegerField()
    image = models.ImageField(upload_to='carental/static/carental/car_images')
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.brand + ' ' + self.model


class User(AbstractUser):
    balance = models.PositiveIntegerField(default=0, blank=True)
    penalty = models.BooleanField(default=False)

    def __str__(self):
        return self.username


class Reservation(models.Model):
    car = models.ForeignKey('Car', on_delete=models.CASCADE)
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    date = models.DateTimeField()
    finish_date = models.DateTimeField()
    duration = models.PositiveSmallIntegerField(default=1)
    cancelled = models.CharField(choices=(('false', 'false'), ('true', 'true'), ('seen', 'seen')), default='false', max_length=10)

    def __str__(self):
        return str(self.car) + ' by: ' + str(self.user) + ' at: ' + self.date.strftime('%Y/%m/%d %H:00')


class Promotion(models.Model):
    car = models.OneToOneField('Car', on_delete=models.CASCADE)
    percentage = models.PositiveSmallIntegerField(choices=[(x, x) for x in range(5, 101, 5)])
    begin_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f"{self.car.model}: {self.percentage}% - {self.begin_date} to {self.end_date}"
