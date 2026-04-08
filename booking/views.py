from django.shortcuts import render
from .models import Room, Category, Booking

# функція представлення списку всіх кімнат
def room_list(request):
    all_rooms = Room.objects.all()
    context = {
        "rooms": all_rooms
    }
    return render(request=request, template_name="booking/room_list.html", context=context)
