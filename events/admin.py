from django.contrib import admin
from .models import Event, MyClubUser, Venue

# class EventAdmin(admin.ModelAdmin):
#     list_display = ("name", "date", "venue")
#     list_filter = ("date", "venue")

# Register your models here.

# admin.site.register(Venue)
admin.site.register(MyClubUser)
# admin.site.register(Event, EventAdmin)

@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin):
    list_display = ("name", "address", "phone")
    # ordering data based on alphabet on names
    ordering = ("name",)
    search_fields = ("name", "address")


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    fields = (("name", "venue"), "date", "description", "manager")
    list_display = ("name", "date", "venue")
    list_filter = ("date", "venue")
    ordering = ("date",)