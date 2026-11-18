from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('fields/', views.fields, name='fields'),
    path('fields/<int:pk>/', views.field_detail, name='field_detail'),
    path('fields/<int:pk>/book/', views.book_field, name='book_field'),
    path('my_fields/', views.my_fields, name='my_fields'),
    path('bookings/<int:pk>/', views.booking_detail, name='booking_detail'),
    path('bookings/<int:pk>/cancel/', views.cancel_booking, name='cancel_booking'),
    path('bookings/<int:pk>/finish/', views.finish_booking, name='finish_booking'),
    path('play_together/', views.play_together, name='play_together'),
    path('bookings/<int:pk>/join/', views.join_team, name='join_team'),
    path('bookings/<int:pk>/leave/', views.leave_team, name='leave_team'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('users/<int:pk>/', views.user_profile, name='user_profile'),
]