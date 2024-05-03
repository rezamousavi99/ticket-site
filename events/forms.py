from django import forms
from events.models import Venue


class VenueForm(forms.ModelForm):
    class Meta:
        model = Venue
        fields = "__all__"
