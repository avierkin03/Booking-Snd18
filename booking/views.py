from django.shortcuts import render
from .models import Room, Category, Booking

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
    if request.method == "GET":
        room = Room.objects.get(pk=room_id)
        context = {
            "room": room
        }
        return render(request=request, template_name="booking/booking_form.html", context=context)
    
    elif request.method == "POST":
        start_date = request.POST.get("start_date")
        end_date = request.POST.get("end_date")

        user = request.user
        room = Room.objects.get(pk=room_id)

        # TODO додати превірку коректності дат + перевірку чи зайнята кімната на ці дати
        # створюємо бронювання
        Booking.objects.create(
            user = user,
            room = room,
            start_date = start_date,
            end_date = end_date
        )
        context = {
            "bookings": Booking.objects.filter(user=user)
        }
        return render(request=request, template_name="booking/my_bookings.html", context=context)

