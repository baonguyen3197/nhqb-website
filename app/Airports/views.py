from django.shortcuts import render
from django.core.paginator import Paginator
from .models import Airport

def airport_list(request):
    airports = Airport.objects.all()
    paginator = Paginator(airports, 5)  # Show 5 airports per page

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    additional_data = {
        'caption_title': 'Airport List',
        'caption_description': 'List of all airports with their details',
        'headers': ['IATA', 'Location', 'ICAO', 'Airport Name', 'Coordinate', 'Type']
    }
    return render(request, 'includes/airport/airport_list.html', {'page_obj': page_obj, 'additional_data': additional_data})