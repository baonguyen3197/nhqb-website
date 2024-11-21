# app/Bookings/admin.py

from django.contrib import admin
from django.core.management import call_command
from django.contrib import messages
from .models import Hotel

def randomize_hotel_status(modeladmin, request, queryset):
    if request.user.is_superuser:
        try:
            call_command('randomize_hotel_status')
            messages.success(request, "Hotel statuses randomized successfully.")
        except Exception as e:
            messages.error(request, f"Error randomizing hotel statuses: {e}")
    else:
        messages.error(request, "You do not have permission to perform this action.")

randomize_hotel_status.short_description = "Randomize Hotel Status"

class HotelAdmin(admin.ModelAdmin):
    actions = [randomize_hotel_status]

admin.site.register(Hotel, HotelAdmin)