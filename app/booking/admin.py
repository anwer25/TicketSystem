from django.contrib import admin
from .models import Venue, Seat, Event, Booking

class SeatInline(admin.TabularInline):
    model = Seat
    extra = 1
    fields = ('seat_number', 'seat_type', 'row', 'section', 'x_coord', 'y_coord', 'is_booked')
    readonly_fields = ('is_booked',)

@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin):
    inlines = [SeatInline]
    list_display = ('name', 'address', 'capacity')
    search_fields = ('name', 'address')

@admin.register(Seat)
class SeatAdmin(admin.ModelAdmin):
    list_display = ('seat_number', 'venue', 'seat_type', 'row', 'section', 'is_booked')
    list_filter = ('venue', 'seat_type', 'is_booked')
    search_fields = ('seat_number', 'venue__name')

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'venue', 'base_price', 'premium_price', 'vip_price', 'is_active')
    list_filter = ('date', 'venue', 'is_active')
    search_fields = ('title', 'description', 'venue__name')

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'event', 'booking_date', 'total_price', 'is_confirmed')
    list_filter = ('booking_date', 'event', 'is_confirmed')
    search_fields = ('user__username', 'event__title', 'payment_reference')
    filter_horizontal = ('seats',)