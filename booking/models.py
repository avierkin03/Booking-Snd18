from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    title = models.CharField(max_length=50)

    def __str__(self):
        return self.title


class Room(models.Model):
    number = models.IntegerField()
    capacity = models.IntegerField()
    price = models.FloatField()
    image = models.ImageField(upload_to='rooms', null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='rooms')

    def __str__(self):
        return f'Room №{self.number} for {self.capacity} person(s)'


class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bookings")
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="bookings")
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'Booking by {self.user.username} - room №{self.room.number}'