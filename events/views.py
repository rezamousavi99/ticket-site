from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
import calendar
from calendar import HTMLCalendar, month_name
from datetime import datetime
from .models import Event, Venue
from .forms import VenueForm, EventForm, AdminEventForm
from django.urls import reverse
import csv

from django.http import FileResponse
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter

from django.core.paginator import Paginator
from django.contrib.auth.models import User

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

def all_events(request, error_message=2):
    if request.method == 'POST':
        search_input = request.POST.get('search_input')
        searched_events = Event.objects.filter(name__contains=search_input)
        print('*' * 40)
        print(search_input)
        print(searched_events)
        print('*' * 40)

        return render(request, 'events/all_events.html', {
            'events': searched_events,
            'search_input': search_input,
            'error_message': error_message
        })
    else:
        events = Event.objects.all().order_by('date')
        return render(request, 'events/all_events.html', {
            'events': events,
            'error_message': error_message
            # 'all_attendees': events.attendees.all()
        })


def add_venue(request):
    submitted = False
    if request.method == 'POST':
        venue_form = VenueForm(request.POST)
        if venue_form.is_valid():
            venue = venue_form.save(commit=False)
            venue.owner = request.user.id
            venue.save()
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
    # venues = Venue.objects.all().order_by('name')
    venue_list = Venue.objects.all()

    #set up Pagination
    p = Paginator(venue_list, 4)
    page = request.GET.get('page')
    venues = p.get_page(page)
    nums = 'a' * venues.paginator.num_pages
    # print(nums)

    return render(request, 'events/all_venues.html', {
        # 'venue_list': venue_list,
        'venues': venues,
        'nums': nums
    })


def detail_venue(request, venue_id):
    venue = Venue.objects.get(pk=venue_id)
    venue_owner = User.objects.get(pk=venue.owner)
    return render(request, 'events/detail_venue.html', {
        'venue': venue,
        'venue_owner': venue_owner
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

# def search_events(request):
#     if request.method == "POST":
#         search_input = request.POST.get('search_input')
#         searched_events = Event.objects.filter(name__contains=search_input)
#
#         return render(request, 'events/search_events.html', {
#             'searched_events': searched_events,
#             'search_input': search_input
#         })
#     else:
#         return render(request, 'events/search_events.html', {})

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
        if request.user.is_superuser:
            event_form = AdminEventForm(request.POST)
            if event_form.is_valid():
                event_form.save()
                return HttpResponseRedirect(reverse("add-event") + "?submitted=True")
        else:
            event_form = EventForm(request.POST)
            if event_form.is_valid():
                event = event_form.save(commit=False)
                event.manager = request.user
                event.save()
                return HttpResponseRedirect(reverse("add-event") + "?submitted=True")
    else:
        if request.user.is_superuser:
            event_form = AdminEventForm()
        else:
            event_form = EventForm()
        if "submitted" in request.GET:
            submitted = True

    return render(request, "events/add_event.html", {
        "form": event_form,
        "submitted": submitted
    })


def update_event(request, event_id):
    submitted = False
    existing_event = Event.objects.get(pk=event_id)
    if request.method == 'POST':
        if request.user.is_superuser:
            event_form = AdminEventForm(request.POST, instance=existing_event)
        else:
            event_form = EventForm(request.POST, instance=existing_event)
        if event_form.is_valid():
            event_form.save()
            return HttpResponseRedirect(reverse("update-event", args=[existing_event.id]) + "?submitted=True")
    else:
        if request.user.is_superuser:
            event_form = AdminEventForm(instance=existing_event)
        else:
            event_form = EventForm(instance=existing_event)

        if "submitted" in request.GET:
            submitted = True

    return render(request, "events/update_event.html", {
        "event": existing_event,
        "form": event_form,
        "submitted": submitted
    })


#BUG
def delete_event(request, event_id):
    # events = Event.objects.all().order_by('date')
    error_massage = False
    event = Event.objects.get(pk=event_id)
    # event = events.get(id=event_id)
    if request.user == event.manager:
        event.delete()
        return all_events(request, error_massage)
    else:
        error_massage = True
        # return all_events(request, error_massage)
        return HttpResponseRedirect(reverse("all_events"))


# def delete_event(request, event_id):
#     events = Event.objects.all().order_by('date')
#     error_massage = False
#     # event = Event.objects.get(pk=event_id)
#     event = events.get(id=event_id)
#     if request.user == event.manager:
#         event.delete()
#     else:
#         error_massage = True
#     # return HttpResponseRedirect(reverse("all_events"))
#     return render(request, "events/all_events.html", {
#         'error_massage': error_massage,
#         'events': events
#     })

def delete_venue(request, venue_id):
    venue = Venue.objects.get(pk=venue_id)
    venue.delete()
    return HttpResponseRedirect(reverse("list_venues"))

def venue_text(request):
    response = HttpResponse(content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename=venues.txt'

    venues = Venue.objects.all()
    lines = []
    for venue in venues:
        lines.append(f'name: {venue.name}\n')
        lines.append(f'address: {venue.address}\n')
        lines.append(f'zip code: {venue.zip_code}\n')
        lines.append(f'phone: {venue.phone}\n')
        lines.append(f'website: {venue.website}\n')
        lines.append(f'email address: {venue.email_address}\n')
        lines.append('-' * 40 + '\n')

    response.writelines(lines)
    return response


def venue_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=venues.csv'

    writer = csv.writer(response)
    writer.writerow(['Name', 'Address', 'Zip Code', 'Phone', 'Website', 'Email'])
    venues = Venue.objects.all()
    for venue in venues:
        writer.writerow([venue.name, venue.address, venue.zip_code, venue.phone, venue.website, venue.email_address])
    return response


def venue_pdf(request):
    # Create Bytestream buffer
    buf = io.BytesIO()
    # Create a canvas
    c = canvas.Canvas(buf, pagesize=letter, bottomup=0)
    # Create a text object
    textob = c.beginText()
    textob.setTextOrigin(inch, inch)
    textob.setFont('Helvetica', 14)

    # Add some lines of text
    venues = Venue.objects.all()
    lines = []
    for venue in venues:
        lines.append(f'name: {venue.name}')
        lines.append(f'address: {venue.address}')
        lines.append(f'zip code: {venue.zip_code}')
        lines.append(f'phone: {venue.phone}')
        lines.append(f'website: {venue.website}')
        lines.append(f'email address: {venue.email_address}')
        lines.append('-' * 40)

    # Loop
    for line in lines:
        textob.textLine(line)

    # Finish Up
    c.drawText(textob)
    c.showPage()
    c.save()
    buf.seek(0)

    return FileResponse(buf, as_attachment=True, filename='venues.pdf')

def my_events(request):
    #BUG
    user_attendee = request.user.id
    my_events = Event.objects.filter(attendees=user_attendee)
    return render(request, 'events/my_events.html', {
        'my_events': my_events,
    })