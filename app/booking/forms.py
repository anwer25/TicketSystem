from django import forms
from .models import Booking, Event, Seat
from django.core.exceptions import ValidationError

class SeatSelectionForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = []
        
    def __init__(self, *args, **kwargs):
        self.event = kwargs.pop('event', None)
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
    def clean(self):
        cleaned_data = super().clean()
        selected_seats = self.data.getlist('seats')
        
        if not selected_seats:
            raise ValidationError("Please select at least one seat.")
            
        seats = Seat.objects.filter(
            id__in=selected_seats,
            venue=self.event.venue,
            is_booked=False
        )
        
        if len(seats) != len(selected_seats):
            raise ValidationError("One or more selected seats are no longer available.")
            
        cleaned_data['seats'] = seats
        return cleaned_data

class EventFilterForm(forms.Form):
    SEAT_TYPE_CHOICES = [
        ('', 'All Types'),
        ('standard', 'Standard'),
        ('premium', 'Premium'),
        ('vip', 'VIP'),
        ('disabled', 'Disabled Access'),
    ]
    
    search = forms.CharField(required=False, label='Search events')
    date_from = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    date_to = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    seat_type = forms.ChoiceField(required=False, choices=SEAT_TYPE_CHOICES)
    min_price = forms.DecimalField(required=False, max_digits=6, decimal_places=2)
    max_price = forms.DecimalField(required=False, max_digits=6, decimal_places=2)