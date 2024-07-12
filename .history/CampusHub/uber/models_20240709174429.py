from django.db import models
from django.contrib.auth.models import User

class Driver(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    license_number = models.CharField(max_length=50)
    car_model = models.CharField(max_length=100)
    car_license_plate = models.CharField(max_length=20)
    phone_number = models.CharField(max_length=15)
    address = models.CharField(max_length=255, default='Default Address')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.user.username} - {self.car_license_plate}'

class Vehicle(models.Model):
    driver = models.OneToOneField(Driver, on_delete=models.CASCADE)
    car_model = models.CharField(max_length=100)
    car_license_plate = models.CharField(max_length=20)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.car_model} - {self.car_license_plate}'
    
class Trip(models.Model):
    driver = models.ForeignKey(to='auth.User', on_delete=models.CASCADE)  # Replace 'auth.User' with your driver model
    distance = models.FloatField()
    fare = models.FloatField()

class UberRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='requests')
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, related_name='requests', blank=True, null=True)
    destination = models.CharField(max_length=250)
    fare_estimate = models.DecimalField(max_digits=10, decimal_places=2)
    driver_rating = models.DecimalField(max_digits=3, decimal_places=2, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    pickup_location = models.CharField(max_length=200, blank=True)
    status = models.CharField(max_length=50, default="pending", choices=[('requested', 'Requested'), ('accepted', 'Accepted'), ('completed', 'Completed')])

    def __str__(self):
        return f"UberRequest by {self.user.username} to {self.destination}"
    
class ChatMessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    uber_request = models.ForeignKey(UberRequest, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.user.username} at {self.timestamp}"
