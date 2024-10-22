from django.shortcuts import render
from .forms import UserForm  # Import UserForm
from django.shortcuts import redirect, render

def index(request):
    return render(request, 'includes/home.html')

def home(request):
    products = [
        {"name": "Apple MacBook Pro 17\"", "color": "Silver", "category": "Laptop", "price": 2999},
        {"name": "Microsoft Surface Pro", "color": "White", "category": "Laptop PC", "price": 1999},
        {"name": "Magic Mouse 2", "color": "Black", "category": "Accessories", "price": 99},
    ]

    additional_data = {
        "headers": ["Name", "Color", "Category", "Price"],
        "caption_title": "Our products",
        "caption_description": "Browse a list of Flowbite products designed to help you work and play, stay organized, get answers, keep in touch, grow your business, and more."
    }
    context = {
        'products': products,
        'additional_data': additional_data,
    }
    return render(request, 'includes/home.html', context)

def dashboard(request):
    return render(request, 'includes/dashboard.html')

def user_register(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user_success')
    else:
        form = UserForm()
    return render(request, 'includes/user/user_register.html', {'form': form})

def user_success(request):
    return render(request, 'includes/user/user_success.html')