from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser

class Venue(models.Model):
    name = models.CharField(max_length=200)
    address = models.TextField()
    capacity = models.PositiveIntegerField()
    seating_plan = models.ImageField(upload_to='venue_seating_plans/', null=True, blank=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Seat(models.Model):
    SEAT_TYPES = (
        ('standard', 'Standard'),
        ('premium', 'Premium'),
        ('vip', 'VIP'),
        ('disabled', 'Disabled Access'),
    )
    
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE, related_name='seats')
    seat_number = models.CharField(max_length=10)
    seat_type = models.CharField(max_length=10, choices=SEAT_TYPES, default='standard')
    row = models.CharField(max_length=5)
    section = models.CharField(max_length=50)
    x_coord = models.FloatField(help_text="X coordinate (0-100) for seat positioning")
    y_coord = models.FloatField(help_text="Y coordinate (0-100) for seat positioning")
    is_booked = models.BooleanField(default=False)

    class Meta:
        unique_together = ('venue', 'seat_number')

    def __str__(self):
        return f"{self.seat_number} ({self.get_seat_type_display()})"

class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateTimeField()
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE, related_name='events')
    image = models.ImageField(upload_to='event_images/', null=True, blank=True)
    base_price = models.DecimalField(max_digits=6, decimal_places=2)
    premium_price = models.DecimalField(max_digits=6, decimal_places=2)
    vip_price = models.DecimalField(max_digits=6, decimal_places=2)
    disabled_price = models.DecimalField(max_digits=6, decimal_places=2)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    def available_seats(self):
        return self.venue.seats.filter(is_booked=False)

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    seats = models.ManyToManyField(Seat)
    booking_date = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    is_confirmed = models.BooleanField(default=False)
    payment_reference = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.event.title}"