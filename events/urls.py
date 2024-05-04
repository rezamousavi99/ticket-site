from django.urls import path
from events import views

urlpatterns = [

    path('', views.home, name='home'),
    # int, str, path, slug, UID: Universally Unique Identifier(user number)
    path('<int:year>/<str:month>/', views.home),
    path('events', views.all_events, name='all_events'),
    path('add-venue', views.add_venue, name='add_venue'),
    path('list-venues', views.list_venues, name='list_venues'),
    path('show-venues/<venue_id>', views.detail_venue, name='detail_venue'),
]