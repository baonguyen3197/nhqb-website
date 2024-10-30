from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.core.paginator import Paginator
from .models import Hotel, Booking
from datetime import datetime

def hotel_list(request):
    query = request.GET.get('q')
    hotel_list = Hotel.objects.filter(is_active=True)
    
    if query:
        hotel_list = hotel_list.filter(name__icontains=query)
    
    paginator = Paginator(hotel_list, 10)  # Show 10 hotels per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'includes/booking/hotel_list.html', {'page_obj': page_obj, 'query': query})


def hotel_detail(request, pk):
    hotel = get_object_or_404(Hotel, pk=pk, is_active=True)
    return render(request, 'includes/booking/hotel_detail.html', {'hotel': hotel})

def book_hotel(request, hotel_id):
    hotel = get_object_or_404(Hotel, pk=hotel_id)
    user = request.user
    start_date = request.POST.get('start_date')
    end_date = request.POST.get('end_date')

    if hotel.check_availability(start_date, end_date):
        Booking.objects.create(hotel=hotel, user=user, start_date=start_date, end_date=end_date)
        hotel.update_status()
        return JsonResponse({'status': 'success', 'message': 'Booking successful'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Hotel is not available for the selected dates'})