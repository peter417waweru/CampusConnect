
from django.db import models
from django.contrib.auth.models import User

class TradeItem(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='trade_items/', blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class TradeRequest(models.Model):
    item = models.ForeignKey(TradeItem, on_delete=models.CASCADE)
    requester = models.ForeignKey(User, on_delete=models.CASCADE, related_name='trade_requests')
    message = models.TextField()
    status = models.CharField(max_length=20, choices=(('pending', 'Pending'), ('accepted', 'Accepted'), ('rejected', 'Rejected')), default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Request for {self.item.name} by {self.requester.username}"

class BoardRoom(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    participants = models.ManyToManyField(User, related_name='boardroom_participants')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
