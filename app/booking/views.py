from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Event, Booking, Seat, Venue
from .forms import SeatSelectionForm, EventFilterForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

def event_list(request):
    form = EventFilterForm(request.GET or None)
    events = Event.objects.filter(is_active=True).order_by('date')
    
    if form.is_valid():
        if form.cleaned_data['search']:
            events = events.filter(
                Q(title__icontains=form.cleaned_data['search']) |
                Q(description__icontains=form.cleaned_data['search']) |
                Q(venue__name__icontains=form.cleaned_data['search'])
            )
        
        if form.cleaned_data['date_from']:
            events = events.filter(date__gte=form.cleaned_data['date_from'])
        
        if form.cleaned_data['date_to']:
            events = events.filter(date__lte=form.cleaned_data['date_to'])
        
        if form.cleaned_data['seat_type']:
            events = events.filter(
                venue__seats__seat_type=form.cleaned_data['seat_type'],
                venue__seats__is_booked=False
            ).distinct()
        
        if form.cleaned_data['min_price']:
            events = events.filter(base_price__gte=form.cleaned_data['min_price'])
        
        if form.cleaned_data['max_price']:
            events = events.filter(vip_price__lte=form.cleaned_data['max_price'])
    
    return render(request, 'booking/event_list.html', {
        'events': events,
        'form': form,
    })

def event_detail(request, pk):
    event = get_object_or_404(Event, pk=pk, is_active=True)
    available_seats = event.available_seats()
    
    seat_counts = {
        'standard': available_seats.filter(seat_type='standard').count(),
        'premium': available_seats.filter(seat_type='premium').count(),
        'vip': available_seats.filter(seat_type='vip').count(),
        'disabled': available_seats.filter(seat_type='disabled').count(),
    }
    
    return render(request, 'booking/event_detail.html', {
        'event': event,
        'seat_counts': seat_counts,
    })

@login_required
def book_event(request, pk):
    event = get_object_or_404(Event, pk=pk, is_active=True)

    if request.method == 'POST':
        form = SeatSelectionForm(request.POST, event=event, user=request.user)
        if form.is_valid():
            selected_seats = form.cleaned_data['seats']

            booking = Booking(
                user=request.user,
                event=event,
                is_confirmed=True
            )
            booking.save()  

            booking.seats.set(selected_seats) 

            
            seat_prices = {
                'standard': event.base_price,
                'premium': event.premium_price,
                'vip': event.vip_price,
                'disabled': event.disabled_price,
            }
            booking.total_price = sum(seat_prices[seat.seat_type] for seat in selected_seats)
            booking.save() 

            
            for seat in selected_seats:
                seat.is_booked = True
                seat.save()

            messages.success(request, 'Your booking was successful!')
            return redirect('booking_confirmation', booking.id)
    else:
        form = SeatSelectionForm(event=event, user=request.user)

    available_seats = event.available_seats()

    return render(request, 'booking/book_event.html', {
        'form': form,
        'event': event,
        'available_seats': available_seats,
        'seat_types': dict(Seat.SEAT_TYPES),
    })

@login_required
def booking_confirmation(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    return render(request, 'booking/confirmation.html', {
        'booking': booking,
        'seats': booking.seats.all(),
    })

@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(user=request.user).order_by('-booking_date')
    return render(request, 'booking/my_bookings.html', {
        'bookings': bookings,
    })

@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    
    if request.method == 'POST':
        # Free up the seats
        for seat in booking.seats.all():
            seat.is_booked = False
            seat.save()
        
        booking.delete()
        messages.success(request, 'Your booking has been cancelled.')
        return redirect('my_bookings')
    
    return render(request, 'booking/cancel_booking.html', {
        'booking': booking,
    })

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('event_list')
    else:
        form = UserCreationForm()

    return render(request, 'registration/register.html', {'form': form})