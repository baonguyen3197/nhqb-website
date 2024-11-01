from django.urls import path
from .views import user_register, user_success, user_profile, CustomLoginView, CustomLogoutView, delete_user, booking_history

urlpatterns = [
    path('register/', user_register, name='user_register'),
    path('success/', user_success, name='user_success'),
    path('profile/', user_profile, name='user_profile'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('delete/', delete_user, name='delete_user'),
    path('booking_history/', booking_history, name='booking_history'),
]