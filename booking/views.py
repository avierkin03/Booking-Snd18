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
