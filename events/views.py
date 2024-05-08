from django.http import HttpResponseRedirect
from django.shortcuts import render
import calendar
from calendar import HTMLCalendar, month_name
from datetime import datetime
from .models import Event, Venue
from .forms import VenueForm, EventForm
from django.urls import reverse
# Create your views here.


def home(request, year=datetime.now().year, month=datetime.now().strftime('%B')):

    # convert month from name to number
    month = month.title()
    month_number = list(calendar.month_name).index(month)
    month_number = int(month_number)

    # create a calendar
    cal = HTMLCalendar().formatmonth(year, month_number)

    # Get current year
    now = datetime.now()
    current_year = now.year

    # Get Current time
    time = now.strftime("%I:%M %p")

    return render(request, 'events/home.html', {
        "year": year,
        "month": month,
        "month_number": month,
        "calendar": cal,
        "current_year": current_year,
        "time": time
    })

def all_events(request):
    events = Event.objects.all()
    return render(request, 'events/all_events.html', {
        'events': events,
        # 'all_attendees': events.attendees.all()
    })


def add_venue(request):
    submitted = False
    if request.method == 'POST':
        venue_form = VenueForm(request.POST)
        if venue_form.is_valid():
            venue_form.save()
            return HttpResponseRedirect(reverse("add_venue") + "?submitted=True")
    else:
        venue_form = VenueForm()
        if "submitted" in request.GET:
            submitted = True

    return render(request, "events/add_venue.html", {
        "form": venue_form,
        "submitted": submitted
    })


def list_venues(request):
    venues = Venue.objects.all()
    return render(request, 'events/all_venues.html', {
        'venues': venues
    })


def detail_venue(request, venue_id):
    venue = Venue.objects.get(pk=venue_id)
    return render(request, 'events/detail_venue.html', {
        'venue': venue
    })


def search_venues(request):
    if request.method == "POST":
        search_input = request.POST['search_input']
        # print(f'input user --> {search_input}')
        searched_venues = Venue.objects.filter(name__contains=search_input)
        # print(f'venues --> {searched_venues}')
        # print(bool(searched_venues))
        return render(request, 'events/search_venues.html', {
            'searched_venues': searched_venues,
            'search_input': search_input
        })
    else:
        return render(request, 'events/search_venues.html', {})

def update_venue(request, venue_id):
    submitted = False
    existing_venue = Venue.objects.get(pk=venue_id)
    if request.method == "POST":
        venue_form = VenueForm(request.POST, instance=existing_venue)
        if venue_form.is_valid():
            venue_form.save()
            return HttpResponseRedirect(reverse("update-venue", args=[existing_venue.id]) + "?submitted=True")
    else:
        venue_form = VenueForm(instance=existing_venue)
        if "submitted" in request.GET:
            submitted = True

    return render(request, 'events/update_venue.html', {
        'form': venue_form,
        'submitted': submitted
    })


def add_event(request):
    submitted = False
    if request.method == 'POST':
        event_form = EventForm(request.POST)
        if event_form.is_valid():
            event_form.save()
            return HttpResponseRedirect(reverse("add-event") + "?submitted=True")
    else:
        event_form = EventForm()
        if "submitted" in request.GET:
            submitted = True

    return render(request, "events/add_event.html", {
        "form": event_form,
        "submitted": submitted
    })