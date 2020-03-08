import datetime

from carental.models import Car, Reservation
from django.forms import ModelForm, NumberInput
from django import forms
from carental.models import User
from django.contrib.auth.forms import UserCreationForm


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2', 'balance']


class CarForm(ModelForm):
    class Meta:
        model = Car
        fields = '__all__'


# class DateInput(forms.DateInput):
#     input_type = 'date'
#
#
# class ReservationForm(ModelForm):
#     class Meta:
#         model = Reservation
#         fields = ['date', 'duration']
#         widgets = {
#             'date': DateInput(attrs={'value': datetime.date.today}),
#             'duration': NumberInput(attrs={'min': '12', 'max': '720', 'step': '12'})
#         }
