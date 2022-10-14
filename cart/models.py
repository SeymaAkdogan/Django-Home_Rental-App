from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from home.models import Home 

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=datetime.now)

class CartItem(models.Model):
    home = models.ForeignKey(Home, on_delete=models.CASCADE)
    start_time = models.DateField()
    end_time = models.DateField()
    price = models.FloatField(blank=True)
    cart = models.ForeignKey('Cart', on_delete=models.CASCADE)
