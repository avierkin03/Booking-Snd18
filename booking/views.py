from django.shortcuts import render, redirect
from .models import Room, Category, Booking
from datetime import datetime
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login, authenticate, logout

# функція представлення списку всіх кімнат
def room_list(request):
    all_rooms = Room.objects.all()
    categories = Category.objects.all()

    category_id = request.GET.get("category")
    capacity = request.GET.get("capacity")
    price_max = request.GET.get("price_max")

    if category_id:
        all_rooms = all_rooms.filter(category = category_id)
    if capacity:
        all_rooms = all_rooms.filter(capacity__gte = int(capacity))
    if price_max:
        all_rooms = all_rooms.filter(price__lte = float(price_max))

    context = {
        "rooms": all_rooms,
        "category": categories,
        "selected_capacity": capacity,
        "selected_price_max": price_max,
        "selected_category": category_id
    }
    return render(request=request, template_name="booking/room_list.html", context=context)


# функція представлення бронювання кімнати
def book_room(request, room_id):
    room = Room.objects.get(pk=room_id)
    context = {
        "room": room
    }
    
    if request.method == "GET":
        return render(request=request, template_name="booking/booking_form.html", context=context)
    
    elif request.method == "POST":
        start_date = datetime.strptime(request.POST.get("start_date"), "%Y-%m-%d").date()
        end_date = datetime.strptime(request.POST.get("end_date"), "%Y-%m-%d").date()

        user = request.user
        room = Room.objects.get(pk=room_id)

        # перевірка коректності дат
        if end_date <= start_date or start_date < datetime.now().date():
            return render(request=request, template_name="booking/booking_form.html", context=context)

        # перевірка чи номер вже зайнятий на дати, які вибрав користувач
        if Booking.objects.filter(room=room, start_date__lt=end_date, end_date__gt=start_date).exists():
            return render(request=request, template_name="booking/booking_form.html", context=context)

        # створюємо бронювання
        Booking.objects.create(
            user = user,
            room = room,
            start_date = start_date,
            end_date = end_date
        )
        context = {
            "bookings": Booking.objects.filter(user=user).order_by('-start_date')
        }
        return render(request=request, template_name="booking/my_bookings.html", context=context)


# функція представлення сторінки історії бронювань користувача
def user_bookings(request):
    context = {
        "bookings": Booking.objects.filter(user=request.user).order_by('-start_date')
    }
    return render(request=request, template_name="booking/my_bookings.html", context=context)


# функція представлення логіну користувача
def user_login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("rooms")
    else:
        form = AuthenticationForm()

    return render(request, template_name="auth/login.html", context={"form": form})


# функція представлення логауту користувача
def user_logout(request):
    logout(request)
    return redirect("rooms")


# функція представлення рестрації користувача
def user_register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            login(request, new_user)
            return redirect("rooms")
    else:
        form = UserCreationForm()

    return render(request, template_name="auth/register.html", context={"form": form})