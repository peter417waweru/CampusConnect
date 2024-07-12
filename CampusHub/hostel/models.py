from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser

class Hostel(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    amenities = models.TextField()
    rental_rate = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(upload_to='hostel/hostel_images/', null=True, blank=True)

    def __str__(self):
        return self.name

class Booking(models.Model):
    hostel = models.ForeignKey(Hostel, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    approved = models.BooleanField(default=False)

    def __str__(self):
        return f"Booking by {self.user.username} for {self.hostel.name}"


