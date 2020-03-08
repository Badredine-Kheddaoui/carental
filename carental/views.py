import datetime
import pytz
from collections import namedtuple

from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import redirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.db.models import F
from django.urls import reverse

from .forms import CarForm
from .models import Car, Reservation, User, Promotion
from .forms import UserRegisterForm

utc = pytz.UTC


@login_required
def profile(request):
    return render(request, 'carental/profile.html')


def home(request):
    return render(request, 'carental/base.html')


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            form.save()
            messages.success(request, f'Account created for {username}!')
            return redirect('home')
    else:
        form = UserRegisterForm()
    return render(request, 'carental/register.html', {'form': form})


@permission_required('user.is_superuser')
def add_car(request):
    if request.method == "POST":
        form = CarForm(request.POST)
        if form.is_valid():
            form.save()
    return render(request, "carental/add_car.html", {'carForm': CarForm()})


# TODO add a form for customized search
def cars(request):
    return render(request, "carental/cars.html", {'cars': Car.objects.all()})


@permission_required('user.is_superuser')
def update_car(request):
    if request.method == "POST":
        form = request.POST
        updatedCar = Car.objects.filter(pk=form.get('id'))
        updatedCar.update(mileage=form.get('mileage'), price=form.get('price'),
                          available=True if form.get('available') else False)
    return render(request, "carental/update_car.html", {'cars': Car.objects.all()})


@permission_required('user.is_superuser')
def reservations(request):
    prettyReservation = namedtuple('Reservation', ['id', 'car', 'user', 'date', 'finish_date', 'duration'])
    prettyReservations = []
    reservations = Reservation.objects.all()
    for reservation in reservations:
        prettyReservations.append(prettyReservation(reservation.id,
                                                    ' '.join(Car.objects.values('brand', 'model').get(
                                                        pk=reservation.car_id).values()),
                                                    ' '.join(User.objects.values('first_name', 'last_name').get(
                                                        pk=reservation.user_id).values()),
                                                    reservation.date.strftime('%Y/%m/%d %H:00'),
                                                    reservation.finish_date.strftime('%Y/%m/%d %H:00'),
                                                    reservation.duration // 24
                                                    ))

    return render(request, "carental/reservations.html", {'reservations': prettyReservations})


@login_required
def reserve(request):
    if request.method == "POST":
        form = request.POST
        print(f"\nthe form: {form}")
        if form.get('duration'):  # request comes from the reserve page
            if request.user.balance < (int(form['duration'])) * int(form['price']):
                return JsonResponse({"tag": "danger", "message": """Unsufficient funds, You can recharge your account from 
                <a data-toggle="modal" data-target="#exampleModal">here</a>"""
                                     })
            if not possibe_reservation(request):
                return JsonResponse({"tag": "danger", "message": "Reservation not possible at the selected time"})
            date = form['date'] + ' ' + form['time']
            date = datetime.datetime.strptime(date, '%Y-%m-%d %H')
            duration = int(form['duration']) * 24
            try:
                Reservation(car_id=form['car_id'], user_id=request.user.id, date=date,
                            finish_date=date + datetime.timedelta(hours=duration), duration=duration).save()
                u = User.objects.get(pk=request.user.id)
                u.balance -= int(form['duration']) * int(form['price'])
                u.save()
                return JsonResponse({"tag": "success", "message": "Reservation saved", "balance": u.balance})
            except:
                return JsonResponse({"tag": "danger", "message": "Reservation failed"})
        else:  # request comes from the cars page
            car = ' '.join(Car.objects.values('brand', 'model').get(pk=form.get('id')).values())
            return render(request, "carental/reserve.html",
                          {'car': {'id': form.get('id'), 'name': car, 'price': form.get('price')},
                           'duration_list': [x for x in range(2, 31)],
                           'time_list': [f'{x}' for x in range(8, 24)]})
    return cars(request)


# Check if the requested reservation overlaps with a previous one
@login_required
def possibe_reservation(request):
    if request.method == "POST":
        form = request.POST
        form_date = form['date'] + ' ' + form['time']
        form_date = datetime.datetime.strptime(form_date, '%Y-%m-%d %H')
        same_car_reservations = list(Reservation.objects.filter(car_id=form['car_id']))
        for car_res in same_car_reservations:
            car_res_date = car_res.date.replace(tzinfo=utc)
            form_date = form_date.replace(tzinfo=utc)
            print(f"res date: {car_res_date}")
            print(f"form date: {form_date}")
            if car_res_date <= form_date < car_res_date + datetime.timedelta(hours=car_res.duration) or \
                    form_date <= car_res_date < form_date + datetime.timedelta(hours=int(form['duration']) * 24):
                print("nope")
                return False
        return True


# tell the user if a car is on a sale
def promotion(request):
    promotions = list(Promotion.objects.all())
    if len(promotions) == 0:
        return JsonResponse({"tag": "danger", "message": "no promotions"})
    else:
        for i in range(1, len(promotions)):
            if promotions[-i].begin_date <= datetime.date.today() <= promotions[-i].end_date:
                return JsonResponse({"tag": "success", "percentage": promotions[-i].percentage,
                                     "car": promotions[-i].car.brand + " " + promotions[-i].car.model,
                                     "end": promotions[-i].end_date})


# penalize the user if he made a reservation and didn't commit
@permission_required('user.is_superuser')
def penalize(request):
    if request.method == "POST":
        form = request.POST
        r = Reservation.objects.get(pk=form['id'])
        if form['action'] == 'penalize':
            u = User.objects.get(pk=r.user_id)
            u.penalty = True
            if u.balance > 999:
                u.balance -= 1000
            else:
                u.balance = 0
            u.save()
            print(f"user id: {r.user_id}, penalty: {User.objects.get(pk=r.user_id).penalty}")
            r.delete()
            messages.success(request, f'user: ({u.username}) penalized and reservation: ({r}) deleted!')
        elif form['action'] == 'cancel':
            r.cancelled = 'true'
            r.save()
            messages.success(request, f'Reservation ({str(r)}) Cancelled')
        return redirect('reservations')


# tell the user if he was penalized
@login_required
def penalties(request):
    u = User.objects.get(pk=request.user.pk)
    print(str(u) + str(u.penalty))
    if u.penalty:
        u.penalty = False
        u.save()
        return JsonResponse({"tag": "danger",
                             "message": '<span style="font-size: 20px; color: red">1000 DA </span> have been deducted from your account for not honoring your engagement'})
    else:
        return JsonResponse({"tag": "success"})


# tell the user if one of his reservations were cancelled
@login_required
def cancellations(request):
    u = User.objects.get(pk=request.user.pk)
    r = list(Reservation.objects.filter(user_id=u.id, cancelled='true'))
    if len(r) > 0:
        r[-1].cancelled = 'seen'
        r[-1].save()
        return JsonResponse({"tag": "danger", "message": f"your {r[-1]} reservation was cancelled, "
        f"would you like to <a href=\"{reverse('reserve')}\">make another reservation?</a>"})
    return JsonResponse({"tag": "success", "message": f'so far so good'})


# TODO: smooth redirects
@login_required
def add_balance(request):
    if request.method == "POST":
        try:
            form = request.POST
            print(form)
            User.objects.filter(pk=form['user']).update(balance=F('balance') + form['amount'])
            print(f"User: {form['user']}, new amount: {User.objects.get(pk=form['user']).balance}")
            s = '../' + str(request.META.get('HTTP_REFERER', '')).split('/', 3)[-1]     # to redirect the user to the current page
            return redirect(s)
        except:
            return None
    else:
        return redirect('cars')

