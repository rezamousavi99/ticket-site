from django import forms
from events.models import Venue, Event


class VenueForm(forms.ModelForm):
    class Meta:
        model = Venue
        fields = "__all__"

class EventForm(forms.ModelForm):

    class Meta:
        model = Event
        fields = ("name", "date", "venue", "manager", "attendees", "description")

        widgets = {
            "date": forms.TextInput(attrs={"placeholder": "YYYY-MM-DD HH:MM:SS"})
        }
