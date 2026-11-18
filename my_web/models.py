from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings






class CustomUser(AbstractUser):
    photo = models.ImageField(upload_to='profiles/', blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True)
    about = models.TextField(blank=True)





class Category(models.Model):
    name = models.CharField(max_length=100)
    players_count = models.PositiveIntegerField()

    def __str__(self):
        return self.name







class Field(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    description = models.TextField()
    category = models.ForeignKey(Category,on_delete=models.CASCADE,related_name='fields')
    price = models.DecimalField(max_digits=8, decimal_places=2)
    photo = models.ImageField(upload_to='fields/')
    is_free = models.BooleanField(default=True)

    def __str__(self):
        return self.name





class Booking(models.Model):
    user = models.ForeignKey( settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bookings')
    field = models.ForeignKey( Field, on_delete=models.CASCADE, related_name='bookings')
    has_team = models.BooleanField(default=True)
    players_needed = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=20,default='active')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.field.name




class Participant(models.Model):
    booking = models.ForeignKey( Booking, on_delete=models.CASCADE, related_name='participants')
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    joined_at = models.DateTimeField(auto_now_add=True)
    unique_together = ('booking', 'user')
    def __str__(self):
        return self.user.username


