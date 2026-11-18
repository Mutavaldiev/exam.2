from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Category, Field, Booking, Participant


admin.site.register(CustomUser, UserAdmin)
admin.site.register(Category)
admin.site.register(Field)
admin.site.register(Booking)
admin.site.register(Participant)