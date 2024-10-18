from django.shortcuts import render
from .forms import UserForm  # Import UserForm
from django.shortcuts import redirect

def index(request):
    return render(request, 'includes/home.html')

def home(request):
    return render(request, 'includes/home.html')

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