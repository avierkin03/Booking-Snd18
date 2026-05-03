from django.urls import path
from booking import views

urlpatterns = [
    path("", views.room_list, name="rooms"),
    path("booking/<int:room_id>", views.book_room, name="booking"),
]