from django.shortcuts import render
import calendar
from calendar import HTMLCalendar, month_name
from datetime import datetime
from .models import Event
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
    return render(request, 'events/all-events.html', {
        'events': events,
        # 'all_attendees': events.attendees.all()
    })
