from django.shortcuts import render, redirect

def index(request):
    return render(request, 'includes/home.html')

def home(request):
    products = [
        {"name": "Apple MacBook Pro 17\"", "color": "Silver", "category": "Laptop", "price": 2999},
        {"name": "Microsoft Surface Pro", "color": "White", "category": "Laptop PC", "price": 1999},
        {"name": "Magic Mouse 2", "color": "Black", "category": "Accessories", "price": 99},
    ]

    additional_data = {
        "headers": ["Location", "ICAO", "IATA", "Airport name", "Coordinates"],
        "caption_title": "Civil airports",
        "caption_description": "This is a list of airports in Vietnam, grouped by type and sorted by location. Airports in Vietnam are managed and operated by Airports Corporation of Vietnam."
    }
    context = {
        'products': products,
        'additional_data': additional_data,
    }
    return render(request, 'includes/home.html', context)

def dashboard(request):
    return render(request, 'includes/dashboard.html')
