from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import CustomUser, Category, Field, Booking, Participant





def home(request):
    return render(request, 'home.html')






def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        photo = request.FILES.get('photo')
        user = CustomUser.objects.create_user( username=username, email=email, password=password)
        if photo:
            user.photo = photo
            user.save()
        login(request, user)
        return redirect('home')
    return render(request, 'register.html')









def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate( request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        messages.error(request)
    return render(request, 'login.html')








@login_required
def logout_user(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')
    return redirect('home')










@login_required
def fields(request):
    field_list = Field.objects.all()
    categories = Category.objects.all()
    search = request.GET.get('search')
    category_ids = request.GET.getlist('category')
    if search:
        field_list = field_list.filter(
            Q(name__icontains=search) | Q(address__icontains=search))
    if category_ids:
        field_list = field_list.filter(category__id__in=category_ids)
    return render(request, 'fields.html', {'fields': field_list,'categories': categories,'search': search,'selected_categories': category_ids})









@login_required
def field_detail(request, pk):
    field = get_object_or_404(Field, pk=pk)
    return render(request, 'field_detail.html', {'field': field})










@login_required
def book_field(request, pk):
    field = get_object_or_404(Field, pk=pk)
    if not field.is_free:
        messages.error(request)
        return redirect('field_detail', pk=field.pk)
    if request.method == 'POST':
        has_team = request.POST.get('has_team') == 'yes'
        players_needed = request.POST.get('players_needed', 0)
        booking = Booking.objects.create( user=request.user, field=field, has_team=has_team, players_needed=players_needed, status='active')
        field.is_free = False
        field.save()
        return redirect('booking_detail', pk=booking.pk)
    return render(request, 'booking.html', {'field': field})





@login_required
def my_fields(request):
    active_bookings = Booking.objects.filter(user=request.user,status='active')
    history = Booking.objects.filter(user=request.user)
    return render(request, 'my_fields.html', {'active_bookings': active_bookings,'history': history})







@login_required
def booking_detail(request, pk):
    booking = get_object_or_404( Booking.objects.select_related('field', 'user'), pk=pk, user=request.user)
    return render(request, 'booking_detail.html', {'booking': booking})






@login_required
def cancel_booking(request, pk):
    booking = get_object_or_404( Booking, pk=pk, user=request.user, status='active' )
    if request.method == 'POST':
        booking.save()
        booking.field.is_free = True
        booking.field.save()
        return redirect('my_fields')
    return redirect('booking_detail', pk=booking.pk)







@login_required
def finish_booking(request, pk):
    booking = get_object_or_404(Booking, pk=pk, user=request.user, status='active')
    if request.method == 'POST':
        booking.status = 'completed'
        booking.save()
        booking.field.is_free = True
        booking.field.save()
        return redirect('my_fields')
    return redirect('booking_detail', pk=booking.pk)







@login_required
def join_team(request, pk):
    booking = get_object_or_404( Booking, pk=pk, status='active', has_team=False)
    if request.method == 'POST':
        if booking.user == request.user:
            messages.error(request)
        elif booking.participants.count() >= booking.players_needed:
            messages.error(request)
        else:
            Participant.objects.create(booking=booking,user=request.user)
    return redirect('play_together')









@login_required
def leave_team(request, pk):
    booking = get_object_or_404(Booking, pk=pk, status='active', has_team=False)
    if request.method == 'POST':
        participant = Participant.objects.filter( booking=booking, user=request.user ).first()
        if participant:
            participant.delete()
    return redirect('play_together')






@login_required
def profile(request):
    bookings_count = Booking.objects.filter(user=request.user).count()
    return render(request, 'profile.html', {'bookings_count': bookings_count})







@login_required
def edit_profile(request):
    if request.method == 'POST':
        request.user.username = request.POST.get('username')
        request.user.email = request.POST.get('email')
        request.user.phone = request.POST.get('phone')
        request.user.about = request.POST.get('about')
        photo = request.FILES.get('photo')
        if photo:
            request.user.photo = photo
        request.user.save()
        return redirect('profile')
    return render(request, 'edit_profile.html')







@login_required
def user_profile(request, pk):
    player = get_object_or_404(CustomUser, pk=pk)
    return render(request, 'user_profile.html', {'player': player})

